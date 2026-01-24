import pytest
from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb import app as tdb


def test_address_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", "--db-connection-uri", temporary_db.connectionURI, "address", "add"],
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
            "--db-connection-uri",
            temporary_db.connectionURI,
            "address",
            "add",
            "--entity-gid",
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
            "--db-connection-uri",
            temporary_db.connectionURI,
            "address",
            "add",
            "--entity-gid",
            "test_01kah9p4b0ejfb7apkkr2abr7c",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_address_delete(capsys, monkeypatch, temporary_db):
    test_address = test_db.OrganizationAddress(connection=temporary_db.connection)
    assert (
        test_db.OrganizationAddress.get(
            test_address.id, connection=temporary_db.connection
        )
        is test_address
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "address",
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
        test_db.OrganizationAddress.get(
            test_address.id, connection=temporary_db.connection
        )


def test_address_list(capsys, monkeypatch, temporary_db, tmp_path_factory):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_address_listes.sqlite")
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            f"sqlite:{empty_db_file}",
            "address",
            "list",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    test_db.OrganizationAddress(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", "--db-connection-uri", temporary_db.connectionURI, "address", "list"],
    )
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("addr_")
    assert captured.out.count("addr_") >= 1


def test_address_view(capsys, monkeypatch, temporary_db):
    address = test_db.OrganizationAddress(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "address",
            "view",
            str(address.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("\nAddress ID: addr_")
