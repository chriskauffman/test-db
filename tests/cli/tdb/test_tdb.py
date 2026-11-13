from types import SimpleNamespace
from unittest.mock import Mock

import pytest
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
    initialize_default_paths = Mock()
    monkeypatch.setattr(tdb, "initialize_default_paths", initialize_default_paths)
    monkeypatch.setattr(tdb.test_db, "DatabaseController", Mock(return_value=database))
    ctx = Mock(invoked_subcommand="person")
    ctx.call_on_close.side_effect = lambda callback: callback()

    tdb.tdb_app_callback(ctx)

    database.close.assert_called_once_with()
    initialize_default_paths.assert_not_called()


def test_callback_uses_screen_logging_when_log_file_is_unwritable(
    monkeypatch, tmp_path
):
    database = Mock()
    settings = SimpleNamespace(
        db_connection_uri=SecretStr("sqlite:test.sqlite"),
        log_path=tmp_path,
        log_level_file="DEBUG",
        log_level_screen="ERROR",
    )
    monkeypatch.setattr(tdb, "Settings", Mock(return_value=settings))
    monkeypatch.setattr(tdb, "initialize_default_paths", Mock())
    monkeypatch.setattr(
        tdb.logging.handlers,
        "RotatingFileHandler",
        Mock(side_effect=PermissionError("read-only log directory")),
    )
    monkeypatch.setattr(tdb.test_db, "DatabaseController", Mock(return_value=database))
    ctx = Mock(invoked_subcommand="person")
    ctx.call_on_close.side_effect = lambda callback: callback()

    tdb.tdb_app_callback(ctx)

    database.close.assert_called_once_with()


def test_upgrade_requires_confirmation(monkeypatch, tmp_path):
    settings = SimpleNamespace(
        db_connection_uri=SecretStr("sqlite:test.sqlite"),
        log_path=tmp_path,
        log_level_file="DEBUG",
        log_level_screen="ERROR",
    )
    database_controller = Mock(side_effect=ValueError("test_db file needs upgrade"))
    monkeypatch.setattr(tdb, "initialize_default_paths", Mock())
    monkeypatch.setattr(tdb, "Settings", Mock(return_value=settings))
    monkeypatch.setattr(tdb.test_db, "DatabaseController", database_controller)
    monkeypatch.setattr(tdb.typer, "confirm", Mock(return_value=False))

    with pytest.raises(tdb.typer.Abort):
        tdb.tdb_app_callback(Mock(invoked_subcommand="person"), upgrade=True)

    database_controller.assert_called_once_with(
        SecretStr("sqlite:test.sqlite"), defaultConnection=True, upgrade=False
    )


def test_upgrade_passes_after_confirmation(monkeypatch, tmp_path):
    settings = SimpleNamespace(
        db_connection_uri=SecretStr("sqlite:test.sqlite"),
        log_path=tmp_path,
        log_level_file="DEBUG",
        log_level_screen="ERROR",
    )
    database = Mock()
    database_controller = Mock(
        side_effect=[ValueError("test_db file needs upgrade"), database]
    )
    monkeypatch.setattr(tdb, "initialize_default_paths", Mock())
    monkeypatch.setattr(tdb, "Settings", Mock(return_value=settings))
    monkeypatch.setattr(tdb.test_db, "DatabaseController", database_controller)
    monkeypatch.setattr(tdb.typer, "confirm", Mock(return_value=True))
    ctx = Mock(invoked_subcommand="person")

    tdb.tdb_app_callback(ctx, upgrade=True)

    assert database_controller.call_args_list == [
        (
            (SecretStr("sqlite:test.sqlite"),),
            {"defaultConnection": True, "upgrade": False},
        ),
        (
            (SecretStr("sqlite:test.sqlite"),),
            {"defaultConnection": True, "upgrade": True},
        ),
    ]


def test_upgrade_skips_confirmation_for_current_database(monkeypatch, tmp_path):
    settings = SimpleNamespace(
        db_connection_uri=SecretStr("sqlite:test.sqlite"),
        log_path=tmp_path,
        log_level_file="DEBUG",
        log_level_screen="ERROR",
    )
    database = Mock()
    database_controller = Mock(return_value=database)
    confirm = Mock()
    monkeypatch.setattr(tdb, "initialize_default_paths", Mock())
    monkeypatch.setattr(tdb, "Settings", Mock(return_value=settings))
    monkeypatch.setattr(tdb.test_db, "DatabaseController", database_controller)
    monkeypatch.setattr(tdb.typer, "confirm", confirm)

    tdb.tdb_app_callback(Mock(invoked_subcommand="person"), upgrade=True)

    confirm.assert_not_called()
    database_controller.assert_called_once_with(
        SecretStr("sqlite:test.sqlite"), defaultConnection=True, upgrade=False
    )


def test_database_error_is_reported_without_traceback(monkeypatch, tmp_path):
    settings = SimpleNamespace(
        db_connection_uri=SecretStr("sqlite:test.sqlite"),
        log_path=tmp_path,
        log_level_file="DEBUG",
        log_level_screen="ERROR",
    )
    monkeypatch.setattr(tdb, "initialize_default_paths", Mock())
    monkeypatch.setattr(tdb, "Settings", Mock(return_value=settings))
    monkeypatch.setattr(
        tdb.test_db,
        "DatabaseController",
        Mock(side_effect=ValueError("not a test_db file")),
    )

    with pytest.raises(tdb.typer.BadParameter) as exc_info:
        tdb.tdb_app_callback(Mock(invoked_subcommand="person"))

    assert str(exc_info.value) == "not a test_db file"


def test_unexpected_database_error_is_not_relabelled(monkeypatch, tmp_path):
    settings = SimpleNamespace(
        db_connection_uri=SecretStr("sqlite:test.sqlite"),
        log_path=tmp_path,
        log_level_file="DEBUG",
        log_level_screen="ERROR",
    )
    monkeypatch.setattr(tdb, "initialize_default_paths", Mock())
    monkeypatch.setattr(tdb, "Settings", Mock(return_value=settings))
    monkeypatch.setattr(
        tdb.test_db,
        "DatabaseController",
        Mock(side_effect=RuntimeError("programming error")),
    )

    with pytest.raises(RuntimeError, match="programming error"):
        tdb.tdb_app_callback(Mock(invoked_subcommand="person"))


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
