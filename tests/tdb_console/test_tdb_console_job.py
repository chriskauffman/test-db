import test_db as db
from test_db.tdb_console import main as tdb


def test_job_view(capsys, monkeypatch, db_file, temporary_db):
    job = db.Job(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_file_path {db_file}",
            f"tdb_job_view {job.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert f"\nJob ID: {db.Job._gIDPrefix}" in captured.out
