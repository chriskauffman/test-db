import pytest

from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb_console import main as tdb


def test_organization_key_value_add(capsys, monkeypatch, temporary_db):
    organization = test_db.Organization(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "set command_interaction false",
            f"tdb_organization_key_value_add {organization.gID} test_key_value_add test_key_value_add_value",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.err


def test_organization_key_value_delete(capsys, monkeypatch, temporary_db, organization):
    organization_key_value = test_db.OrganizationKeyValue(
        connection=temporary_db.connection,
        organization=organization,
        key="test_organization_key_value_delete",
        value="test_organization_key_value_delete_value",
    )
    assert (
        test_db.OrganizationKeyValue.get(
            organization_key_value.id, connection=temporary_db.connection
        )
        is organization_key_value
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_organization_key_value_delete {organization.gID} {organization_key_value.key}",
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
        test_db.OrganizationKeyValue.get(
            organization_key_value.id, connection=temporary_db.connection
        )


def test_organization_key_value_list(capsys, monkeypatch, temporary_db):
    organization = test_db.Organization(connection=temporary_db.connection)
    organization_key_value = test_db.OrganizationKeyValue(
        connection=temporary_db.connection,
        organization=organization,
        key="test_organization_key_value_list",
        value="test_organization_key_value_list_value",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_organization_key_value_list {organization.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert organization_key_value.key in captured.out


def test_organization_key_value_view(capsys, monkeypatch, temporary_db):
    organization = test_db.Organization(connection=temporary_db.connection)
    organization_key_value = test_db.OrganizationKeyValue(
        connection=temporary_db.connection,
        organization=organization,
        key="test_organization_key_value_view",
        value="test_organization_key_value_view_value",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_organization_key_value_view {organization.gID} {organization_key_value.key}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "test_organization_key_value_view" in captured.out
    assert "test_organization_key_value_view_value" in captured.out
