import test_db
from test_db.tdb_console import main as tdb


def test_job_key_value_view(capsys, monkeypatch, temporary_db):
    job = test_db.Job(connection=temporary_db.connection)
    job_key_value = test_db.JobKeyValue(
        connection=temporary_db.connection,
        job=job,
        itemKey="test_job_key_value_view",
        itemValue="testest_job_key_value_view_value",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_connection_uri {temporary_db.connectionURI}",
            f"tdb_job_key_value_view {job.gID} {job_key_value.itemKey}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "test_job_key_value_view" in captured.out
    assert "testest_job_key_value_view_value" in captured.out


def test_job_key_value_list(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_connection_uri {temporary_db.connectionURI}",
            "tdb_job_key_value_list",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out
