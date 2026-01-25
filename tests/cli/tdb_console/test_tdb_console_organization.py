import pytest

from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb_console import main as tdb


def test_organization_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "set command_interaction false",
            "tdb_organization_add",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert test_db.Organization._gIDPrefix in captured.out

def test_organization_delete(capsys, monkeypatch, temporary_db):
    organization = test_db.Organization(connection=temporary_db.connection)
    assert (
        test_db.Organization.get(organization.id, connection=temporary_db.connection)
        is organization
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_organization_delete {organization.gID}",
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
        test_db.Organization.get(organization.id, connection=temporary_db.connection)

def test_organization_list(capsys, monkeypatch, temporary_db):
    organization = test_db.Organization(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "tdb_organization_list",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert str(organization.gID) in captured.out

def test_organization_view(capsys, monkeypatch, temporary_db):
    organization = test_db.Organization(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_organization_view {organization.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert str(organization.gID) in captured.out
