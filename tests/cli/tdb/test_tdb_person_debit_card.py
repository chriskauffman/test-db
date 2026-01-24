import pytest
from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb import app as tdb


def test_debit_card_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", "--db-connection-uri", temporary_db.connectionURI, "debit-card", "add"],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("dc_")


def test_debit_card_add_with_owner(capsys, monkeypatch, person, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
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


def test_debit_card_add_with_bad_owner(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
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


def test_debit_card_delete(capsys, monkeypatch, temporary_db):
    test_debit_card = test_db.PersonDebitCard(connection=temporary_db.connection)
    assert (
        test_db.PersonDebitCard.get(
            test_debit_card.id, connection=temporary_db.connection
        )
        is test_debit_card
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
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
        test_db.PersonDebitCard.get(
            test_debit_card.id, connection=temporary_db.connection
        )


def test_debit_card_list(capsys, monkeypatch, temporary_db, tmp_path_factory):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_address_listes.sqlite")
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            f"sqlite:{empty_db_file}",
            "debit-card",
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

    test_db.PersonDebitCard(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "debit-card",
            "list",
        ],
    )
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("dc_")
    assert captured.out.count("dc_") >= 1


def test_debit_card_view(capsys, monkeypatch, temporary_db):
    debit_card = test_db.PersonDebitCard(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "debit-card",
            "view",
            str(debit_card.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("dc_")
