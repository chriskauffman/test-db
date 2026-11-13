from types import SimpleNamespace
from unittest.mock import Mock
from urllib.parse import parse_qsl, urlsplit

from sqlobject.dbconnection import TheURIOpener

from test_db._connection import (
    _MySQLConfigConnection,
    _with_mysql_defaults,
    connectionForURI,
)
from test_db._database_controller import DatabaseController


def test_mysql_uri_loads_local_client_config(monkeypatch, tmp_path):
    config_file = tmp_path / ".my.cnf"
    config_file.write_text("[client]\nuser=test_db\npassword=secret\n")
    monkeypatch.setenv("HOME", str(tmp_path))

    adapted_uri = _with_mysql_defaults("mysql://test_db@nas02/test_db")
    options = dict(parse_qsl(urlsplit(adapted_uri).query))

    assert options == {
        "read_default_file": str(config_file),
    }


def test_connection_for_uri_passes_adapted_mysql_uri(monkeypatch, tmp_path):
    config_file = tmp_path / ".my.cnf"
    config_file.write_text("[client]\npassword=secret\n")
    monkeypatch.setenv("HOME", str(tmp_path))
    connection = SimpleNamespace(dbName="mysql", password="")
    monkeypatch.setattr(
        _MySQLConfigConnection,
        "connectionFromURI",
        classmethod(lambda cls, uri: connection),
    )

    uri = "mysql://test_db@nas02/test_db"
    adapted_uri = _with_mysql_defaults(uri)

    assert connectionForURI(uri) is connection
    assert TheURIOpener.cachedURIs[uri] is connection
    assert TheURIOpener.cachedURIs[adapted_uri] is connection


def test_mysql_uri_preserves_explicit_options(monkeypatch, tmp_path):
    config_file = tmp_path / ".my.cnf"
    config_file.write_text("[client]\npassword=secret\n")
    monkeypatch.setenv("HOME", str(tmp_path))

    uri = "mysql://test_db@nas02/test_db?read_default_file=/custom.cnf"

    assert _with_mysql_defaults(uri) == uri


def test_with_mysql_defaults_leaves_other_uris_unchanged(monkeypatch, tmp_path):
    (tmp_path / ".my.cnf").write_text("[client]\npassword=secret\n")
    monkeypatch.setenv("HOME", str(tmp_path))

    assert _with_mysql_defaults("postgresql://test_db@nas02/test_db") == (
        "postgresql://test_db@nas02/test_db"
    )
    assert _with_mysql_defaults("mysql://test_db:secret@nas02/test_db") == (
        "mysql://test_db:secret@nas02/test_db"
    )


def test_failed_initialization_removes_mysql_cache_aliases():
    connection = Mock()
    uri = "mysql://test_db@nas02/test_db"
    adapted_uri = f"{uri}?read_default_file=%2Ftmp%2Fmy.cnf"
    opener = TheURIOpener
    opener.cachedURIs[uri] = connection
    opener.cachedURIs[adapted_uri] = connection

    database = object.__new__(DatabaseController)
    database._connection_was_cached = False
    database._connection_uri = uri
    database.connection = connection

    database._cleanup_failed_initialization()

    assert uri not in opener.cachedURIs
    assert adapted_uri not in opener.cachedURIs
    connection.close.assert_called_once_with()
