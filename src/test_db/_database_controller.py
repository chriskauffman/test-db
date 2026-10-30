import base64
import logging
import secrets
import sqlite3
from datetime import UTC, datetime
from types import SimpleNamespace

import sqlobject
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pydantic import SecretStr
from sqlobject import sqlbuilder
from sqlobject.col import BinaryValidator

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

APPLICATION_ID = 990001
CURRENT_APPLICATION_SCHEMA_VERSION = 1

logger = logging.getLogger(__name__)


class _SQLiteConnection(sqlite3.Connection):
    """Enable foreign-key enforcement on each physical SQLite connection."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.execute("PRAGMA foreign_keys = ON").close()


class DatabaseController:
    """DatabaseController

    Basic class to handle the connection, configuration and upgrade of a test_db

    Args:
        connectionURI (str | SecretStr): SQLObject connection URI
        defaultConnection (bool, optional): sets DB as default sqlobject connection
        upgrade (bool, optional): upgrade the database if it is out of date
        databaseEncryptionKey (str | None):

    Raises:
        ValueError: invalid database

    Instance Attributes:
        applicationID (int): database application ID unique to test_db
        applicationSchemaVersion (int): test_db schema version number
        connection (sqlobject.connectionForURI)
        connectionURI (SecretStr): location of DB file
        validSchema (bool): True if schema passes checks
    """

    def __init__(
        self,
        connectionURI: str | SecretStr,
        defaultConnection: bool = False,
        upgrade: bool = False,
        databaseEncryptionKey: str | None = None,
    ) -> None:
        if isinstance(connectionURI, SecretStr):
            self.connectionURI = connectionURI
        else:
            self.connectionURI = SecretStr(connectionURI)

        self.connection = sqlobject.connectionForURI(
            self.connectionURI.get_secret_value()
        )
        self.connection.tdbGlobalDatabaseOptions = _GlobalDatabaseOptions()
        if self.connection.dbName == "sqlite":
            # URI arguments cannot carry a callable factory; keep the cached adapter.
            self.connection._connOptions["factory"] = _SQLiteConnection
            self.connection.query("PRAGMA foreign_keys = ON")

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

        databaseEncryptionKey = (
            databaseEncryptionKey
            or self.connection.tdbGlobalDatabaseOptions.databaseEncryptionKey
        )
        if databaseEncryptionKey:
            try:
                fernet_salt = KeyValue.byKey(
                    "TestDB_EncryptedPickleColSalt", connection=self.connection
                ).value
            except sqlobject.SQLObjectNotFound:
                fernet_salt = None
            try:
                iterations_record = KeyValue.byKey(
                    "TestDB_EncryptedPickleColIterations",
                    connection=self.connection,
                )
            except sqlobject.SQLObjectNotFound:
                iterations_record = None
                fernet_iterations = (
                    self.connection.tdbGlobalDatabaseOptions.fernetIterations
                )
            else:
                if not fernet_salt:
                    raise ValueError("Encryption metadata is missing its salt")
                try:
                    fernet_iterations = int(iterations_record.value)
                except (TypeError, ValueError) as exc:
                    raise ValueError(
                        "Encryption iterations must be a positive integer"
                    ) from exc
            if type(fernet_iterations) is not int or fernet_iterations <= 0:
                raise ValueError("Encryption iterations must be a positive integer")
            new_salt = fernet_salt is None
            if new_salt:
                fernet_salt = secrets.token_hex(16)
            fernet_kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=fernet_salt.encode(ENCODING),
                iterations=fernet_iterations,
            )
            fernet_key_material = databaseEncryptionKey.encode(ENCODING)
            key = base64.urlsafe_b64encode(fernet_kdf.derive(fernet_key_material))
            fernet = Fernet(key)
            if iterations_record is None:
                if not new_salt:
                    # Authenticate legacy ciphertext before pinning an unverified count.
                    query = sqlbuilder.Select(
                        PersonSecureKeyValue.q.value,
                        where=sqlbuilder.ISNOTNULL(PersonSecureKeyValue.q.value),
                        limit=1,
                    )
                    row = self.connection.queryOne(self.connection.sqlrepr(query))
                    if row is not None:
                        token = BinaryValidator(name="value").to_python(
                            row[0], SimpleNamespace(connection=self.connection)
                        )
                        try:
                            fernet.decrypt(token)
                        except InvalidToken as exc:
                            raise ValueError(
                                "Unable to authenticate legacy encrypted data; "
                                "check the original password and iteration count"
                            ) from exc
                if new_salt:
                    KeyValue(
                        key="TestDB_EncryptedPickleColSalt",
                        value=fernet_salt,
                        connection=self.connection,
                    )
                KeyValue(
                    key="TestDB_EncryptedPickleColIterations",
                    value=str(fernet_iterations),
                    connection=self.connection,
                )
            self.connection.dbFernet = fernet
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
                now = datetime.now(UTC)
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
                now = datetime.now(UTC)
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
        return self.applicationID == APPLICATION_ID

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
        return True

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
