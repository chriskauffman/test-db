import test_db
from test_db.tdb_console import main as tdb


def test_debit_card_view(capsys, monkeypatch, temporary_db, person):
    debit_card = test_db.PersonDebitCard(
        person=person, connection=temporary_db.connection
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_connection_uri {temporary_db.connectionURI}",
            f"tdb_person_debit_card_view {debit_card.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert debit_card.visualID in captured.out
