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
from test_db._listeners import updateListener
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
        filePath (Union[pathlib.Path, str]): path to sqlite file
        create (bool, optional): creates the database file when True
        defaultConnection (bool, optional): sets DB as default sqlobject connection
        upgrade (bool, optional): upgrade the database if it is out of date

    Raises:
        ValueError: invalid database

    Instance Attributes:
        applicationID (int): database application ID unique to test_db
        applicationSchemaVersion (int): test_db schema version number
        connection (sqlobject.connectionForURI)
        dbSchemaVersion (int): database schema version
        filePath (pathlib.Path): location of DB file
        validSchema (bool): True if schema passes checks
    """

    _globalDatabaseOptions = _GlobalDatabaseOptions()

    def __init__(
        self,
        filePath: Union[pathlib.Path, str],
        create: bool = False,
        defaultConnection: bool = False,
        upgrade: bool = False,
    ) -> None:
        self.filePath = pathlib.Path(os.path.abspath(filePath))

        # In-memory DB can be opened with 'sqlite:/:memory:'
        if not self.filePath.is_file() and not create:
            raise ValueError(f"DB file {self.filePath} does not exist")

        self.connection = sqlobject.connectionForURI(f"sqlite:{self.filePath}")
        self._raw = self.connection.getConnection()
        self._rawCursor = self._raw.cursor()

        logger.debug("sqlite3_application_id=%s", self.applicationID)
        logger.debug("sqlite3_schema_version=%s", self.dbSchemaVersion)
        logger.debug("sqlite3_user_version=%s", self.applicationSchemaVersion)

        if self._isTestDB:
            if self.validSchema:
                pass
            else:
                if upgrade:
                    self._upgrade()
                else:
                    raise ValueError("test_db file needs upgrade")
        elif self._isEmptyDB:
            self._new()
        else:
            logger.error("not a test_db file")
            raise ValueError("not a test_db file")

        self._rawCursor.execute("PRAGMA foreign_keys = ON")

        for table in TABLES:
            sqlobject.events.listen(
                updateListener, table, sqlobject.events.RowUpdateSignal
            )

        if defaultConnection:
            sqlobject.sqlhub.processConnection = self.connection

    @property
    def applicationID(self) -> int:
        return int(self._rawCursor.execute("PRAGMA application_id").fetchone()[0])

    @applicationID.setter
    def applicationID(self, applicationID: int) -> None:
        self._rawCursor.execute(f"PRAGMA application_id = {applicationID}")

    @property
    def applicationSchemaVersion(self) -> int:
        return int(self._rawCursor.execute("PRAGMA user_version").fetchone()[0])

    @applicationSchemaVersion.setter
    def applicationSchemaVersion(self, applicationSchemaVersion: int) -> None:
        self._rawCursor.execute(f"PRAGMA user_version = {applicationSchemaVersion}")

    @property
    def dbSchemaVersion(self) -> int:
        return int(self._rawCursor.execute("PRAGMA schema_version").fetchone()[0])

    @property
    def _isEmptyDB(self) -> bool:
        return (
            self.applicationID == 0
            and self.dbSchemaVersion == 0
            and self.applicationSchemaVersion == 0
        )

    @property
    def _isTestDB(self) -> bool:
        if self.applicationID == APPLICATION_ID:
            return True
        return False

    @property
    def validSchema(self) -> bool:
        """Validate current schema"""
        if not self._isTestDB:
            logger.debug("DB does not appear to be any version of a TestDB")
            return False
        if not self._schemaVersion(CURRENT_APPLICATION_SCHEMA_VERSION):
            logger.debug(
                "DB invalid: app ID %s, db schema version %s, app schema version %s",
                self.applicationID,
                self.dbSchemaVersion,
                self.applicationSchemaVersion,
            )
            return False
        for table in TABLES:
            if not self._tableExists(table.sqlmeta.table):
                logger.debug("Table %s missing", table)
                return False
        return True

    def _columnExists(self, table_name: str, column_name: str) -> bool:
        """Determine if table exists in DB

        Args:
            table_name (str): name of the table
            column_name (str): name of the column

        Returns:
            bool: True if column exists
        """
        return column_name in (
            x[1]
            for x in self._rawCursor.execute(
                f"PRAGMA table_info('{table_name}')"
            ).fetchall()
        )

    def _indexExists(self, index_name: str) -> bool:
        """Determine if an index exists in DB

        Args:
            index_name (str): name of the index

        Returns:
            bool: True if index exists
        """
        return (
            len(
                self._rawCursor.execute(f"PRAGMA index_list('{index_name}')").fetchall()
            )
            > 0
        )

    def _tableExists(self, table_name: str) -> bool:
        """Determine if table exists in DB

        Args:
            table_name (str): name of the table

        Returns:
            bool: True if table exists
        """
        return (
            len(
                self._rawCursor.execute(f"PRAGMA table_list('{table_name}')").fetchall()
            )
            > 0
        )

    def _new(self):
        """Setup new database"""
        logger.debug("DatabaseController: New file, creating complete schema")
        for table in TABLES:
            table.createTable(connection=self.connection)

        self.applicationID = APPLICATION_ID
        self.applicationSchemaVersion = CURRENT_APPLICATION_SCHEMA_VERSION

    def _schemaVersion(self, version: int) -> bool:
        return (
            self.applicationID == APPLICATION_ID
            and self.dbSchemaVersion > 0
            and self.applicationSchemaVersion == version
        )

    def _upgrade(self):
        """Upgrade existing database

        Attempts to upgrade database based on expected values of SQLite's
        applicationID, dbSchemaVersion and user_version. applicationID and
        user_version are set by this class. dbSchemaVersion is automatically
        incremented by SQLite.

        Raises:
            ValueError:
        """
        logger.debug("DatabaseController: Upgrading if possible")

        # self._upgrade_to_schema_2()

        if not self.validSchema:
            # upgrade has failed for some reason
            logger.error("unable to upgrade")
            raise ValueError("unable to upgrade")

        logger.debug("DatabaseController: Upgrade successful")

    def close(self):
        """Close the database"""
        if sqlobject.sqlhub.processConnection == self.connection:
            sqlobject.sqlhub.processConnection = None
        self.connection.close()
