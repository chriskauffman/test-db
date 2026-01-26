import pytest

from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb_console import main as tdb


def test_bank_account_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "set command_interaction false",
            "tdb_organization_bank_account_add",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert test_db.OrganizationBankAccount._gIDPrefix in captured.out


def test_bank_account_delete(capsys, monkeypatch, temporary_db, organization):
    bank_account = test_db.OrganizationBankAccount(
        organization=organization, connection=temporary_db.connection
    )
    assert (
        test_db.OrganizationBankAccount.get(
            bank_account.id, connection=temporary_db.connection
        )
        is bank_account
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_organization_bank_account_delete {bank_account.gID}",
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
        test_db.OrganizationBankAccount.get(
            bank_account.id, connection=temporary_db.connection
        )


def test_bank_account_list(capsys, monkeypatch, temporary_db, organization):
    bank_account = test_db.OrganizationBankAccount(
        organization=organization, connection=temporary_db.connection
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "tdb_organization_bank_account_list",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert str(bank_account.gID) in captured.out


def test_bank_account_view(capsys, monkeypatch, temporary_db, organization):
    bank_account = test_db.OrganizationBankAccount(
        organization=organization, connection=temporary_db.connection
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_organization_bank_account_view {bank_account.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert str(bank_account.gID) in captured.out
