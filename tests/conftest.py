import os

import pytest

import test_db


@pytest.fixture(scope="session")
def temporary_db(tmp_path_factory):
    db_connection_uri = os.getenv("PYTEST_DATABASE_CONNECTION_URI")

    test_db.autoCreateDependents = True
    if db_connection_uri:
        return test_db.DatabaseController(db_connection_uri)
    else:
        db_file = tmp_path_factory.mktemp("data") / "test_db_test.sqlite"
        return test_db.DatabaseController(f"sqlite://{db_file}")
