import pytest
from sqlobject import SQLObjectNotFound

import test_db as db
from test_db.tdb import app as tdb


def test_bank_account_add(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--db-file-path", db_file, "bank-account", "add"]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("ba_")


def test_bank_account_add_with_owner(capsys, monkeypatch, db_file, person):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "bank-account",
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
    assert captured.out.startswith("ba_")


def test_bank_account_add_with_bad_owner(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "bank-account",
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


def test_bank_account_connect(capsys, monkeypatch, db_file, temporary_db):
    test_bank_account = db.BankAccount(connection=temporary_db.connection)

    test_person = db.Person(connection=temporary_db.connection)

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "bank-account",
            "connect",
            str(test_bank_account.gID),
            str(test_person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.BankAccount.get(test_bank_account.id)
    assert db.Person.get(test_person.id)
    assert test_bank_account in test_person.bankAccounts

    test_organization = db.Organization(connection=temporary_db.connection)

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "bank-account",
            "connect",
            str(test_bank_account.gID),
            str(test_organization.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.BankAccount.get(test_bank_account.id)
    assert db.Organization.get(test_organization.id)
    assert test_bank_account in test_organization.bankAccounts


def test_bank_account_delete(capsys, monkeypatch, db_file, temporary_db):
    test_bank_account = db.BankAccount(connection=temporary_db.connection)
    assert (
        db.BankAccount.get(test_bank_account.id, connection=temporary_db.connection)
        is test_bank_account
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "bank-account",
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
        db.BankAccount.get(test_bank_account.id, connection=temporary_db.connection)


def test_bank_account_disconnect(capsys, monkeypatch, db_file, temporary_db):
    test_bank_account = db.BankAccount(connection=temporary_db.connection)

    test_person = db.Person(connection=temporary_db.connection)
    test_person.addBankAccount(test_bank_account)

    assert test_bank_account in test_person.bankAccounts

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "bank-account",
            "disconnect",
            str(test_bank_account.gID),
            str(test_person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.BankAccount.get(test_bank_account.id)
    assert db.Person.get(test_person.id)
    assert test_bank_account not in test_person.bankAccounts

    test_organization = db.Organization(connection=temporary_db.connection)
    test_organization.addBankAccount(test_bank_account)

    assert test_bank_account in test_organization.bankAccounts

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "bank-account",
            "disconnect",
            str(test_bank_account.gID),
            str(test_organization.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.BankAccount.get(test_bank_account.id)
    assert db.Organization.get(test_organization.id)
    assert test_bank_account not in test_organization.bankAccounts


def test_bank_account_list(
    capsys, monkeypatch, db_file, temporary_db, tmp_path_factory
):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_address_listes.sqlite")
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", "--create", "--db-file-path", empty_db_file, "bank-account", "list"],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    db.BankAccount(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--db-file-path", db_file, "bank-account", "list"]
    )
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("ba_")
    assert captured.out.count("ba_") >= 1


def test_bank_account_view(capsys, monkeypatch, db_file, temporary_db):
    bank_account = db.BankAccount(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "bank-account",
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
