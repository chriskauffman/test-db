import logging
import os
import pathlib

import sqlobject  # type: ignore
from typing_extensions import Union

from test_db._address import PersonalAddress
from test_db._app_settings import AppSettings
from test_db._app_settings import PersonalAppSettings
from test_db._bank_account import PersonalBankAccount
from test_db._debit_card import PersonalDebitCard
from test_db._employer import Employer
from test_db._job import Job
from test_db._listeners import update_listener
from test_db._oauth2_token import PersonalOAuth2Token
from test_db._person import Person
from test_db._settings import Settings

IN_MEMORY_DB_FILE = "/:memory:"

TABLES = (
    AppSettings,
    Employer,
    Job,
    Person,
    PersonalAddress,
    PersonalAppSettings,
    PersonalBankAccount,
    PersonalDebitCard,
    PersonalOAuth2Token,
    Settings,
)

APPLICATION_ID = 990001
BACKUP_PATH = "backups"
CURRENT_APPLICATION_SCHEMA_VERSION = 1

logger = logging.getLogger(__name__)


class _GlobalDatabaseOptions:
    pass


class DatabaseController:
    """DatabaseController

    Basic class to handle the connection, configuration and upgrade of a test_db
    Connect SQLite Database for SQLObject Access

    Args:
        file_path (Union[pathlib.Path, str]): path to sqlite file
        create (bool, optional): creates the database file when True
        default_connection (bool, optional): sets DB as default sqlobject connection
        upgrade (bool, optional): upgrade the database if it is out of date

    Raises:
        ValueError: invalid database

    Instance Attributes:
        application_id (int): database application ID unique to test_db
        application_schema_version (int): test_db schema version number
        connection (sqlobject.connectionForURI)
        db_schema_version (int): database schema version
        file_path (pathlib.Path): location of DB file
        valid_schema (bool): True if schema passes checks
    """

    _global_database_options = _GlobalDatabaseOptions()

    def __init__(
        self,
        file_path: Union[pathlib.Path, str],
        create: bool = False,
        default_connection: bool = False,
        upgrade: bool = False,
    ) -> None:
        self.file_path = pathlib.Path(os.path.abspath(file_path))

        # In-memory DB can be opened with 'sqlite:/:memory:'
        if not self.file_path.is_file() and not create:
            raise ValueError(f"DB file {self.file_path} does not exist")

        self.connection = sqlobject.connectionForURI(f"sqlite:{self.file_path}")
        self._raw = self.connection.getConnection()
        self._raw_cursor = self._raw.cursor()

        logger.debug("sqlite3_application_id=%s", self.application_id)
        logger.debug("sqlite3_schema_version=%s", self.db_schema_version)
        logger.debug("sqlite3_user_version=%s", self.application_schema_version)

        if self._is_test_db:
            if self.valid_schema:
                pass
            else:
                if upgrade:
                    self._upgrade()
                else:
                    raise ValueError("test_db file needs upgrade")
        elif self._is_empty_db:
            self._new()
        else:
            logger.error("not a test_db file")
            raise ValueError("not a test_db file")

        self._raw_cursor.execute("PRAGMA foreign_keys = ON")

        for table in TABLES:
            sqlobject.events.listen(
                update_listener, table, sqlobject.events.RowUpdateSignal
            )

        if default_connection:
            sqlobject.sqlhub.processConnection = self.connection

    @property
    def application_id(self) -> int:
        """Property application_id"""
        return int(self._raw_cursor.execute("PRAGMA application_id").fetchone()[0])

    @application_id.setter
    def application_id(self, application_id: int) -> None:
        """Property application_id setter"""
        self._raw_cursor.execute(f"PRAGMA application_id = {application_id}")

    @property
    def application_schema_version(self) -> int:
        """Property application_schema_version"""
        return int(self._raw_cursor.execute("PRAGMA user_version").fetchone()[0])

    @application_schema_version.setter
    def application_schema_version(self, application_schema_version: int) -> None:
        """Property application_schema_version setter"""
        self._raw_cursor.execute(f"PRAGMA user_version = {application_schema_version}")

    @property
    def db_schema_version(self) -> int:
        """Property db_schema_version"""
        return int(self._raw_cursor.execute("PRAGMA schema_version").fetchone()[0])

    @property
    def _is_empty_db(self) -> bool:
        return (
            self.application_id == 0
            and self.db_schema_version == 0
            and self.application_schema_version == 0
        )

    @property
    def _is_test_db(self) -> bool:
        if self.application_id == APPLICATION_ID:
            return True
        return False

    @property
    def valid_schema(self) -> bool:
        """Validate current schema"""
        if not self._is_test_db:
            logger.debug("DB does not appear to be any version of a TestDB")
            return False
        if not self._schema_version(CURRENT_APPLICATION_SCHEMA_VERSION):
            logger.debug(
                "DB invalid: app ID %s, db schema version %s, app schema version %s",
                self.application_id,
                self.db_schema_version,
                self.application_schema_version,
            )
            return False
        for table in TABLES:
            if not self._table_exists(table.sqlmeta.table):
                logger.debug("Table %s missing", table)
                return False
        return True

    def _column_exists(self, table_name: str, column_name: str) -> bool:
        """Determine if table exists in DB

        Args:
            table_name (str): name of the table
            column_name (str): name of the column

        Returns:
            bool: True if column exists
        """
        return column_name in (
            x[1]
            for x in self._raw_cursor.execute(
                f"PRAGMA table_info('{table_name}')"
            ).fetchall()
        )

    def _index_exists(self, index_name: str) -> bool:
        """Determine if an index exists in DB

        Args:
            index_name (str): name of the index

        Returns:
            bool: True if index exists
        """
        return (
            len(
                self._raw_cursor.execute(
                    f"PRAGMA index_list('{index_name}')"
                ).fetchall()
            )
            > 0
        )

    def _table_exists(self, table_name: str) -> bool:
        """Determine if table exists in DB

        Args:
            table_name (str): name of the table

        Returns:
            bool: True if table exists
        """
        return (
            len(
                self._raw_cursor.execute(
                    f"PRAGMA table_list('{table_name}')"
                ).fetchall()
            )
            > 0
        )

    def _new(self):
        """Setup new database"""
        logger.debug("DatabaseController: New file, creating complete schema")
        for table in TABLES:
            table.createTable(connection=self.connection)

        self.application_id = APPLICATION_ID
        self.application_schema_version = CURRENT_APPLICATION_SCHEMA_VERSION

    def _schema_version(self, version: int) -> bool:
        return (
            self.application_id == APPLICATION_ID
            and self.db_schema_version > 0
            and self.application_schema_version == version
        )

    def _upgrade(self):
        """Upgrade existing database

        Attempts to upgrade database based on expected values of SQLite's
        application_id, db_schema_version and user_version. application_id and
        user_version are set by this class. db_schema_version is automatically
        incremented by SQLite.

        Raises:
            ValueError:
        """
        logger.debug("DatabaseController: Upgrading if possible")

        # self._upgrade_to_schema_2()

        if not self.valid_schema:
            # upgrade has failed for some reason
            logger.error("unable to upgrade")
            raise ValueError("unable to upgrade")

        logger.debug("DatabaseController: Upgrade successful")

    def close(self):
        """Close the database"""
        if sqlobject.sqlhub.processConnection == self.connection:
            sqlobject.sqlhub.processConnection = None
        self.connection.close()
