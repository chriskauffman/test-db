import os
import pytest

import test_db


@pytest.fixture(scope="module")
def organization(temporary_db):
    return test_db.Organization(connection=temporary_db.connection)


@pytest.fixture(scope="module")
def person(temporary_db):
    return test_db.Person(connection=temporary_db.connection)


@pytest.fixture(scope="module", autouse=True)
def set_env(db_encryption_key, temporary_db, tmp_path_factory):
    os.environ["DATABASE_ENCRYPTION_KEY"] = db_encryption_key
    os.environ["BACKUP_PATH"] = str(tmp_path_factory.mktemp("backup"))
    os.environ["LOG_LEVEL_FILE"] = "DEBUG"
    os.environ["LOG_PATH"] = str(tmp_path_factory.mktemp("log"))
    # setting DB connection to avoid defaulting to a real DB in tests
    os.environ["DB_CONNECTION_URI"] = temporary_db.connectionURI
