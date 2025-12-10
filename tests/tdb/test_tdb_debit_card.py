import pytest
from sqlobject import SQLObjectNotFound

import test_db as db
from test_db.tdb import app as tdb


def test_debit_card_add(capsys, monkeypatch, db_file, temporary_db):
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--db-file-path", db_file, "debit-card", "add"]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("dc_")


def test_debit_card_add_with_owner(capsys, monkeypatch, db_file, person):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "debit-card",
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
    assert captured.out.startswith("dc_")


def test_debit_card_add_with_bad_owner(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "debit-card",
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


def test_debit_card_connect(capsys, monkeypatch, db_file, temporary_db):
    test_debit_card = db.DebitCard(connection=temporary_db.connection)

    test_person = db.Person(connection=temporary_db.connection)

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "debit-card",
            "connect",
            str(test_debit_card.gID),
            str(test_person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.DebitCard.get(test_debit_card.id)
    assert db.Person.get(test_person.id)
    assert test_debit_card in test_person.debitCards

    test_organization = db.Organization(connection=temporary_db.connection)

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "debit-card",
            "connect",
            str(test_debit_card.gID),
            str(test_organization.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.DebitCard.get(test_debit_card.id)
    assert db.Organization.get(test_organization.id)
    assert test_debit_card in test_organization.debitCards


def test_debit_card_delete(capsys, monkeypatch, db_file, temporary_db):
    test_debit_card = db.DebitCard(connection=temporary_db.connection)
    assert (
        db.DebitCard.get(test_debit_card.id, connection=temporary_db.connection)
        is test_debit_card
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "debit-card",
            "delete",
            str(test_debit_card.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        db.DebitCard.get(test_debit_card.id, connection=temporary_db.connection)


def test_debit_card_disconnect(capsys, monkeypatch, db_file, temporary_db):
    test_debit_card = db.DebitCard(connection=temporary_db.connection)

    test_person = db.Person(connection=temporary_db.connection)
    test_person.addDebitCard(test_debit_card)

    assert test_debit_card in test_person.debitCards

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "debit-card",
            "disconnect",
            str(test_debit_card.gID),
            str(test_person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.DebitCard.get(test_debit_card.id)
    assert db.Person.get(test_person.id)
    assert test_debit_card not in test_person.debitCards

    test_organization = db.Organization(connection=temporary_db.connection)
    test_organization.addDebitCard(test_debit_card)

    assert test_debit_card in test_organization.debitCards

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "debit-card",
            "disconnect",
            str(test_debit_card.gID),
            str(test_organization.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.DebitCard.get(test_debit_card.id)
    assert db.Organization.get(test_organization.id)
    assert test_debit_card not in test_organization.debitCards


def test_debit_card_list(capsys, monkeypatch, db_file, temporary_db, tmp_path_factory):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_address_listes.sqlite")
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", "--create", "--db-file-path", empty_db_file, "debit-card", "list"],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    db.DebitCard(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--db-file-path", db_file, "debit-card", "list"]
    )
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("dc_")
    assert captured.out.count("dc_") >= 1


def test_debit_card_view(capsys, monkeypatch, db_file, temporary_db):
    debit_card = db.DebitCard(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", "--db-file-path", db_file, "debit-card", "view", str(debit_card.gID)],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("dc_")
