import pytest

from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb_console import main as tdb


def test_job_key_value_add(capsys, monkeypatch, temporary_db):
    job = test_db.Job(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "set command_interaction false",
            f"tdb_job_key_value_add {job.gID} test_job_key_value_add test_job_key_value_add_value",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.err


def test_job_key_value_delete(capsys, monkeypatch, temporary_db):
    job = test_db.Job(connection=temporary_db.connection)
    job_key_value = test_db.JobKeyValue(
        connection=temporary_db.connection,
        job=job,
        itemKey="test_job_key_value_delete",
        itemValue="test_job_key_value_delete_value",
    )
    assert (
        test_db.JobKeyValue.get(job_key_value.id, connection=temporary_db.connection)
        is job_key_value
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_job_key_value_delete {job.gID} {job_key_value.itemKey}",
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
        test_db.JobKeyValue.get(job_key_value.id, connection=temporary_db.connection)


def test_job_key_value_list(capsys, monkeypatch, temporary_db):
    job = test_db.Job(connection=temporary_db.connection)
    job_key_value = test_db.JobKeyValue(
        connection=temporary_db.connection,
        job=job,
        itemKey="test_job_key_value_list",
        itemValue="test_job_key_value_list_value",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_job_key_value_list {job.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert job_key_value.itemKey in captured.out


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
