from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import sqlobject
from sqlobject.dbconnection import TheURIOpener
from sqlobject.mysql.mysqlconnection import MySQLConnection


class _MySQLConfigConnection(MySQLConnection):
    def makeConnection(self):
        if self.password or self.driver not in ("mysqldb", "pymysql"):
            return super().makeConnection()

        module = self.module

        class Module:
            OperationalError = module.OperationalError

            @staticmethod
            def connect(**kwargs):
                kwargs.pop("passwd", None)
                return module.connect(**kwargs)

        self.module = Module
        try:
            return super().makeConnection()
        finally:
            self.module = module


def connectionForURI(uri: str):
    """Open a SQLObject connection, loading the local MySQL client config."""
    adapted_uri = _with_mysql_defaults(uri)
    parsed = urlsplit(adapted_uri)
    uses_config = (
        parsed.scheme == "mysql"
        and not parsed.password
        and any(name == "read_default_file" for name, _ in parse_qsl(parsed.query))
    )
    if uses_config:
        if adapted_uri in TheURIOpener.cachedURIs:
            connection = TheURIOpener.cachedURIs[adapted_uri]
            TheURIOpener.cachedURIs[uri] = connection
            return connection
        connection = _MySQLConfigConnection.connectionFromURI(adapted_uri)
        TheURIOpener.cachedURIs[adapted_uri] = connection
        TheURIOpener.cachedURIs[uri] = connection
        return connection
    return sqlobject.connectionForURI(adapted_uri)


def _with_mysql_defaults(uri: str) -> str:
    parsed = urlsplit(uri)
    if parsed.scheme != "mysql" or parsed.password:
        return uri

    config_file = Path.home() / ".my.cnf"
    if not config_file.is_file():
        return uri

    query = parse_qsl(parsed.query, keep_blank_values=True)
    query_names = {name for name, _ in query}
    if "read_default_file" in query_names:
        return uri
    query.append(("read_default_file", str(config_file)))
    return urlunsplit(parsed._replace(query=urlencode(query)))
