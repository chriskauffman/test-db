import pytest
from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb import app as tdb


def test_organization_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "organization",
            "add",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("o_")


def test_organization_delete(capsys, monkeypatch, temporary_db):
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
            "--db-connection-uri",
            temporary_db.connectionURI,
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


def test_organization_list(capsys, monkeypatch, temporary_db, tmp_path_factory):
    test_db.Organization(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "organization",
            "list",
        ],
    )
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("o_")
    assert captured.out.count("o_") >= 1


def test_organization_view(capsys, monkeypatch, organization, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
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
