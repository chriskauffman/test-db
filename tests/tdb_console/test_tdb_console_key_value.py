import test_db
from test_db.tdb_console import main as tdb


def test_key_value_view(capsys, monkeypatch, db_file, temporary_db):
    key_value = test_db.KeyValue(
        connection=temporary_db.connection, key="key1", value="test"
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_file_path {db_file}",
            f"tdb_key_value_view {key_value.key}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "key1 = test" in captured.out
