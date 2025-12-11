import pytest
from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb import app as tdb


def test_personal_key_value_secure_add(capsys, monkeypatch, person, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "personal-key-value-secure",
            "add",
            str(person.gID),
            "secret",
            "value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out


def test_personal_key_value_secure_add_bad_person(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "personal-key-value-secure",
            "add",
            "test_01kah9p4b0ejfb7apkkr2abr7c",
            "secret",
            "value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "does not exist" in captured.err


def test_personal_key_value_secure_add_duplicate(
    capsys, monkeypatch, person, temporary_db
):
    person.getPersonalKeyValueSecureByKey("secret2", value="test value")
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "personal-key-value-secure",
            "add",
            str(person.gID),
            "secret2",
            "value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "UNIQUE constraint failed" in captured.err


def test_personal_key_value_secure_delete(capsys, monkeypatch, person, temporary_db):
    test_personal_key_value_secure = test_db.PersonalKeyValueSecure(
        connection=temporary_db.connection,
        key="test_delete_personal_key_value_secure",
        person=person,
    )
    assert (
        test_db.PersonalKeyValueSecure.get(
            test_personal_key_value_secure.id, connection=temporary_db.connection
        )
        is test_personal_key_value_secure
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "personal-key-value-secure",
            "delete",
            str(person.gID),
            test_personal_key_value_secure.key,
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        test_db.PersonalKeyValueSecure.get(
            test_personal_key_value_secure.id, connection=temporary_db.connection
        )
