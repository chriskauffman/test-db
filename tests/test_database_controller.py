import os
import shutil
import sqlite3
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import sqlobject
from sqlobject.dberrors import IntegrityError

import test_db
from test_db._database_controller import DatabaseController, _migration_statements
from test_db._person import Person
from test_db._person_address import PersonAddress


def db_schema_is_valid(database_contoller):
    # assert (
    #     database_contoller._rawCursor.execute("PRAGMA application_id").fetchone()[0]
    #     == APPLICATION_ID
    # )
    # assert (
    #     database_contoller._rawCursor.execute("PRAGMA schema_version").fetchone()[0] > 0
    # )
    # assert (
    #     database_contoller._rawCursor.execute("PRAGMA user_version").fetchone()[0]
    #     == CURRENT_APPLICATION_SCHEMA_VERSION
    # )

    # assert (
    #     len(
    #         database_contoller._rawCursor.execute(
    #             f"PRAGMA index_list({test_db.BankAccount.sqlmeta.table})"
    #         ).fetchall()
    #     )
    #     == 2
    # )
    # assert (
    #     len(
    #         database_contoller._rawCursor.execute(
    #             f"PRAGMA index_list({test_db.DebitCard.sqlmeta.table})"
    #         ).fetchall()
    #     )
    #     == 2
    # )
    # assert (
    #     len(
    #         database_contoller._rawCursor.execute(
    #             f"PRAGMA index_list({test_db.Job.sqlmeta.table})"
    #         ).fetchall()
    #     )
    #     == 2
    # )

    assert database_contoller.validSchema

    return True


def test_init():
    db = DatabaseController(test_db.IN_MEMORY_DB_FILE)

    # assert isinstance(db.filePath, pathlib.Path)
    assert db.connection
    assert db_schema_is_valid(db)


def test_default_connection_create_signals(tmp_path):
    db = DatabaseController(
        f"sqlite:{tmp_path / 'default-connection.sqlite'}",
        defaultConnection=True,
    )
    previous_connection = sqlobject.sqlhub.processConnection
    previous_auto_create_dependents = test_db.autoCreateDependents
    test_db.autoCreateDependents = True
    try:
        person = test_db.Person()
        organization = test_db.Organization()

        assert person._connection is db.connection
        assert organization._connection is db.connection
        assert sqlobject.sqlhub.processConnection is db.connection
        assert test_db.PersonAddress.select().count() == 1
        assert test_db.PersonBankAccount.select().count() == 1
        assert test_db.PersonDebitCard.select().count() == 1
        assert test_db.OrganizationAddress.select().count() == 1
        assert test_db.OrganizationBankAccount.select().count() == 1
    finally:
        test_db.autoCreateDependents = previous_auto_create_dependents
        db.close()
        sqlobject.sqlhub.processConnection = previous_connection


def test_multiple_memory_connections(tmp_path_factory):
    db_1 = DatabaseController(test_db.IN_MEMORY_DB_FILE)
    db_2 = DatabaseController(test_db.IN_MEMORY_DB_FILE)

    # Note: two memory db's seem to have one connection
    assert db_1.connection == db_2.connection

    # __connection__ = db_1.connection
    # assert db_1.connection == Person(connection=db_1.connection)._connection

    # __connection__ = db_2.connection
    # assert db_2.connection == Person(connection=db_2.connection)._connection


def test_multiple_file_connections(tmp_path_factory):
    db_1_file = tmp_path_factory.mktemp("data") / "test_multiple_connections_1.sqlite"
    db_1 = DatabaseController(f"sqlite://{db_1_file}")
    db_2_file = tmp_path_factory.mktemp("data") / "test_multiple_connections_2.sqlite"
    db_2 = DatabaseController(f"sqlite://{db_2_file}")

    assert db_1.connection != db_2.connection

    # __connection__ = db_1.connection
    assert db_1.connection == Person(connection=db_1.connection)._connection

    # __connection__ = db_2.connection
    assert db_2.connection == Person(connection=db_2.connection)._connection


def test_file_version_1(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("data") / "test_file_version_1.sqlite"
    # shutil.copy2("tests/data/test.9.sqlite", db_file)

    db = DatabaseController(f"sqlite://{db_file}")

    assert db_schema_is_valid(db)


def test_upgrade_from_schema_v1(tmp_path):
    db_file = tmp_path / "test_schema_v1.sqlite"
    database = DatabaseController(f"sqlite:{db_file}")
    cursor = database._rawCursor
    cursor.execute("PRAGMA foreign_keys=OFF")
    cursor.execute(
        """
        CREATE TABLE job_old (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            g_id VARCHAR(90) NOT NULL UNIQUE,
            description TEXT,
            employee_id TEXT,
            location TEXT,
            pay_group TEXT,
            position TEXT,
            organization_id INT REFERENCES organization(id),
            person_id INT REFERENCES person(id),
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
        """
    )
    cursor.execute("INSERT INTO job_old SELECT * FROM job")
    cursor.execute("DROP TABLE job")
    cursor.execute("ALTER TABLE job_old RENAME TO job")
    cursor.execute(
        "CREATE UNIQUE INDEX job_employeeIDOrganizationIndex "
        "ON job (employee_id, organization_id)"
    )
    cursor.execute(
        """
        CREATE TABLE person_secure_key_value (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INT NOT NULL REFERENCES person(id) ON DELETE CASCADE,
            key_name TEXT NOT NULL,
            value TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
        """
    )
    cursor.execute(
        "CREATE UNIQUE INDEX person_secure_key_value_personKeyIndex "
        "ON person_secure_key_value (person_id, key_name)"
    )
    database.applicationSchemaVersion = 1
    database.close()

    upgraded = DatabaseController(f"sqlite:{db_file}", upgrade=True)
    try:
        assert upgraded.applicationSchemaVersion == 2
        assert upgraded.validSchema
        assert not upgraded.connection.tableExists("person_secure_key_value")
    finally:
        upgraded.close()


def test_mysql_migration_skips_completed_foreign_key_steps():
    database = object.__new__(DatabaseController)
    database.connection = SimpleNamespace(dbName="mysql")
    database._rawCursor = Mock()
    database._rawCursor.fetchone.return_value = ("CASCADE",)

    database._execute_migration_statement(
        "ALTER TABLE job ADD CONSTRAINT job_organization_id_exists "
        "FOREIGN KEY (organization_id) REFERENCES organization (id) "
        "ON DELETE CASCADE"
    )

    database._rawCursor.execute.assert_called_once_with(
        "SELECT delete_rule "
        "FROM information_schema.referential_constraints "
        "WHERE constraint_schema = DATABASE() "
        "AND constraint_name = %s",
        ("job_organization_id_exists",),
    )


def test_migration_statements_strip_sql_comments():
    assert list(
        _migration_statements("-- comment\nALTER TABLE job DROP FOREIGN KEY fk;")
    ) == ["ALTER TABLE job DROP FOREIGN KEY fk"]


def test_failed_upgrade_restores_sqlite_foreign_keys(tmp_path, monkeypatch):
    database = DatabaseController(f"sqlite:{tmp_path / 'failed_upgrade.sqlite'}")
    database.applicationSchemaVersion = 1
    monkeypatch.setattr(
        database,
        "_execute_migration_statement",
        Mock(side_effect=RuntimeError("migration failed")),
    )

    try:
        with pytest.raises(ValueError, match="unable to upgrade test_db schema"):
            database._upgrade()
        assert database.applicationSchemaVersion == 1
        assert database._rawCursor.execute("PRAGMA foreign_keys").fetchone() == (1,)
    finally:
        database.close()


def test_failed_upgrade_validation_rolls_back(tmp_path, monkeypatch):
    database = DatabaseController(f"sqlite:{tmp_path / 'invalid_upgrade.sqlite'}")
    database.applicationSchemaVersion = 1
    monkeypatch.setattr(database, "_raw_schema_is_valid", Mock(return_value=False))

    try:
        with pytest.raises(ValueError, match="unable to upgrade test_db schema"):
            database._upgrade()
        assert database.applicationSchemaVersion == 1
    finally:
        database.close()


def test_open_empty(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("data") / "test_open_empty.sqlite"
    if os.path.isfile(db_file):
        os.remove(db_file)
    test_db = DatabaseController(f"sqlite://{db_file}")

    assert test_db.validSchema

    test_users = Person.select(connection=test_db.connection)

    assert not test_users.count()


@pytest.fixture(params=["file", "memory"])
def sqlite_db(request, tmp_path, monkeypatch):
    monkeypatch.setattr(test_db, "autoCreateDependents", False)
    uri = (
        "sqlite:/:memory:?cache=False"
        if request.param == "memory"
        else f"sqlite:{tmp_path / 'foreign_keys.sqlite'}?timeout=0.25"
    )
    db = DatabaseController(uri)
    try:
        yield db
    finally:
        db.close()


def test_sqlite_foreign_keys_enabled_for_raw_and_orm(sqlite_db):
    assert sqlite_db._rawCursor.execute("PRAGMA foreign_keys").fetchone() == (1,)
    assert sqlite_db.connection.queryOne("PRAGMA foreign_keys") == (1,)
    assert (
        sqlobject.connectionForURI(sqlite_db.connectionURI.get_secret_value())
        is sqlite_db.connection
    )


def test_sqlite_rejects_orphan_address(sqlite_db):
    with pytest.raises(IntegrityError, match="FOREIGN KEY constraint failed"):
        PersonAddress(person=999999, connection=sqlite_db.connection)
    assert PersonAddress.select(connection=sqlite_db.connection).count() == 0


def test_sqlite_new_physical_connections_enforce_foreign_keys(sqlite_db):
    first = sqlite_db.connection.getConnection()
    second = sqlite_db.connection.getConnection()
    try:
        if not sqlite_db.connection._memory:
            assert first is not second
            assert first is not sqlite_db._raw
        assert first.execute("PRAGMA foreign_keys").fetchone() == (1,)
        assert second.execute("PRAGMA foreign_keys").fetchone() == (1,)
    finally:
        sqlite_db.connection.releaseConnection(second)
        sqlite_db.connection.releaseConnection(first)


def test_sqlite_reopen_enforces_foreign_keys(sqlite_db):
    connection = sqlite_db.connection
    uri = sqlite_db.connectionURI.get_secret_value()
    sqlite_db.close()
    # In-memory close eagerly creates a replacement physical connection.
    if connection._memory:
        assert connection._memoryConn.execute("PRAGMA foreign_keys").fetchone() == (1,)
    reopened = DatabaseController(uri)
    try:
        assert reopened.connection is connection
        assert reopened.connection.queryOne("PRAGMA foreign_keys") == (1,)
        with pytest.raises(IntegrityError, match="FOREIGN KEY constraint failed"):
            PersonAddress(person=999999, connection=reopened.connection)
    finally:
        reopened.close()


def test_sqlite_valid_nullable_and_cascading_relationships(sqlite_db):
    connection = sqlite_db.connection
    person = Person(connection=connection)
    address = PersonAddress(person=person, connection=connection)
    unowned = PersonAddress(person=None, connection=connection)
    assert address.personID == person.id
    assert unowned.personID is None
    # Bypass SQLObject's own cascading deletes to verify the database constraint.
    connection.query(f"DELETE FROM person WHERE id = {person.id}")
    assert PersonAddress.selectBy(id=address.id, connection=connection).count() == 0
    assert PersonAddress.selectBy(id=unowned.id, connection=connection).count() == 1
    assert connection.queryAll("PRAGMA foreign_key_check") == []


def test_sqlite_configures_preexisting_cached_connection(tmp_path, monkeypatch):
    uri = f"sqlite:{tmp_path / 'cached.sqlite'}"
    connection = sqlobject.connectionForURI(uri)
    assert connection.queryOne("PRAGMA foreign_keys") == (0,)
    db = DatabaseController(uri)
    try:
        assert db.connection is connection
        assert connection.queryOne("PRAGMA foreign_keys") == (1,)
        assert db._rawCursor.execute("PRAGMA foreign_keys").fetchone() == (1,)
    finally:
        db.close()


def test_close_does_not_close_preexisting_cached_connection(tmp_path):
    uri = f"sqlite:{tmp_path / 'cached-close.sqlite'}"
    connection = sqlobject.connectionForURI(uri)
    db = DatabaseController(uri)

    db.close()

    assert connection.queryOne("PRAGMA foreign_keys") == (1,)
    connection.close()


def test_open_empty_existing_file(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("data") / "test_open_empty_existing_file.sqlite"
    shutil.copy2("tests/data/test_empty.sqlite", db_file)

    test_db = DatabaseController(f"sqlite://{db_file}")

    assert db_schema_is_valid(test_db)

    test_users = Person.select(connection=test_db.connection)

    assert not test_users.count()


def test_open_foreign_database_refused(tmp_path):
    db_file = tmp_path / "foreign.sqlite"
    raw = sqlite3.connect(db_file)
    raw.execute("CREATE TABLE t (x)")
    raw.commit()
    raw.close()

    with pytest.raises(ValueError, match="not a test_db file"):
        DatabaseController(f"sqlite:{db_file}")

    raw = sqlite3.connect(db_file)
    tables = [r[0] for r in raw.execute("SELECT name FROM sqlite_master")]
    raw.close()
    assert tables == ["t"]


def test_failed_open_closes_connection(tmp_path):
    db_file = tmp_path / "foreign.sqlite"
    raw = sqlite3.connect(db_file)
    raw.execute("CREATE TABLE t (x)")
    raw.commit()
    raw.close()

    with pytest.raises(ValueError, match="not a test_db file"):
        DatabaseController(f"sqlite:{db_file}")

    assert f"sqlite:{db_file}" not in sqlobject.connectionForURI.__self__.cachedURIs
