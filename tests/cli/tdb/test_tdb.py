from unittest.mock import Mock

from typer.testing import CliRunner

from test_db import tdb


def test_callback_closes_database_controller(monkeypatch, tmp_path):
    database = Mock()
    monkeypatch.setattr(tdb.test_db, "DatabaseController", Mock(return_value=database))
    result = CliRunner().invoke(
        tdb.app,
        ["--db-connection-uri", "sqlite:test.sqlite", "version"],
        env={"LOG_PATH": str(tmp_path)},
    )

    assert result.exit_code == 0
    database.close.assert_called_once_with()
