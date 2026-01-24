import pytest
from sqlobject import SQLObjectNotFound
import uuid

import test_db
from test_db.tdb import app as tdb


def test_organization_key_value_add(capsys, monkeypatch, organization, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "organization-key-value",
            "add",
            str(organization.gID),
            "secret",
            "value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out


def test_organization_key_value_delete(capsys, monkeypatch, organization, temporary_db):
    test_organization_key_value = test_db.OrganizationKeyValue(
        connection=temporary_db.connection,
        itemKey="test_delete_organization_key_value",
        organization=organization,
    )
    assert (
        test_db.OrganizationKeyValue.get(
            test_organization_key_value.id, connection=temporary_db.connection
        )
        is test_organization_key_value
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "organization-key-value",
            "delete",
            str(organization.gID),
            test_organization_key_value.itemKey,
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
            test_organization_key_value.id, connection=temporary_db.connection
        )


def test_organization_key_value_list(capsys, monkeypatch, organization, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "organization-key-value",
            "list",
            str(organization.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out


def test_organization_key_value_view(capsys, monkeypatch, organization, temporary_db):
    test_key = str(uuid.uuid4())
    organization.getKeyValueByKey(test_key, itemValue="test value")
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "organization-key-value",
            "view",
            str(organization.gID),
            test_key,
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert test_key in captured.out
