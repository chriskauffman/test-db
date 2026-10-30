import pytest
import sqlobject
from cryptography.fernet import InvalidToken

import test_db
from test_db._views._key_value import KeyValueView
from test_db.tdb import app as cli
from test_db.tdb_console import main as console

PASSWORD = "regression-test-password"
WRONG_PASSWORD = "wrong-password"
ITERATIONS = 1_000
KEY = "secret"
DECRYPTION_ERROR = "Unable to decrypt"


@pytest.fixture
def wrong_key_database(tmp_path, monkeypatch):
    """Persist encrypted data with one key, then reopen it with another"""
    monkeypatch.setattr(test_db, "fernetIterations", ITERATIONS)
    uri = f"sqlite:{tmp_path / 'wrong-key.sqlite'}"
    db = test_db.DatabaseController(uri, databaseEncryptionKey=PASSWORD)
    person = test_db.Person(connection=db.connection)
    test_db.PersonSecureKeyValue(
        person=person,
        key=KEY,
        value="original value",
        connection=db.connection,
    )
    person_gid = str(person.gID)
    db.close()

    # SQLObject caches connections and rows; force reads from persisted data.
    sqlobject.connectionForURI(uri).cache.clear()
    db = test_db.DatabaseController(uri, databaseEncryptionKey=WRONG_PASSWORD)
    yield db, uri, person_gid
    db.close()


def test_model_read_raises_invalid_token(wrong_key_database):
    db, _, person_gid = wrong_key_database
    person = test_db.Person.byGID(person_gid, connection=db.connection)

    with pytest.raises(InvalidToken):
        _ = person.secureKeyValues[0].value


def test_list_reports_decryption_error(capsys, wrong_key_database):
    db, _, person_gid = wrong_key_database
    person = test_db.Person.byGID(person_gid, connection=db.connection)

    KeyValueView.list(person.secureKeyValuesSelect)

    assert DECRYPTION_ERROR in capsys.readouterr().out


@pytest.mark.parametrize("command", ["list", "view", "edit"])
def test_cli_reports_decryption_error(capsys, monkeypatch, wrong_key_database, command):
    _, uri, person_gid = wrong_key_database
    monkeypatch.setenv("DATABASE_ENCRYPTION_KEY", WRONG_PASSWORD)
    arguments = [person_gid] if command == "list" else [person_gid, KEY]
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", "-d", uri, "person-secure-key-value", command, *arguments],
    )

    with pytest.raises(SystemExit) as exc:
        cli()
    captured = capsys.readouterr()

    assert exc.value.code == (0 if command == "list" else 1)
    assert DECRYPTION_ERROR in captured.out + captured.err


@pytest.mark.parametrize("command", ["list", "view"])
def test_console_reports_decryption_error(
    capsys, monkeypatch, wrong_key_database, command
):
    _, uri, person_gid = wrong_key_database
    monkeypatch.setenv("DB_CONNECTION_URI", uri)
    monkeypatch.setenv("DATABASE_ENCRYPTION_KEY", WRONG_PASSWORD)
    arguments = f"{person_gid}" if command == "list" else f"{person_gid} {KEY}"
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", f"tdb_person_secure_key_value_{command} {arguments}", "quit"],
    )

    with pytest.raises(SystemExit) as exc:
        console()
    captured = capsys.readouterr()

    assert exc.value.code == 0
    assert DECRYPTION_ERROR in captured.out + captured.err
