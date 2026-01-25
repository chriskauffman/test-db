import test_db
from test_db.tdb_console import main as tdb


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
    assert bank_account.visualID in captured.out
