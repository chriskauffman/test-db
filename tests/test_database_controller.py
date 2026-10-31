import os
import shutil
import sqlite3

import pytest
import sqlobject
from sqlobject.dberrors import IntegrityError

import test_db
from test_db._database_controller import DatabaseController
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


# def test_schema_X_upgrade(tmp_path_factory, db_encryption_key):
#     test_db.databaseEncryptionKey = db_encryption_key
#     db_file = tmp_path_factory.mktemp("data") / "upgrade_0.sqlite"
#     shutil.copy2("tests/data/test.0.sqlite", db_file)

#     raw_connection = sqlite3.connect(db_file)
#     raw_cursor = raw_connection.cursor()

#     assert raw_cursor.execute("PRAGMA application_id").fetchone()[0] == 0
#     assert raw_cursor.execute("PRAGMA user_version").fetchone()[0] == 0

#     test_db = DatabaseController(db_file, defaultConnection=True)

#     assert db_schema_is_valid(test_db)


def test_file_version_1(tmp_path_factory, db_encryption_key):
    test_db.databaseEncryptionKey = db_encryption_key
    db_file = tmp_path_factory.mktemp("data") / "test_file_version_1.sqlite"
    # shutil.copy2("tests/data/test.9.sqlite", db_file)

    db = DatabaseController(f"sqlite://{db_file}")

    assert db_schema_is_valid(db)


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
    monkeypatch.setattr(test_db, "databaseEncryptionKey", None)
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
    monkeypatch.setattr(test_db, "databaseEncryptionKey", None)
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
