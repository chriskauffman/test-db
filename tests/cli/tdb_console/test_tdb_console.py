import sys
from unittest.mock import Mock

from test_db import tdb_console


def test_version_command_does_not_initialize_default_paths(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["tdb-console", "version", "quit"])
    initialize = Mock()
    monkeypatch.setattr(tdb_console, "initialize_default_paths", initialize)

    tdb_console.main()

    assert capsys.readouterr().out.strip()
    initialize.assert_not_called()
