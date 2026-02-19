import pytest
from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb import app as tdb


def test_address_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "person-address",
            "add",
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert captured.out.startswith("addr_")


def test_address_add_with_owner(capsys, monkeypatch, person, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "person-address",
            "add",
            "--person-gid",
            str(person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("addr_")


def test_address_add_with_bad_owner(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "person-address",
            "add",
            "--person-gid",
            "test_01kah9p4b0ejfb7apkkr2abr7c",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "does not exist" in captured.err


def test_address_bulk_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", "person-address", "bulk-add", "--count", "10"],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.err


def test_address_delete(capsys, monkeypatch, temporary_db, person):
    test_address = test_db.PersonAddress(
        person=person, connection=temporary_db.connection
    )
    assert (
        test_db.PersonAddress.get(test_address.id, connection=temporary_db.connection)
        is test_address
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "person-address",
            "delete",
            str(test_address.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        test_db.PersonAddress.get(test_address.id, connection=temporary_db.connection)


def test_address_list(capsys, monkeypatch, temporary_db, tmp_path_factory, person):
    address = test_db.PersonAddress(person=person, connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "person-address",
            "list",
            "--person-gid",
            str(person.gID),
        ],
    )
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert str(address.gID) in captured.out
    assert captured.out.count("addr_") >= 1


def test_address_view(capsys, monkeypatch, temporary_db, person):
    address = test_db.PersonAddress(person=person, connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "person-address",
            "view",
            str(address.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert str(address.gID) in captured.out
