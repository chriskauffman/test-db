from types import SimpleNamespace
from unittest.mock import Mock

from pydantic import SecretStr
from typer.testing import CliRunner

from test_db import tdb


def test_callback_closes_database_controller(monkeypatch, tmp_path):
    database = Mock()
    settings = SimpleNamespace(
        db_connection_uri=SecretStr("sqlite:test.sqlite"),
        log_path=tmp_path,
        log_level_file="DEBUG",
        log_level_screen="ERROR",
    )
    monkeypatch.setattr(tdb, "Settings", Mock(return_value=settings))
    monkeypatch.setattr(tdb.test_db, "DatabaseController", Mock(return_value=database))
    ctx = Mock(invoked_subcommand="person")
    ctx.call_on_close.side_effect = lambda callback: callback()

    tdb.tdb_app_callback(ctx)

    database.close.assert_called_once_with()


def test_help_does_not_initialize_default_paths(monkeypatch):
    initialize = Mock()
    monkeypatch.setattr(tdb, "initialize_default_paths", initialize)

    result = CliRunner().invoke(tdb.app, ["--help"])

    assert result.exit_code == 0
    initialize.assert_not_called()


def test_version_does_not_initialize_default_paths(monkeypatch):
    initialize = Mock()
    monkeypatch.setattr(tdb, "initialize_default_paths", initialize)
    monkeypatch.setattr(tdb.test_db, "DatabaseController", Mock())

    result = CliRunner().invoke(tdb.app, ["version"])

    assert result.exit_code == 0
    initialize.assert_not_called()
