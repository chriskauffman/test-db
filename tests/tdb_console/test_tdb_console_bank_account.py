import test_db as db
from test_db.tdb_console import main as tdb


def test_bank_account_view(capsys, monkeypatch, db_file, temporary_db):
    bank_account = db.BankAccount(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_file_path {db_file}",
            f"tdb_bank_account_view {bank_account.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert bank_account.visualID in captured.out
