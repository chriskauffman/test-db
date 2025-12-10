import pytest

import test_db

TEST_ENCRYPTION_KEY = "a test encryption key"


@pytest.fixture(scope="module")
def temporary_db(tmp_path_factory):
    test_db.autoCreateDependents = True
    test_db.databaseEncryptionKey = TEST_ENCRYPTION_KEY
    db_file = tmp_path_factory.mktemp("data") / "test_db_test.sqlite"
    return test_db.DatabaseController(db_file, create=True)
