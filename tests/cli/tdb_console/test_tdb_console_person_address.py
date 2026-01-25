import test_db
from test_db.tdb_console import main as tdb


def test_address_view(capsys, monkeypatch, temporary_db, person):
    address = test_db.PersonAddress(person=person, connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_connection_uri {temporary_db.connectionURI}",
            f"tdb_person_address_view {address.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert f"\nAddress ID: {test_db.PersonAddress._gIDPrefix}" in captured.out
