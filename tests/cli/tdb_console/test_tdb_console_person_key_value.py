import test_db
from test_db.tdb_console import main as tdb


def test_person_key_value_view(capsys, monkeypatch, temporary_db):
    person = test_db.Person(connection=temporary_db.connection)
    personal_key_value = test_db.PersonKeyValue(
        connection=temporary_db.connection,
        person=person,
        itemKey="test_person_key_value_view",
        itemValue="test_person_key_value_view_value",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_connection_uri {temporary_db.connectionURI}",
            f"tdb_person_key_value_view {person.gID} {personal_key_value.itemKey}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "test_person_key_value_view" in captured.out
    assert "test_person_key_value_view_value" in captured.out


def test_person_key_value_list(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_connection_uri {temporary_db.connectionURI}",
            "tdb_person_key_value_list",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out
