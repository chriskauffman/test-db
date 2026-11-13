import sys
from types import SimpleNamespace
from typing import cast
from unittest.mock import Mock

import pytest
from pydantic import SecretStr

from test_db import tdb_console


def test_tdb_alias_enables_legacy_command_names():
    console = SimpleNamespace(
        aliases={},
        get_all_commands=lambda: ["job_list", "version"],
        find_commandset_for_command=lambda command: command == "job_list",
        poutput=Mock(),
    )

    tdb_console.Console.do_tdb_alias(cast(tdb_console.Console, console), None)

    assert console.aliases == {"tdb_job_list": "job_list"}
    console.poutput.assert_called_once_with("Legacy tdb_* aliases enabled")


def test_version_command_does_not_initialize_default_paths(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["tdb-console", "version", "quit"])
    initialize = Mock()
    monkeypatch.setattr(tdb_console, "initialize_default_paths", initialize)

    tdb_console.main()

    assert capsys.readouterr().out.strip()
    initialize.assert_not_called()


def test_configured_database_uses_screen_logging_when_log_file_is_unwritable(
    monkeypatch, tmp_path
):
    settings = Mock(
        db_connection_uri=SecretStr("sqlite:test.sqlite"),
        log_path=tmp_path,
        log_level_file="DEBUG",
        log_level_screen="ERROR",
    )
    console = Mock()
    console.cmdloop.return_value = 0
    monkeypatch.setattr(tdb_console, "Settings", Mock(return_value=settings))
    monkeypatch.setattr(
        tdb_console.logging.handlers,
        "RotatingFileHandler",
        Mock(side_effect=PermissionError("read-only log directory")),
    )
    monkeypatch.setattr(tdb_console, "Console", Mock(return_value=console))
    monkeypatch.setattr(sys, "argv", ["tdb-console"])

    with pytest.raises(SystemExit, match="0"):
        tdb_console.main()

    console.cmdloop.assert_called_once_with()
