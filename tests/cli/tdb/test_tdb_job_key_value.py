import pytest
from sqlobject import SQLObjectNotFound
import uuid

import test_db
from test_db.tdb import app as tdb


@pytest.fixture(scope="module")
def job(temporary_db):
    return test_db.Job(connection=temporary_db.connection)

def test_entity_key_value_add(capsys, monkeypatch, job, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
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


def test_entity_key_value_add_bad_person(capsys, monkeypatch, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "job-key-value",
            "add",
            "test_01kah9p4b0ejfb7apkkr2abr7c",
            "secret",
            "value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "person or organization not found" in captured.err


def test_entity_key_value_add_duplicate(capsys, monkeypatch, person, temporary_db):
    test_key = str(uuid.uuid4())
    person.getKeyValueByKey(test_key, itemValue="test value")
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "job-key-value",
            "add",
            str(person.gID),
            test_key,
            "value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert captured.err


def test_entity_key_value_delete(capsys, monkeypatch, person, temporary_db):
    test_entity_key_value = test_db.JobKeyValue(
        connection=temporary_db.connection,
        itemKey="test_delete_entity_key_value",
        entity=person,
    )
    assert (
        test_db.JobKeyValue.get(
            test_entity_key_value.id, connection=temporary_db.connection
        )
        is test_entity_key_value
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "job-key-value",
            "delete",
            str(person.gID),
            test_entity_key_value.itemKey,
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
            test_entity_key_value.id, connection=temporary_db.connection
        )


def test_entity_key_value_list(capsys, monkeypatch, person, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "job-key-value",
            "list",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out


def test_entity_key_value_view(capsys, monkeypatch, person, temporary_db):
    test_key = str(uuid.uuid4())
    person.getKeyValueByKey(test_key, itemValue="test value")
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "job-key-value",
            "view",
            str(person.gID),
            test_key,
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert test_key in captured.out
