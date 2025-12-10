import test_db as db
from test_db.tdb_console import main as tdb


def test_debit_card_view(capsys, monkeypatch, db_file, temporary_db):
    debit_card = db.DebitCard(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_file_path {db_file}",
            f"tdb_debit_card_view {debit_card.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert debit_card.visualID in captured.out
