import pytest
from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb import app as tdb


def test_entity_key_value_add(capsys, monkeypatch, person, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "entity-key-value",
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


def test_entity_key_value_add_bad_person(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "entity-key-value",
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
    assert "person or organization not found" in captured.err


def test_entity_key_value_add_duplicate(capsys, monkeypatch, person, temporary_db):
    person.getKeyValueByKey("secret2", value="test value")
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "entity-key-value",
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


def test_entity_key_value_delete(capsys, monkeypatch, person, temporary_db):
    test_entity_key_value = test_db.EntityKeyValue(
        connection=temporary_db.connection,
        key="test_delete_entity_key_value",
        entity=person,
    )
    assert (
        test_db.EntityKeyValue.get(
            test_entity_key_value.id, connection=temporary_db.connection
        )
        is test_entity_key_value
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "entity-key-value",
            "delete",
            str(person.gID),
            test_entity_key_value.key,
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        test_db.EntityKeyValue.get(
            test_entity_key_value.id, connection=temporary_db.connection
        )
