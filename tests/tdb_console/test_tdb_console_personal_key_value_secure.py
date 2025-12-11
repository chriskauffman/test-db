import test_db
from test_db.tdb_console import main as tdb


def test_personal_key_value_secure_view(capsys, monkeypatch, temporary_db):
    person = test_db.Person(connection=temporary_db.connection)
    personal_key_value = test_db.PersonalKeyValueSecure(
        connection=temporary_db.connection, person=person, key="secret", value="test"
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_file_path {temporary_db.filePath}",
            f"tdb_personal_key_value_secure_view {person.gID} {personal_key_value.key}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "secret = test" in captured.out
