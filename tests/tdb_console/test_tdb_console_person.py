import test_db as db
from test_db.tdb_console import main as tdb


def test_person_view(capsys, monkeypatch, db_file, temporary_db):
    person = db.Person(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_file_path {db_file}",
            f"tdb_person_view {person.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert f"\nPerson ID: {db.Person._gIDPrefix}" in captured.out
