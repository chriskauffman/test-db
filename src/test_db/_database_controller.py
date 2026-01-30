import base64
from datetime import datetime, timezone
import logging
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import sqlobject  # type: ignore

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Optional

from test_db._global_database_options import _GlobalDatabaseOptions
from test_db._job import Job
from test_db._job_key_value import JobKeyValue
from test_db._key_value import KeyValue
from test_db._organization import Organization
from test_db._organization_address import OrganizationAddress
from test_db._organization_bank_account import OrganizationBankAccount
from test_db._organization_key_value import OrganizationKeyValue
from test_db._person import Person
from test_db._person_address import PersonAddress
from test_db._person_bank_account import PersonBankAccount
from test_db._person_debit_card import PersonDebitCard
from test_db._person_key_value import PersonKeyValue
from test_db._person_secure_key_value import PersonSecureKeyValue

from test_db._listeners import (
    handleRowCreatedSignal,
    handleRowCreateSignal,
    handleRowUpdateSignal,
)

ENCODING = "utf-8"
IN_MEMORY_DB_FILE = "sqlite:/:memory:"

# Note: order of TABLES matters for creation due to foreign key dependencies
TABLES = (
    KeyValue,
    Organization,
    OrganizationAddress,
    OrganizationBankAccount,
    OrganizationKeyValue,
    Person,
    PersonAddress,
    PersonBankAccount,
    PersonDebitCard,
    PersonKeyValue,
    PersonSecureKeyValue,
    Job,
    JobKeyValue,
)

# Entity is base class, do not add listeners
TABLES_WITH_SIGNAL_HANDLING = [table for table in TABLES if table not in ()]

APPLICATION_ID = 990001
CURRENT_APPLICATION_SCHEMA_VERSION = 1

logger = logging.getLogger(__name__)


class DatabaseController:
    """DatabaseController

    Basic class to handle the connection, configuration and upgrade of a test_db

    Args:
        connectionURI (str): SQLObject connection URI
        defaultConnection (bool, optional): sets DB as default sqlobject connection
        upgrade (bool, optional): upgrade the database if it is out of date
        databaseEncryptionKey (Optional[str]):

    Raises:
        ValueError: invalid database

    Instance Attributes:
        applicationID (int): database application ID unique to test_db
        applicationSchemaVersion (int): test_db schema version number
        connection (sqlobject.connectionForURI)
        connectionURI (str): location of DB file
        validSchema (bool): True if schema passes checks
    """

    def __init__(
        self,
        connectionURI: str,
        defaultConnection: bool = False,
        upgrade: bool = False,
        databaseEncryptionKey: Optional[str] = None,
    ) -> None:
        self.connectionURI = connectionURI

        self.connection = sqlobject.connectionForURI(self.connectionURI)
        self.connection.tdbGlobalDatabaseOptions = _GlobalDatabaseOptions()

        self._raw = self.connection.getConnection()
        self._rawCursor = self._raw.cursor()

        logger.debug("connectionURI=%s", self.connectionURI)
        logger.debug("applicationID=%s", self.applicationID)
        logger.debug("applicationSchemaVersion=%s", self.applicationSchemaVersion)

        if self._isTestDB:
            if self.validSchema:
                pass
            else:
                if upgrade:
                    self._upgrade()
                else:
                    raise ValueError("test_db file needs upgrade")
        else:
            if self._isEmptyDB:
                self._new()
            else:
                raise ValueError("not a test_db file")

        # Database specific configuration
        if "sqlite" in str(self.connectionURI):
            self._rawCursor.execute("PRAGMA foreign_keys = ON")

        for table in TABLES_WITH_SIGNAL_HANDLING:
            sqlobject.events.listen(
                handleRowCreateSignal, table, sqlobject.events.RowCreateSignal
            )
            sqlobject.events.listen(
                handleRowUpdateSignal, table, sqlobject.events.RowUpdateSignal
            )
            sqlobject.events.listen(
                handleRowCreatedSignal, table, sqlobject.events.RowCreatedSignal
            )

        databaseEncryptionKey = (
            databaseEncryptionKey
            or self.connection.tdbGlobalDatabaseOptions.databaseEncryptionKey
        )
        if databaseEncryptionKey:
            try:
                fernet_salt = KeyValue.byKey(
                    "TestDB_EncryptedPickleColSalt", connection=self.connection
                ).value.encode(ENCODING)
            except sqlobject.SQLObjectNotFound:
                fernet_salt = KeyValue(
                    key="TestDB_EncryptedPickleColSalt",
                    value=secrets.token_hex(16),
                    connection=self.connection,
                ).value.encode(ENCODING)
            fernet_kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=fernet_salt,
                iterations=self.connection.tdbGlobalDatabaseOptions.fernetIterations,
            )
            fernet_key_material = databaseEncryptionKey.encode(ENCODING)
            key = base64.urlsafe_b64encode(fernet_kdf.derive(fernet_key_material))
            self.connection.dbFernet = Fernet(key)
        else:
            logger.warning(
                "databaseEncryptionKey not set, encrypted storage not available"
            )
            self.connection.dbFernet = None

        if defaultConnection:
            sqlobject.sqlhub.processConnection = self.connection

    @property
    def applicationID(self) -> int:
        if self.connection.tableExists(KeyValue.sqlmeta.table):
            try:
                return int(
                    KeyValue.byKey(
                        "TestDB_ApplicationID", connection=self.connection
                    ).value
                )
            except sqlobject.SQLObjectNotFound:
                return 0
        return 0

    @applicationID.setter
    def applicationID(self, applicationID: int) -> None:
        if self.connection.tableExists(KeyValue.sqlmeta.table):
            try:
                KeyValue.byKey(
                    "TestDB_ApplicationID", connection=self.connection
                ).value = str(applicationID)
            except sqlobject.SQLObjectNotFound:
                now = datetime.now(timezone.utc)
                KeyValue(
                    key="TestDB_ApplicationID",
                    value=str(applicationID),
                    createdAt=now,
                    updatedAt=now,
                    connection=self.connection,
                )

    @property
    def applicationSchemaVersion(self) -> int:
        if self.connection.tableExists(KeyValue.sqlmeta.table):
            try:
                return int(
                    KeyValue.byKey(
                        "TestDB_ApplicationSchemaVersion", connection=self.connection
                    ).value
                )
            except sqlobject.SQLObjectNotFound:
                return 0
        return 0

    @applicationSchemaVersion.setter
    def applicationSchemaVersion(self, applicationSchemaVersion: int) -> None:
        if self.connection.tableExists(KeyValue.sqlmeta.table):
            try:
                KeyValue.byKey(
                    "TestDB_ApplicationSchemaVersion", connection=self.connection
                ).value = str(applicationSchemaVersion)
            except sqlobject.SQLObjectNotFound:
                now = datetime.now(timezone.utc)
                KeyValue(
                    key="TestDB_ApplicationSchemaVersion",
                    value=str(applicationSchemaVersion),
                    createdAt=now,
                    updatedAt=now,
                    connection=self.connection,
                )

    @property
    def _isEmptyDB(self) -> bool:
        return self.applicationID == 0 and self.applicationSchemaVersion == 0

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
                "DB invalid: app ID %s, app schema version %s",
                self.applicationID,
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
        try:
            self._rawCursor.execute(f"SELECT {column_name} FROM {table_name} LIMIT 1")
            return True
        except Exception:
            return False

    def _tableExists(self, table_name: str) -> bool:
        """Determine if table exists in DB

        Args:
            table_name (str): name of the table

        Returns:
            bool: True if table exists
        """
        try:
            self._rawCursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
            return True
        except Exception:
            return False

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
            and self.applicationSchemaVersion == version
        )

    def _upgrade(self):
        """Upgrade existing database

        Attempts to upgrade database based on expected values of the DB's
        applicationID and applicationSchemaVersion. applicationID and
        applicationSchemaVersion are set by this class.

        Raises:
            ValueError:
        """
        logger.debug("DatabaseController: Upgrading if possible")

        # self._upgrade_to_schema_vX()

        if not self.validSchema:
            # upgrade has failed for some reason
            logger.error("unable to upgrade")
            raise ValueError("unable to upgrade")

        logger.debug("DatabaseController: Upgrade successful")

    # def _upgrade_to_schema_vX(self):
    #     # Upgrade to application schema X
    #     if (
    #         self.applicationID == APPLICATION_ID
    #         and self.applicationSchemaVersion == 1
    #     ):
    #         logger.info("Upgrading DB schema to vX")

    #         # (sqlite doesn't allow alter on table with unique column)
    #         self._rawCursor.execute("PRAGMA foreign_keys = OFF")

    #         # Update tables here

    #         self._rawCursor.execute("PRAGMA foreign_keys = ON")
    #         self.applicationID = APPLICATION_ID
    #         self.applicationSchemaVersion = CURRENT_APPLICATION_SCHEMA_VERSION

    def close(self):
        """Close the database"""
        try:
            if sqlobject.sqlhub.processConnection == self.connection:
                sqlobject.sqlhub.processConnection = None
        except AttributeError:
            pass
        self.connection.close()
