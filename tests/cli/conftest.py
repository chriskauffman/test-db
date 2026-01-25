import os
import pytest

import test_db


@pytest.fixture(scope="module")
def cli_test_connection(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("data") / "test_db_cli_test.sqlite"
    return f"sqlite://{db_file}"


@pytest.fixture(scope="module")
def temporary_db(cli_test_connection):
    return test_db.DatabaseController(cli_test_connection)


@pytest.fixture(scope="module")
def organization(temporary_db):
    return test_db.Organization(connection=temporary_db.connection)


@pytest.fixture(scope="module")
def person(temporary_db):
    return test_db.Person(connection=temporary_db.connection)


@pytest.fixture(scope="module", autouse=True)
def set_env():
    os.environ["DATABASE_ENCRYPTION_KEY"] = "a test encryption key"
    os.environ["LOG_PATH"] = "log"
