import pytest

from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb_console import main as tdb


def test_job_add(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "set command_interaction false",
            "tdb_job_add",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert test_db.Job._gIDPrefix in captured.out


def test_job_delete(capsys, monkeypatch, temporary_db):
    job = test_db.Job(connection=temporary_db.connection)
    assert test_db.Job.get(job.id, connection=temporary_db.connection) is job

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_job_delete {job.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        test_db.Job.get(job.id, connection=temporary_db.connection)


def test_job_list(capsys, monkeypatch, temporary_db):
    job = test_db.Job(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "tdb_job_list",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert str(job.gID) in captured.out


def test_job_view(capsys, monkeypatch, temporary_db):
    job = test_db.Job(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_job_view {job.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert str(job.gID) in captured.out
