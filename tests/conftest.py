import os
import pytest

import test_db

TEST_ENCRYPTION_KEY = "a test encryption key"


@pytest.fixture(scope="module")
def db_encryption_key():
    return os.getenv("PYTEST_DATABASE_ENCRYPTION_KEY") or TEST_ENCRYPTION_KEY


@pytest.fixture(scope="module")
def temporary_db(tmp_path_factory, db_encryption_key):
    db_connection_uri = os.getenv("PYTEST_DATABASE_CONNECTION_URI")

    test_db.autoCreateDependents = True
    test_db.databaseEncryptionKey = db_encryption_key
    if db_connection_uri:
        return test_db.DatabaseController(db_connection_uri)
    else:
        db_file = tmp_path_factory.mktemp("data") / "test_db_test.sqlite"
        return test_db.DatabaseController(f"sqlite://{db_file}")
