import test_db
from test_db.tdb_console import main as tdb


def test_job_view(capsys, monkeypatch, temporary_db):
    job = test_db.Job(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_file_path {temporary_db.filePath}",
            f"tdb_job_view {job.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert f"\nJob ID: {test_db.Job._gIDPrefix}" in captured.out
