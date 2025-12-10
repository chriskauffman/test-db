import os
import pytest

import test_db


@pytest.fixture(scope="module")
def db_file(temporary_db):
    return str(temporary_db.filePath)


@pytest.fixture(scope="module")
def person(temporary_db):
    return test_db.Person(connection=temporary_db.connection)


@pytest.fixture(scope="module")
def organization(temporary_db):
    return test_db.Organization(connection=temporary_db.connection)


@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["DATABASE_ENCRYPTION_KEY"] = "a test encryption key"
