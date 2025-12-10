import pytest
from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb import app as tdb


def test_key_value_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "key-value",
            "add",
            "test_add_key_value",
            "test_value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out


def test_add_key_value_duplicate(capsys, monkeypatch, temporary_db):
    test_db.KeyValue(
        key="test_add_key_value_duplicate",
        value="test_value",
        connection=temporary_db.connection,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "key-value",
            "add",
            "test_add_key_value_duplicate",
            "test_value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "UNIQUE constraint failed" in captured.err


def test_key_value_delete(capsys, monkeypatch, temporary_db):
    test_key_value = test_db.KeyValue(
        connection=temporary_db.connection, key="test_delete_key_value"
    )
    assert (
        test_db.KeyValue.get(test_key_value.id, connection=temporary_db.connection)
        is test_key_value
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "key-value",
            "delete",
            test_key_value.key,
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        test_db.KeyValue.get(test_key_value.id, connection=temporary_db.connection)
