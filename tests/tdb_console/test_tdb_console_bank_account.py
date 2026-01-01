import test_db
from test_db.tdb_console import main as tdb


def test_bank_account_view(capsys, monkeypatch, temporary_db):
    bank_account = test_db.BankAccount(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_connection_uri {temporary_db.connectionURI}",
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
