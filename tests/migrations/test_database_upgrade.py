"""Migration tests for disposable PostgreSQL, MySQL, and SQLite databases."""

import os

import pytest

from test_db._database_controller import DatabaseController

pytestmark = pytest.mark.migration


def _prepare_v1(database: DatabaseController) -> None:
    """Convert a fresh v2 database into the v1 shape used by the upgrade."""
    cursor = database._rawCursor
    engine = database.connection.dbName

    if engine == "sqlite":
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
        cursor.execute("PRAGMA foreign_keys=ON")
    elif engine == "postgres":
        cursor.execute("ALTER TABLE job DROP CONSTRAINT organization_id_exists")
        cursor.execute("ALTER TABLE job DROP CONSTRAINT person_id_exists")
        cursor.execute(
            "ALTER TABLE job ADD CONSTRAINT organization_id_exists "
            "FOREIGN KEY (organization_id) REFERENCES organization (id)"
        )
        cursor.execute(
            "ALTER TABLE job ADD CONSTRAINT person_id_exists "
            "FOREIGN KEY (person_id) REFERENCES person (id)"
        )
    elif engine == "mysql":
        cursor.execute("ALTER TABLE job DROP FOREIGN KEY job_organization_id_exists")
        cursor.execute("ALTER TABLE job DROP FOREIGN KEY job_person_id_exists")
        cursor.execute(
            "ALTER TABLE job ADD CONSTRAINT job_organization_id_exists "
            "FOREIGN KEY (organization_id) REFERENCES organization (id)"
        )
        cursor.execute(
            "ALTER TABLE job ADD CONSTRAINT job_person_id_exists "
            "FOREIGN KEY (person_id) REFERENCES person (id)"
        )
    else:
        raise AssertionError(f"unsupported test database: {engine}")

    cursor.execute("DROP TABLE IF EXISTS person_secure_key_value")
    if engine == "postgres":
        cursor.execute(
            """
            CREATE TABLE person_secure_key_value (
                id SERIAL PRIMARY KEY,
                person_id INT NOT NULL REFERENCES person(id),
                key_name TEXT NOT NULL,
                value TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
            """
        )
    elif engine == "mysql":
        cursor.execute(
            """
            CREATE TABLE person_secure_key_value (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                person_id INT NOT NULL,
                key_name TEXT NOT NULL,
                value TEXT,
                created_at TIMESTAMP NULL,
                updated_at TIMESTAMP NULL,
                FOREIGN KEY (person_id) REFERENCES person (id)
            )
            """
        )
    else:
        cursor.execute(
            """
            CREATE TABLE person_secure_key_value (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INT NOT NULL REFERENCES person(id),
                key_name TEXT NOT NULL,
                value TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
            """
        )
    cursor.execute(
        "DELETE FROM key_value WHERE key_name LIKE 'TestDB_EncryptedPickleCol%'"
    )
    cursor.execute(
        "INSERT INTO key_value (key_name, value) "
        "VALUES ('TestDB_EncryptedPickleColSalt', 'salt')"
    )
    database.applicationSchemaVersion = 1
    database._raw.commit()


@pytest.fixture
def migration_database():
    """Open the explicitly configured disposable migration database."""
    uri = os.getenv("PYTEST_MIGRATION_DATABASE_CONNECTION_URI")
    if not uri:
        pytest.skip("set PYTEST_MIGRATION_DATABASE_CONNECTION_URI to run")
    if os.getenv("PYTEST_ALLOW_DESTRUCTIVE_MIGRATION_TESTS") != "1":
        pytest.fail(
            "set PYTEST_ALLOW_DESTRUCTIVE_MIGRATION_TESTS=1 to run destructive tests"
        )

    database = DatabaseController(uri)
    try:
        _prepare_v1(database)
    finally:
        database.close()

    upgraded = DatabaseController(uri, upgrade=True)
    try:
        yield upgraded
    finally:
        upgraded.close()


def test_v1_to_v2_upgrade(migration_database):
    """Upgrade v1 and verify both schema changes on the target backend."""
    database = migration_database

    assert database.applicationSchemaVersion == 2
    assert database.validSchema
    assert not database.connection.tableExists("person_secure_key_value")
    assert (
        database._rawCursor.execute(
            "SELECT count(*) FROM key_value "
            "WHERE key_name LIKE 'TestDB_EncryptedPickleCol%'"
        ).fetchone()[0]
        == 0
    )
