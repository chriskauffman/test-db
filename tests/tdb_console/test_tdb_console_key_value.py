import nanoid

import test_db
from test_db.tdb_console import main as tdb


def test_key_value_view(capsys, monkeypatch, temporary_db):
    key_value = test_db.KeyValue(
        connection=temporary_db.connection, key=nanoid.generate(), value="test"
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_connection_uri {temporary_db.connectionURI}",
            f"tdb_key_value_view {key_value.key}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert f"{key_value.key} = {key_value.value}" in captured.out
