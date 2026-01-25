import test_db
from test_db.tdb_console import main as tdb


def test_person_secure_key_value_view(capsys, monkeypatch, temporary_db):
    person = test_db.Person(connection=temporary_db.connection)
    personal_key_value = test_db.PersonSecureKeyValue(
        connection=temporary_db.connection,
        person=person,
        itemKey="test_person_secure_key_value_view",
        itemValue="test_person_secure_key_value_view_value",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_person_secure_key_value_view {person.gID} {personal_key_value.itemKey}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "test_person_secure_key_value_view" in captured.out
    assert "test_person_secure_key_value_view_value" in captured.out


def test_person_secure_key_value_list(capsys, monkeypatch, temporary_db):
    person = test_db.Person(connection=temporary_db.connection)
    person_key_value = test_db.PersonSecureKeyValue(
        connection=temporary_db.connection,
        person=person,
        itemKey="test_person_secure_key_value_list",
        itemValue="test_person_secure_key_value_list_value",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_person_secure_key_value_list {person.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert person_key_value.itemKey in captured.out
