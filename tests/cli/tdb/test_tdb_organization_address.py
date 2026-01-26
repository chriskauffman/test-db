import pytest
from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb import app as tdb


def test_address_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "organization-address",
            "add",
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert captured.out.startswith("addr_")


def test_address_add_with_owner(capsys, monkeypatch, organization, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "organization-address",
            "add",
            "--organization-gid",
            str(organization.gID),
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
            "organization-address",
            "add",
            "--organization-gid",
            "test_01kah9p4b0ejfb7apkkr2abr7c",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "does not exist" in captured.err


def test_address_delete(capsys, monkeypatch, temporary_db, organization):
    test_address = test_db.OrganizationAddress(
        organization=organization, connection=temporary_db.connection
    )
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
            "organization-address",
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


def test_address_list(
    capsys, monkeypatch, temporary_db, tmp_path_factory, organization
):
    address = test_db.OrganizationAddress(
        organization=organization, connection=temporary_db.connection
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "organization-address",
            "list",
            "--organization-gid",
            str(organization.gID),
        ],
    )
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert str(address.gID) in captured.out
    assert captured.out.count("addr_") >= 1


def test_address_view(capsys, monkeypatch, temporary_db, organization):
    address = test_db.OrganizationAddress(
        organization=organization, connection=temporary_db.connection
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "organization-address",
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
