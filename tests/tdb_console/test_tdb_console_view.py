import test_db as db
from test_db.tdb_console import main as tdb


def test_view_address(capsys, monkeypatch, db_file, temporary_db):
    address = db.Address(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_file_path {db_file}",
            f"tdb_view_address {address.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "\nAddress ID: addr_" in captured.out
