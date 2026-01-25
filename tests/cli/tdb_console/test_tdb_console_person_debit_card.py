import test_db
from test_db.tdb_console import main as tdb


def test_debit_card_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "set command_interaction false",
            "tdb_person_debit_card_add",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert test_db.PersonDebitCard._gIDPrefix in captured.out


def test_debit_card_list(capsys, monkeypatch, temporary_db, person):
    debit_card = test_db.PersonDebitCard(
        person=person, connection=temporary_db.connection
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "tdb_person_debit_card_list",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert str(debit_card.gID) in captured.out


def test_debit_card_view(capsys, monkeypatch, temporary_db, person):
    debit_card = test_db.PersonDebitCard(
        person=person, connection=temporary_db.connection
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_person_debit_card_view {debit_card.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert str(debit_card.gID) in captured.out
