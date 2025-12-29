import os
import pytest

import test_db


@pytest.fixture(scope="module")
def person(temporary_db):
    return test_db.Person(connection=temporary_db.connection)


@pytest.fixture(scope="module")
def organization(temporary_db):
    return test_db.Organization(connection=temporary_db.connection)


@pytest.fixture(scope="module", autouse=True)
def set_env(temporary_db):
    # setting DB connection to avoid defaulting to a real DB in tests
    os.environ["DB_CONNECTION_URI"] = temporary_db.connectionURI
    os.environ["DATABASE_ENCRYPTION_KEY"] = "a test encryption key"
