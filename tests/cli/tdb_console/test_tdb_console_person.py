import pytest

from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb_console import main as tdb


def test_person_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "set command_interaction false",
            "tdb_person_add",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert test_db.Person._gIDPrefix in captured.out


def test_person_delete(capsys, monkeypatch, temporary_db):
    person = test_db.Person(connection=temporary_db.connection)
    assert test_db.Person.get(person.id, connection=temporary_db.connection) is person

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_person_delete {person.gID}",
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
        test_db.Person.get(person.id, connection=temporary_db.connection)


def test_person_list(capsys, monkeypatch, temporary_db):
    person = test_db.Person(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "tdb_person_list",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert str(person.gID) in captured.out


def test_person_view(capsys, monkeypatch, temporary_db):
    person = test_db.Person(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_person_view {person.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert str(person.gID) in captured.out
