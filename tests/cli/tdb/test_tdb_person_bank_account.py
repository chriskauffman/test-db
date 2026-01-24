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
            "bank-account",
            "add",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("ba_")


def test_bank_account_add_with_owner(capsys, monkeypatch, person, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
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


def test_bank_account_add_with_bad_owner(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
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


def test_bank_account_delete(capsys, monkeypatch, temporary_db):
    test_bank_account = test_db.PersonBankAccount(connection=temporary_db.connection)
    assert (
        test_db.PersonBankAccount.get(
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
        test_db.PersonBankAccount.get(
            test_bank_account.id, connection=temporary_db.connection
        )


def test_bank_account_list(capsys, monkeypatch, temporary_db, tmp_path_factory):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_address_listes.sqlite")
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            f"sqlite:{empty_db_file}",
            "bank-account",
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

    test_db.PersonBankAccount(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "bank-account",
            "list",
        ],
    )
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("ba_")
    assert captured.out.count("ba_") >= 1


def test_bank_account_view(capsys, monkeypatch, temporary_db):
    bank_account = test_db.PersonBankAccount(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
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
