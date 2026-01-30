import pytest
from sqlobject import SQLObjectNotFound
import uuid

import test_db
from test_db.tdb import app as tdb


def test_person_secure_key_value_add(capsys, monkeypatch, person, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "person-secure-key-value",
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


def test_person_secure_key_value_add_bad_person(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "person-secure-key-value",
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


def test_person_secure_key_value_delete(capsys, monkeypatch, person, temporary_db):
    test_person_secure_key_value = test_db.PersonSecureKeyValue(
        connection=temporary_db.connection,
        key="test_delete_person_secure_key_value",
        person=person,
    )
    assert (
        test_db.PersonSecureKeyValue.get(
            test_person_secure_key_value.id, connection=temporary_db.connection
        )
        is test_person_secure_key_value
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "person-secure-key-value",
            "delete",
            str(person.gID),
            test_person_secure_key_value.key,
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        test_db.PersonSecureKeyValue.get(
            test_person_secure_key_value.id, connection=temporary_db.connection
        )


def test_person_secure_key_value_list(capsys, monkeypatch, person, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "person-secure-key-value",
            "list",
            str(person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out


def test_person_secure_key_value_view(capsys, monkeypatch, person, temporary_db):
    test_key = str(uuid.uuid4())
    person.getSecureKeyValueByKey(test_key, value="test value")
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "person-secure-key-value",
            "view",
            str(person.gID),
            test_key,
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert test_key in captured.out
