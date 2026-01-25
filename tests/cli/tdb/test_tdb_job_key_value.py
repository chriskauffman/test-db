import pytest
from sqlobject import SQLObjectNotFound
import uuid

import test_db
from test_db.tdb import app as tdb


@pytest.fixture(scope="module")
def job(temporary_db):
    return test_db.Job(connection=temporary_db.connection)


def test_job_key_value_add(capsys, monkeypatch, job, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "job-key-value",
            "add",
            str(job.gID),
            "secret",
            "value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out


def test_job_key_value_delete(capsys, monkeypatch, job, temporary_db):
    test_job_key_value = test_db.JobKeyValue(
        connection=temporary_db.connection,
        itemKey="test_delete_job_key_value",
        job=job,
    )
    assert (
        test_db.JobKeyValue.get(
            test_job_key_value.id, connection=temporary_db.connection
        )
        is test_job_key_value
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "job-key-value",
            "delete",
            str(job.gID),
            test_job_key_value.itemKey,
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        test_db.JobKeyValue.get(
            test_job_key_value.id, connection=temporary_db.connection
        )


def test_job_key_value_list(capsys, monkeypatch, job, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "job-key-value",
            "list",
            str(job.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out


def test_job_key_value_view(capsys, monkeypatch, job, temporary_db):
    test_key = str(uuid.uuid4())
    job.getKeyValueByKey(test_key, itemValue="test value")
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "job-key-value",
            "view",
            str(job.gID),
            test_key,
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert test_key in captured.out
