import base64
import datetime
import pytest
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from sqlobject import connectionForURI, SQLObject

from test_db._encrypted_pickle_col import EncryptedPickleCol

ENCODING = "utf-8"
TEST_ENCRYPTION_KEY = "a really good key"


@pytest.fixture(scope="session")
def fernet():
    fernet_salt = secrets.token_hex(16).encode(ENCODING)
    fernet_kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=fernet_salt,
        iterations=1_200_000,
    )
    fernet_key_material = TEST_ENCRYPTION_KEY.encode(ENCODING)
    key = base64.urlsafe_b64encode(fernet_kdf.derive(fernet_key_material))
    return Fernet(key)


def test_no_fernet(tmp_path_factory):
    class TestTableNoFernet(SQLObject):
        value: EncryptedPickleCol = EncryptedPickleCol(default=None)

    db_file = tmp_path_factory.mktemp("data") / "test_no_fernet.sqlite"
    connection = connectionForURI(f"sqlite:{db_file}")
    TestTableNoFernet.createTable(connection=connection)

    with pytest.raises(ValueError, match="Invalid Fernet config, check dbFernet value"):
        TestTableNoFernet(value=123, connection=encryption_db)


def test_sqlmeta_none(tmp_path_factory):
    class TestTableNoneMeta(SQLObject):
        class sqlmeta:
            dbFernet = None

        value: EncryptedPickleCol = EncryptedPickleCol(default=None)

    db_file = tmp_path_factory.mktemp("data") / "test_sqlmeta_none.sqlite"
    connection = connectionForURI(f"sqlite:{db_file}")
    TestTableNoneMeta.createTable(connection=connection)

    with pytest.raises(ValueError, match="Invalid Fernet config, check dbFernet value"):
        TestTableNoneMeta(value=123, connection=encryption_db)


def test_sqlmeta(tmp_path_factory, fernet):
    class TestTableMeta(SQLObject):
        class sqlmeta:
            dbFernet = fernet

        value: EncryptedPickleCol = EncryptedPickleCol(default=None)

    db_file = tmp_path_factory.mktemp("data") / "test_sqlmeta.sqlite"
    connection = connectionForURI(f"sqlite:{db_file}")
    TestTableMeta.createTable(connection=connection)

    test = TestTableMeta(value=123, connection=connection)

    assert isinstance(test, TestTableMeta)
    assert test.value == 123
    assert isinstance(test.sqlmeta.dbFernet, Fernet)
    assert isinstance(TestTableMeta.sqlmeta.dbFernet, Fernet)


def test_column_option_none(tmp_path_factory):
    class TestTableNoneOption(SQLObject):
        value: EncryptedPickleCol = EncryptedPickleCol(default=None, dbFernet=None)

    db_file = tmp_path_factory.mktemp("data") / "test_column_option_none.sqlite"
    connection = connectionForURI(f"sqlite:{db_file}")
    TestTableNoneOption.createTable(connection=connection)

    with pytest.raises(ValueError, match="Invalid Fernet config, check dbFernet value"):
        TestTableNoneOption(value=123, connection=encryption_db)


def test_column_option(tmp_path_factory, fernet):
    class TestTableOption(SQLObject):
        value: EncryptedPickleCol = EncryptedPickleCol(default=None, dbFernet=fernet)

    db_file = tmp_path_factory.mktemp("data") / "test_column_option.sqlite"
    connection = connectionForURI(f"sqlite:{db_file}")
    TestTableOption.createTable(connection=connection)

    test = TestTableOption(value=123, connection=connection)

    assert isinstance(test, TestTableOption)
    assert test.value == 123
    # ToDo: How do I confirm where the fernet is stored?
    # assert isinstance(test.sqlmeta.dbFernet, Fernet)
    # assert isinstance(TestTableOption.sqlmeta.dbFernet, Fernet)


def test_connection_none(tmp_path_factory):
    class TestTableNoneConnection(SQLObject):
        value: EncryptedPickleCol = EncryptedPickleCol(default=None)

    db_file = tmp_path_factory.mktemp("data") / "test_connection_none.sqlite"
    connection = connectionForURI(f"sqlite:{db_file}")
    connection.dbFernet = None
    TestTableNoneConnection.createTable(connection=connection)

    with pytest.raises(ValueError, match="Invalid Fernet config, check dbFernet value"):
        TestTableNoneConnection(value=123, connection=encryption_db)


def test_connection(tmp_path_factory, fernet):
    class TestTableConnection(SQLObject):
        value: EncryptedPickleCol = EncryptedPickleCol(default=None)

    db_file = tmp_path_factory.mktemp("data") / "test_connection.sqlite"
    connection = connectionForURI(f"sqlite:{db_file}")
    connection.dbFernet = fernet
    TestTableConnection.createTable(connection=connection)

    test = TestTableConnection(value=123, connection=connection)

    assert isinstance(test, TestTableConnection)
    assert test.value == 123
    assert isinstance(test._connection.dbFernet, Fernet)


class SecureTable(SQLObject):
    value: EncryptedPickleCol = EncryptedPickleCol(default=None)


@pytest.fixture(scope="session")
def encryption_db(tmp_path_factory, fernet):
    db_file = tmp_path_factory.mktemp("data") / "encryption_db.sqlite"
    connection = connectionForURI(f"sqlite:{db_file}")
    connection.dbFernet = fernet
    SecureTable.createTable(connection=connection)
    return connection


def test_set_various_values(encryption_db, fernet):
    test_token = SecureTable(
        value={
            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus non turpis non ipsum vestibulum tempor vel at risus. Donec molestie mi in leo tempus, ac congue sem congue. Phasellus nec hendrerit neque. In ut ex dolor. Mauris a mattis sem.",
            "amount": 123498776.67,
            "at": datetime.datetime(2020, 1, 1, 12, 0, 0),
        },
        connection=encryption_db,
    )

    assert isinstance(test_token.value, dict)
    assert (
        test_token.value["text"]
        == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus non turpis non ipsum vestibulum tempor vel at risus. Donec molestie mi in leo tempus, ac congue sem congue. Phasellus nec hendrerit neque. In ut ex dolor. Mauris a mattis sem."
    )
    assert test_token.value["amount"] == 123498776.67
    assert test_token.value["at"] == datetime.datetime(2020, 1, 1, 12, 0, 0)

    test_token.value = "abc123"
    assert isinstance(test_token.value, str)
    assert test_token.value == "abc123"

    test_token.value = 1234
    assert isinstance(test_token.value, int)
    assert test_token.value == 1234

    test_token.value = 1234.11
    assert isinstance(test_token.value, float)
    assert test_token.value == 1234.11

    test_token.value = datetime.datetime(2020, 1, 1, 12, 0, 0)
    assert isinstance(test_token.value, datetime.datetime)
    assert test_token.value == datetime.datetime(2020, 1, 1, 12, 0, 0)
