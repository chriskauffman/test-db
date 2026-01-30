import pytest

from sqlobject import SQLObjectNotFound

import uuid

import test_db
from test_db.tdb_console import main as tdb


def test_key_value_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "set command_interaction false",
            f"tdb_key_value_add {uuid.uuid4()} test_key_value_add_value",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.err


def test_job_delete(capsys, monkeypatch, temporary_db):
    key_value = test_db.KeyValue(
        connection=temporary_db.connection, key=str(uuid.uuid4()), value="test"
    )
    assert (
        test_db.KeyValue.get(key_value.id, connection=temporary_db.connection)
        is key_value
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_key_value_delete {key_value.key}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        test_db.KeyValue.get(key_value.id, connection=temporary_db.connection)


def test_key_value_view(capsys, monkeypatch, temporary_db):
    key_value = test_db.KeyValue(
        connection=temporary_db.connection, key=str(uuid.uuid4()), value="test"
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_key_value_view {key_value.key}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert key_value.key in captured.out
    assert key_value.value in captured.out
