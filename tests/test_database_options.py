"""Tests for database connection options and secure connection string handling."""

import logging
import os
import subprocess
import sys

from pydantic import SecretStr

import test_db
from test_db._cli_settings import Settings, initialize_default_paths
from test_db._database_controller import DatabaseController
from test_db.tdb_console import Console


def test_importing_cli_settings_does_not_write_to_home(tmp_path):
    """Importing CLI settings must not create default user files."""
    env = os.environ | {"HOME": str(tmp_path)}
    subprocess.run(
        [sys.executable, "-c", "import test_db._cli_settings"],
        check=True,
        env=env,
    )

    assert not (tmp_path / ".test_db").exists()


def test_initialize_default_paths_creates_default_files(tmp_path, monkeypatch):
    """CLI startup creates the paths required by the default settings."""
    import test_db._cli_settings as cli_settings

    config_path = tmp_path / ".test_db"
    monkeypatch.setattr(cli_settings, "DEFAULT_CONFIG_PATH", config_path)
    monkeypatch.setattr(cli_settings, "DEFAULT_DB_PATH", config_path / "test_db.sqlite")
    monkeypatch.setattr(cli_settings, "DEFAULT_LOG_PATH", config_path / "log")
    monkeypatch.setattr(cli_settings, "DEFAULT_BACKUP_PATH", config_path / "backup")

    initialize_default_paths()

    assert (config_path / "test_db.sqlite").is_file()
    assert (config_path / "log").is_dir()
    assert (config_path / "backup").is_dir()
    assert (config_path / "test_db.toml").is_file()


def test_settings_db_connection_uri_secret_str():
    """Verify Settings stores db_connection_uri as SecretStr and masks secrets."""
    secret_uri = "postgresql://myuser:supersecretpassword@localhost:5432/testdb"
    settings = Settings(db_connection_uri=secret_uri)

    assert isinstance(settings.db_connection_uri, SecretStr)
    assert settings.db_connection_uri.get_secret_value() == secret_uri
    assert str(settings.db_connection_uri) == "**********"
    assert "supersecretpassword" not in str(settings)
    assert "supersecretpassword" not in repr(settings)


def test_settings_db_connection_uri_from_env(monkeypatch):
    """Verify Settings reads db_connection_uri from environment variable as SecretStr."""
    secret_uri = "mysql://myuser:hiddenpassword@localhost:3306/testdb"
    monkeypatch.setenv("DB_CONNECTION_URI", secret_uri)

    settings = Settings()
    assert isinstance(settings.db_connection_uri, SecretStr)
    assert settings.db_connection_uri.get_secret_value() == secret_uri
    assert "hiddenpassword" not in str(settings)


def test_database_controller_accepts_str_and_masks_uri(caplog):
    """Verify DatabaseController accepts str and stores as SecretStr without logging credentials."""
    with caplog.at_level(logging.DEBUG):
        db = DatabaseController(test_db.IN_MEMORY_DB_FILE)

    assert isinstance(db.connectionURI, SecretStr)
    assert str(db.connectionURI) == "**********"
    assert db.connectionURI.get_secret_value() == test_db.IN_MEMORY_DB_FILE
    assert (
        "connectionURI=**********" in caplog.text
        or "connectionURI=SecretStr('**********')" in caplog.text
    )


def test_database_controller_accepts_secret_str():
    """Verify DatabaseController accepts SecretStr directly."""
    secret_uri = SecretStr(test_db.IN_MEMORY_DB_FILE)
    db = DatabaseController(secret_uri)

    assert isinstance(db.connectionURI, SecretStr)
    assert db.connectionURI == secret_uri
    assert db.connectionURI.get_secret_value() == test_db.IN_MEMORY_DB_FILE
    assert db.validSchema


def test_database_controller_foreign_keys_enabled_for_sqlite():
    """Verify SQLite foreign keys PRAGMA is enabled when using SecretStr."""
    db = DatabaseController(SecretStr(test_db.IN_MEMORY_DB_FILE))
    fk_result = db._rawCursor.execute("PRAGMA foreign_keys").fetchone()[0]
    assert fk_result == 1


def test_console_db_connection_uri_settable():
    """Verify Console registers db_connection_uri as SecretStr Settable."""
    secret_uri = SecretStr(test_db.IN_MEMORY_DB_FILE)
    settings = Settings(db_connection_uri=secret_uri)
    console = Console(settings)

    assert isinstance(console.db_connection_uri, SecretStr)
    assert str(console.db_connection_uri) == "**********"
    assert console.db_connection_uri.get_secret_value() == test_db.IN_MEMORY_DB_FILE

    settable = console.settables.get("db_connection_uri")
    assert settable is not None
    assert settable.val_type is SecretStr
