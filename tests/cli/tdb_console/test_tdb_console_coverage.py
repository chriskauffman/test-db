"""Tests to improve coverage for console command sets."""

import uuid

import test_db
from test_db.tdb_console import main as tdb


def test_validate_job_not_found(capsys, monkeypatch, temporary_db):
    """Test validate_job with invalid GID."""
    invalid_gid = "invalid_gid_12345"
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_job_view {invalid_gid}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "error:" in captured.out or "error:" in captured.err
    assert "AttributeError" not in captured.out + captured.err


def test_validate_person_not_found(capsys, monkeypatch, temporary_db):
    """Test validate_person with invalid GID."""
    invalid_gid = "invalid_gid_12345"
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_person_view {invalid_gid}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "error:" in captured.out or "error:" in captured.err


def test_validate_organization_not_found(capsys, monkeypatch, temporary_db):
    """Test validate_organization with invalid GID."""
    invalid_gid = "invalid_gid_12345"
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_organization_view {invalid_gid}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "error:" in captured.out or "error:" in captured.err


def test_key_value_validate_not_found(capsys, monkeypatch, temporary_db):
    """Test validate_key with invalid key."""
    invalid_key = str(uuid.uuid4())
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_key_value_view {invalid_key}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "error:" in captured.out or "error:" in captured.err


def test_key_value_delete_restricted_key(capsys, monkeypatch, temporary_db):
    """Test deleting a restricted key."""
    restricted_key = next(iter(test_db.RESTRICTED_KEYS))
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_key_value_delete {restricted_key}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "restricted" in captured.out or "restricted" in captured.err


def test_key_value_edit_restricted_key(capsys, monkeypatch, temporary_db):
    """Test editing a restricted key."""
    restricted_key = next(iter(test_db.RESTRICTED_KEYS))
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "set command_interaction false",
            f"tdb_key_value_edit {restricted_key}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "restricted" in captured.out or "restricted" in captured.err


def test_key_value_add_duplicate(capsys, monkeypatch, temporary_db):
    """Test adding a duplicate key."""
    key = str(uuid.uuid4())
    test_db.KeyValue(connection=temporary_db.connection, key=key, value="test")

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "set command_interaction false",
            f"tdb_key_value_add {key} duplicate_value",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "error:" in captured.out or "error:" in captured.err


def test_key_value_list(capsys, monkeypatch, temporary_db):
    """Test listing all key-value pairs."""
    test_db.KeyValue(
        connection=temporary_db.connection, key="test_key_1", value="test_value_1"
    )
    test_db.KeyValue(
        connection=temporary_db.connection, key="test_key_2", value="test_value_2"
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "tdb_key_value_list",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "test_key_1" in captured.out
    assert "test_key_2" in captured.out
