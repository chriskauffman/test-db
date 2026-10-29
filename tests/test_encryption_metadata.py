import base64
import sqlite3
from unittest.mock import Mock

import pytest
import sqlobject
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import test_db
from test_db import DatabaseController, KeyValue, Person, PersonSecureKeyValue

SALT_KEY = "TestDB_EncryptedPickleColSalt"
ITERATIONS_KEY = "TestDB_EncryptedPickleColIterations"
PASSWORD = "regression-test-password"
ITERATIONS = 1_000
LEGACY_SALT = "0123456789abcdef0123456789abcdef"


@pytest.fixture
def encryption_uri(tmp_path, monkeypatch):
    monkeypatch.setattr(test_db, "databaseEncryptionKey", None)
    monkeypatch.setattr(test_db, "fernetIterations", ITERATIONS)
    uri = f"sqlite:{tmp_path / 'encryption.sqlite'}"
    yield uri
    sqlobject.connectionForURI(uri).close()


def _open(uri, password=PASSWORD):
    # SQLObject caches connections and rows; force reads from persisted data.
    sqlobject.connectionForURI(uri).cache.clear()
    return DatabaseController(uri, databaseEncryptionKey=password)


def _metadata(uri):
    with sqlite3.connect(uri.removeprefix("sqlite:")) as connection:
        return dict(
            connection.execute(
                "SELECT key_name, value FROM key_value WHERE key_name IN (?, ?)",
                (SALT_KEY, ITERATIONS_KEY),
            )
        )


@pytest.fixture
def legacy_database(encryption_uri):
    # Initialize only the schema, independently of encryption metadata creation.
    db = _open(encryption_uri, password=None)
    KeyValue(key=SALT_KEY, value=LEGACY_SALT, connection=db.connection)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=LEGACY_SALT.encode(),
        iterations=ITERATIONS,
    )
    db.connection.dbFernet = Fernet(
        base64.urlsafe_b64encode(kdf.derive(PASSWORD.encode()))
    )
    person = Person(connection=db.connection)
    PersonSecureKeyValue(
        person=person, key="null", value=None, connection=db.connection
    )
    record = PersonSecureKeyValue(
        person=person,
        key="legacy",
        value={"legacy": 123},
        connection=db.connection,
    )
    record_id = record.id
    db.close()
    assert _metadata(encryption_uri) == {SALT_KEY: LEGACY_SALT}
    return encryption_uri, record_id


def test_reopen_uses_persisted_iterations(encryption_uri, monkeypatch):
    db = _open(encryption_uri)
    person_id = Person(connection=db.connection).id
    first_id = PersonSecureKeyValue(
        person=person_id,
        key="first",
        value={"number": 123},
        connection=db.connection,
    ).id
    salt = _metadata(encryption_uri)[SALT_KEY]
    db.close()

    monkeypatch.setattr(test_db, "fernetIterations", ITERATIONS * 2)
    db = _open(encryption_uri)
    assert PersonSecureKeyValue.get(first_id, connection=db.connection).value == {
        "number": 123
    }
    second_id = PersonSecureKeyValue(
        person=person_id, key="second", value="new value", connection=db.connection
    ).id
    db.close()

    # Persisted settings must win even over an invalid runtime setting.
    monkeypatch.setattr(test_db, "fernetIterations", 0)
    db = _open(encryption_uri)
    assert PersonSecureKeyValue.get(first_id, connection=db.connection).value == {
        "number": 123
    }
    assert (
        PersonSecureKeyValue.get(second_id, connection=db.connection).value
        == "new value"
    )
    assert _metadata(encryption_uri) == {
        SALT_KEY: salt,
        ITERATIONS_KEY: str(ITERATIONS),
    }
    db.close()


def test_legacy_backfill_authenticates_without_unpickling(legacy_database, monkeypatch):
    uri, record_id = legacy_database
    with sqlite3.connect(uri.removeprefix("sqlite:")) as connection:
        ciphertext = connection.execute(
            "SELECT value FROM person_secure_key_value WHERE id = ?", (record_id,)
        ).fetchone()
    with monkeypatch.context() as patch:
        loads = Mock(side_effect=AssertionError("migration must not unpickle"))
        patch.setattr("test_db._encrypted_pickle_col.pickle.loads", loads)
        db = _open(uri)
        loads.assert_not_called()
    assert _metadata(uri) == {
        SALT_KEY: LEGACY_SALT,
        ITERATIONS_KEY: str(ITERATIONS),
    }
    with sqlite3.connect(uri.removeprefix("sqlite:")) as connection:
        assert (
            connection.execute(
                "SELECT value FROM person_secure_key_value WHERE id = ?",
                (record_id,),
            ).fetchone()
            == ciphertext
        )
    db.close()

    monkeypatch.setattr(test_db, "fernetIterations", ITERATIONS * 2)
    db = _open(uri)
    assert PersonSecureKeyValue.get(record_id, connection=db.connection).value == {
        "legacy": 123
    }
    db.close()


@pytest.mark.parametrize("wrong_setting", ["iterations", "password"])
def test_failed_legacy_authentication_allows_retry(
    legacy_database, monkeypatch, wrong_setting
):
    uri, record_id = legacy_database
    monkeypatch.setattr(
        test_db,
        "fernetIterations",
        ITERATIONS * 2 if wrong_setting == "iterations" else ITERATIONS,
    )
    password = "wrong-password" if wrong_setting == "password" else PASSWORD
    with pytest.raises(ValueError, match="original password and iteration count"):
        _open(uri, password=password)
    assert _metadata(uri) == {SALT_KEY: LEGACY_SALT}

    monkeypatch.setattr(test_db, "fernetIterations", ITERATIONS)
    db = _open(uri)
    assert PersonSecureKeyValue.get(record_id, connection=db.connection).value == {
        "legacy": 123
    }
    assert _metadata(uri)[ITERATIONS_KEY] == str(ITERATIONS)
    db.close()


@pytest.mark.parametrize("null_record", [False, True])
def test_legacy_without_ciphertext_can_backfill(encryption_uri, null_record):
    db = _open(encryption_uri, password=None)
    KeyValue(key=SALT_KEY, value=LEGACY_SALT, connection=db.connection)
    if null_record:
        PersonSecureKeyValue(
            person=Person(connection=db.connection),
            key="null",
            value=None,
            connection=db.connection,
        )
    db.close()
    db = _open(encryption_uri)
    assert _metadata(encryption_uri) == {
        SALT_KEY: LEGACY_SALT,
        ITERATIONS_KEY: str(ITERATIONS),
    }
    db.close()


@pytest.mark.parametrize("count", ["invalid", "0", "-1", None])
def test_invalid_stored_iterations_leave_metadata_unchanged(legacy_database, count):
    uri, _ = legacy_database
    with sqlite3.connect(uri.removeprefix("sqlite:")) as connection:
        connection.execute(
            "INSERT INTO key_value (key_name, value) VALUES (?, ?)",
            (ITERATIONS_KEY, count),
        )
    before = _metadata(uri)
    with pytest.raises(ValueError, match="positive integer"):
        _open(uri)
    assert _metadata(uri) == before


@pytest.mark.parametrize("count", [0, -1, 1.5, True])
def test_invalid_configured_iterations_do_not_create_metadata(
    encryption_uri, monkeypatch, count
):
    monkeypatch.setattr(test_db, "fernetIterations", count)
    with pytest.raises(ValueError, match="positive integer"):
        _open(encryption_uri)
    assert _metadata(encryption_uri) == {}


def test_iterations_without_salt_do_not_generate_replacement(encryption_uri):
    db = _open(encryption_uri, password=None)
    KeyValue(key=ITERATIONS_KEY, value=str(ITERATIONS), connection=db.connection)
    db.close()
    before = _metadata(encryption_uri)
    with pytest.raises(ValueError, match="salt"):
        _open(encryption_uri)
    assert _metadata(encryption_uri) == before


@pytest.mark.parametrize("existing_metadata", ["empty", "salt-only", "complete"])
def test_no_password_leaves_encryption_metadata_unchanged(
    encryption_uri, existing_metadata
):
    if existing_metadata == "complete":
        _open(encryption_uri).close()
    else:
        db = _open(encryption_uri, password=None)
        if existing_metadata == "salt-only":
            KeyValue(key=SALT_KEY, value=LEGACY_SALT, connection=db.connection)
        db.close()
    before = _metadata(encryption_uri)
    db = _open(encryption_uri, password=None)
    assert db.connection.dbFernet is None
    assert _metadata(encryption_uri) == before
    db.close()


def test_wrong_password_cannot_read_persisted_ciphertext(encryption_uri):
    db = _open(encryption_uri)
    record_id = PersonSecureKeyValue(
        person=Person(connection=db.connection),
        key="secret",
        value="original value",
        connection=db.connection,
    ).id
    before = _metadata(encryption_uri)
    db.close()
    db = _open(encryption_uri, password="wrong-password")
    with pytest.raises(InvalidToken):
        _ = PersonSecureKeyValue.get(record_id, connection=db.connection).value
    assert _metadata(encryption_uri) == before
    db.close()
    db = _open(encryption_uri)
    assert (
        PersonSecureKeyValue.get(record_id, connection=db.connection).value
        == "original value"
    )
    db.close()
