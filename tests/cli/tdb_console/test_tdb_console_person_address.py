import test_db
from test_db.tdb_console import main as tdb


def test_address_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "set command_interaction false",
            "tdb_person_address_add",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert test_db.PersonAddress._gIDPrefix in captured.out

def test_address_list(capsys, monkeypatch, temporary_db, person):
    address = test_db.PersonAddress(person=person, connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "tdb_person_address_list",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert str(address.gID) in captured.out

def test_address_view(capsys, monkeypatch, temporary_db, person):
    address = test_db.PersonAddress(person=person, connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_person_address_view {address.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert str(address.gID) in captured.out
