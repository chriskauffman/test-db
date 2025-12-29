import pytest
from sqlobject import SQLObjectNotFound

import test_db
from test_db.tdb import app as tdb


def test_job_add(capsys, monkeypatch, person, organization, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "job",
            "add",
            "--organization-gid",
            str(organization.gID),
            "--person-gid",
            str(person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("j_")


def test_job_add_bad_org(capsys, monkeypatch, person, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "job",
            "add",
            "--organization-gid",
            "test_01kah9p4b0ejfb7apkkr2abr7c",
            "--person-gid",
            str(person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "does not exist" in captured.err


def test_job_add_bad_person(capsys, monkeypatch, organization, temporary_db):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "job",
            "add",
            "--organization-gid",
            str(organization.gID),
            "--person-gid",
            "test_01kah9p4b0ejfb7apkkr2abr7c",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "does not exist" in captured.err


def test_job_delete(capsys, monkeypatch, person, organization, temporary_db):
    test_job = test_db.Job(connection=temporary_db.connection)
    assert test_db.Job.get(test_job.id, connection=temporary_db.connection) is test_job

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "job",
            "delete",
            str(test_job.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        test_db.Job.get(test_job.id, connection=temporary_db.connection)


def test_job_list(
    capsys,
    monkeypatch,
    temporary_db,
    tmp_path_factory,
    organization,
    person,
):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_address_listes.sqlite")
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            f"sqlite:{empty_db_file}",
            "job",
            "list",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    test_db.Job(
        connection=temporary_db.connection,
        organization=organization,
        person=person,
    )
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", "--db-connection-uri", temporary_db.connectionURI, "job", "list"],
    )
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("j_")
    assert captured.out.count("j_") >= 1


def test_job_view(capsys, monkeypatch, temporary_db, organization, person):
    job = test_db.Job(
        organization=organization,
        person=person,
        connection=temporary_db.connection,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-connection-uri",
            temporary_db.connectionURI,
            "job",
            "view",
            str(job.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("\nJob ID: j_")
