import pytest
from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb import app as tdb


def test_bank_account_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "organization-bank-account",
            "add",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("ba_")


def test_bank_account_add_with_owner(capsys, monkeypatch, organization, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "organization-bank-account",
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
    assert captured.out.startswith("ba_")


def test_bank_account_add_with_bad_owner(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "organization-bank-account",
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


def test_bank_account_delete(capsys, monkeypatch, temporary_db, organization):
    test_bank_account = test_db.OrganizationBankAccount(
        organization=organization, connection=temporary_db.connection
    )
    assert (
        test_db.OrganizationBankAccount.get(
            test_bank_account.id, connection=temporary_db.connection
        )
        is test_bank_account
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "organization-bank-account",
            "delete",
            str(test_bank_account.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        test_db.OrganizationBankAccount.get(
            test_bank_account.id, connection=temporary_db.connection
        )


def test_bank_account_list(capsys, monkeypatch, temporary_db, organization):
    test_db.OrganizationBankAccount(
        organization=organization, connection=temporary_db.connection
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "organization-bank-account",
            "list",
            str(organization.gID),
        ],
    )
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("ba_")
    assert captured.out.count("ba_") >= 1


def test_bank_account_view(capsys, monkeypatch, temporary_db, organization):
    bank_account = test_db.OrganizationBankAccount(
        organization=organization, connection=temporary_db.connection
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "organization-bank-account",
            "view",
            str(bank_account.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("ba_")
