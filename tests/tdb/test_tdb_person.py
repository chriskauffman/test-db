import pytest
from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb import app as tdb


def test_person_add(capsys, monkeypatch, db_file):
    monkeypatch.setattr("sys.argv", ["tdb", "--db-file-path", db_file, "person", "add"])

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("p_")


def test_person_delete(capsys, monkeypatch, db_file, temporary_db):
    test_person = test_db.Person(connection=temporary_db.connection)
    assert (
        test_db.Person.get(test_person.id, connection=temporary_db.connection)
        is test_person
    )

    monkeypatch.setattr(
        "sys.argv",
        ["tdb", "--db-file-path", db_file, "person", "delete", str(test_person.gID)],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        test_db.Person.get(test_person.id, connection=temporary_db.connection)


def test_person_list(capsys, monkeypatch, db_file, temporary_db, tmp_path_factory):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_address_listes.sqlite")
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", "--create", "--db-file-path", empty_db_file, "person", "list"],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    test_db.Person(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--db-file-path", db_file, "person", "list"]
    )
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("p_")
    assert captured.out.count("p_") >= 1


def test_person_view(capsys, monkeypatch, db_file, person):
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", "--db-file-path", db_file, "person", "view", str(person.gID)],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("\nPerson ID: p_")
