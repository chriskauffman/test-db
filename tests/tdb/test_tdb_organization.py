import pytest
from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb import app as tdb


def test_organization_add(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--db-file-path", db_file, "organization", "add"]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("o_")


def test_organization_delete(capsys, monkeypatch, db_file, temporary_db):
    test_organization = test_db.Organization(connection=temporary_db.connection)
    assert (
        test_db.Organization.get(
            test_organization.id, connection=temporary_db.connection
        )
        is test_organization
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "organization",
            "delete",
            str(test_organization.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        test_db.Organization.get(
            test_organization.id, connection=temporary_db.connection
        )


def test_organization_list(
    capsys, monkeypatch, db_file, temporary_db, tmp_path_factory
):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_address_listes.sqlite")
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", "--create", "--db-file-path", empty_db_file, "organization", "list"],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    test_db.Organization(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--db-file-path", db_file, "organization", "list"]
    )
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("o_")
    assert captured.out.count("o_") >= 1


def test_organization_view(capsys, monkeypatch, db_file, organization):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "organization",
            "view",
            str(organization.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("\nOrganization ID: o_")
