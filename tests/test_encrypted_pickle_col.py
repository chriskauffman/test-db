import datetime
import pytest

from sqlobject import SQLObject

import test_db as db
from test_db._encrypted_pickle_col import EncryptedPickleCol

TEST_ENCRYPTION_KEY = "a really good key"


class SecureTable(SQLObject):
    value: EncryptedPickleCol = EncryptedPickleCol(default=None)


@pytest.fixture(scope="session")
def encryption_db(tmp_path_factory):
    db.databaseEncryptionKey = TEST_ENCRYPTION_KEY
    db_file = tmp_path_factory.mktemp("data") / "test_db_encryption_test.sqlite"
    encryption_db = db.DatabaseController(db_file, create=True)
    SecureTable.createTable(connection=encryption_db.connection)
    return encryption_db


def test_no_encryption_key(tmp_path_factory):
    db.databaseEncryptionKey = None
    db_file = tmp_path_factory.mktemp("data") / "test_no_encryption_key.sqlite"
    encryption_db = db.DatabaseController(db_file, create=True)
    SecureTable.createTable(connection=encryption_db.connection)

    with pytest.raises(ValueError, match="Invalid Fernet config, check dbFernet value"):
        SecureTable(value=123, connection=encryption_db.connection)


def test_set_various_values(encryption_db):
    test_token = SecureTable(
        value={},
        connection=encryption_db.connection,
    )

    assert isinstance(test_token.value, dict)
    assert test_token.value == {}

    test_token.value = "abc123"
    assert test_token.value == "abc123"

    test_token.value = 1234
    assert test_token.value == 1234

    test_token.value = 1234.11
    assert test_token.value == 1234.11

    test_token.value = datetime.datetime(2020, 1, 1, 12, 0, 0)
    assert test_token.value == datetime.datetime(2020, 1, 1, 12, 0, 0)


# def test_bank_account(encryption_db):
#     SecureTable.new(connection=encryption_db.connection)
