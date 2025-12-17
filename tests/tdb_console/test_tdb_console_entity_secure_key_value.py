import test_db
from test_db.tdb_console import main as tdb


def test_entity_secure_key_value_view(capsys, monkeypatch, temporary_db):
    person = test_db.Person(connection=temporary_db.connection)
    personal_key_value = test_db.EntitySecureKeyValue(
        connection=temporary_db.connection, entity=person, key="secret", value="test"
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_file_path {temporary_db.filePath}",
            f"tdb_entity_secure_key_value_view {person.gID} {personal_key_value.key}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "secret = test" in captured.out
