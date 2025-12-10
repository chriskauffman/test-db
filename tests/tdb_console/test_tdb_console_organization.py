import test_db as db
from test_db.tdb_console import main as tdb


def test_organization_view(capsys, monkeypatch, db_file, temporary_db):
    organization = db.Organization(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_file_path {db_file}",
            f"tdb_organization_view {organization.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert f"\nOrganization ID: {db.Organization._gIDPrefix}" in captured.out
