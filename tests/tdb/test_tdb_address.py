import pytest
from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb import app as tdb


def test_address_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--db-file-path", temporary_db.filePath, "address", "add"]
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
            "--db-file-path",
            temporary_db.filePath,
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
            "--db-file-path",
            temporary_db.filePath,
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


def test_address_connect(capsys, monkeypatch, temporary_db):
    test_address = test_db.Address(connection=temporary_db.connection)

    test_person = test_db.Person(connection=temporary_db.connection)

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "address",
            "connect",
            str(test_address.gID),
            str(test_person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert test_db.Address.get(test_address.id)
    assert test_db.Person.get(test_person.id)
    assert test_address in test_person.addresses

    test_organization = test_db.Organization(connection=temporary_db.connection)

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "address",
            "connect",
            str(test_address.gID),
            str(test_organization.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert test_db.Address.get(test_address.id)
    assert test_db.Organization.get(test_organization.id)
    assert test_address in test_organization.addresses


def test_address_delete(capsys, monkeypatch, temporary_db):
    test_address = test_db.Address(connection=temporary_db.connection)
    assert (
        test_db.Address.get(test_address.id, connection=temporary_db.connection)
        is test_address
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
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
        test_db.Address.get(test_address.id, connection=temporary_db.connection)


def test_address_disconnect(capsys, monkeypatch, temporary_db):
    test_address = test_db.Address(connection=temporary_db.connection)

    test_person = test_db.Person(connection=temporary_db.connection)
    test_person.addAddress(test_address)

    assert test_address in test_person.addresses

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "address",
            "disconnect",
            str(test_address.gID),
            str(test_person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert test_db.Address.get(test_address.id)
    assert test_db.Person.get(test_person.id)
    assert test_address not in test_person.addresses

    test_organization = test_db.Organization(connection=temporary_db.connection)
    test_organization.addAddress(test_address)

    assert test_address in test_organization.addresses

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
            "address",
            "disconnect",
            str(test_address.gID),
            str(test_organization.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert test_db.Address.get(test_address.id)
    assert test_db.Organization.get(test_organization.id)
    assert test_address not in test_organization.addresses


def test_address_list(capsys, monkeypatch, temporary_db, tmp_path_factory):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_address_listes.sqlite")
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--create",
            "--db-file-path",
            empty_db_file,
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

    test_db.Address(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--db-file-path", temporary_db.filePath, "address", "list"]
    )
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("addr_")
    assert captured.out.count("addr_") >= 1


def test_address_view(capsys, monkeypatch, temporary_db):
    address = test_db.Address(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            temporary_db.filePath,
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
