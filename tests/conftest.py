import pytest

import test_db as db

TEST_ENCRYPTION_KEY = "a test encryption key"


@pytest.fixture(scope="module")
def memory_db():
    db.autoCreateDependents = True
    db.databaseEncryptionKey = TEST_ENCRYPTION_KEY
    return db.DatabaseController(db.IN_MEMORY_DB_FILE, create=True)


@pytest.fixture(scope="module")
def temporary_db(tmp_path_factory):
    db.autoCreateDependents = True
    db.databaseEncryptionKey = TEST_ENCRYPTION_KEY
    db_file = tmp_path_factory.mktemp("data") / "test_db_test.sqlite"
    return db.DatabaseController(db_file, create=True)
