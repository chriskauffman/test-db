import logging
import re
import sqlite3
from datetime import UTC, datetime
from importlib.resources import files

import sqlobject
from pydantic import SecretStr

from test_db._connection import connectionForURI
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
    Job,
    JobKeyValue,
)

APPLICATION_ID = 990001
CURRENT_APPLICATION_SCHEMA_VERSION = 2
MIGRATIONS = {
    "sqlite": ("upgrade_sqlite_remove_encryption.sql",),
    "postgres": ("upgrade_postgres_remove_encryption.sql",),
    "mysql": ("upgrade_mysql_remove_encryption.sql",),
}


def _migration_statements(script: str):
    script = re.sub(r"(?m)^[ \t]*--[^\r\n]*(?:\r?\n|$)", "", script)
    return (statement.strip() for statement in script.split(";") if statement.strip())

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
    Initialization failures raise ValueError when the database is foreign or
    outdated.

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
    ) -> None:
        if isinstance(connectionURI, SecretStr):
            self.connectionURI = connectionURI
        else:
            self.connectionURI = SecretStr(connectionURI)

        uri = self.connectionURI.get_secret_value()
        opener = sqlobject.connectionForURI.__self__
        self._connection_was_cached = uri in opener.cachedURIs
        self.connection = connectionForURI(uri)
        self._connection_uri = uri
        self._initialize(
            defaultConnection=defaultConnection,
            upgrade=upgrade,
        )

    def _initialize(
        self,
        defaultConnection: bool,
        upgrade: bool,
    ) -> None:
        try:
            self._initialize_without_cleanup(
                defaultConnection=defaultConnection,
                upgrade=upgrade,
            )
        except Exception:
            self._cleanup_failed_initialization()
            raise

    def _cleanup_failed_initialization(self) -> None:
        if getattr(self, "_rawCursor", None) is not None:
            self._rawCursor.close()
            del self._rawCursor
        if getattr(self, "_raw", None) is not None:
            self.connection.releaseConnection(self._raw)
            del self._raw
        if not self._connection_was_cached:
            opener = sqlobject.connectionForURI.__self__
            for uri, connection in list(opener.cachedURIs.items()):
                if connection is self.connection:
                    opener.cachedURIs.pop(uri)
            self.connection.close()

    def _initialize_without_cleanup(
        self,
        defaultConnection: bool,
        upgrade: bool,
    ) -> None:
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
        # Only a database with no tables at all is safe to initialise; anything
        # else that isn't a test_db belongs to someone else.
        return not self.connection.listTables()

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
        return self._schemaInvariants

    @property
    def _schemaInvariants(self) -> bool:
        """Validate the schema details that version metadata cannot prove."""
        return self._schema_invariants(set(self.connection.listTables()))

    def _schema_invariants(self, tables: set[str]) -> bool:
        if any(table.sqlmeta.table not in tables for table in TABLES):
            return False
        if "person_secure_key_value" in tables:
            return False

        return self._required_cascades_present()

    def _required_cascades_present(self) -> bool:
        if self.connection.dbName == "sqlite":
            rows = self._rawCursor.execute("PRAGMA foreign_key_list(job)").fetchall()
            cascades = {(row[2], row[6].upper()) for row in rows}
            required_cascades = {("organization", "CASCADE"), ("person", "CASCADE")}
        elif self.connection.dbName == "postgres":
            self._rawCursor.execute(
                """
                SELECT tc.constraint_name, rc.delete_rule
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.referential_constraints AS rc
                  ON rc.constraint_schema = tc.constraint_schema
                 AND rc.constraint_name = tc.constraint_name
                WHERE tc.constraint_schema = current_schema()
                  AND tc.table_name = 'job'
                  AND tc.constraint_name IN (
                      'organization_id_exists', 'person_id_exists'
                  )
                """
            )
            cascades = {(row[0], row[1].upper()) for row in self._rawCursor.fetchall()}
            required_cascades = {
                ("organization_id_exists", "CASCADE"),
                ("person_id_exists", "CASCADE"),
            }
        elif self.connection.dbName == "mysql":
            self._rawCursor.execute(
                """
                SELECT tc.constraint_name, rc.delete_rule
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.referential_constraints AS rc
                  ON rc.constraint_schema = tc.constraint_schema
                 AND rc.constraint_name = tc.constraint_name
                WHERE tc.constraint_schema = DATABASE()
                  AND tc.table_name = 'job'
                  AND tc.constraint_name IN (
                      'job_organization_id_exists', 'job_person_id_exists'
                  )
                """
            )
            cascades = {(row[0], row[1].upper()) for row in self._rawCursor.fetchall()}
            required_cascades = {
                ("job_organization_id_exists", "CASCADE"),
                ("job_person_id_exists", "CASCADE"),
            }
        else:
            return False

        return required_cascades <= cascades

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

        if self.applicationSchemaVersion != 1:
            raise ValueError(
                f"unsupported test_db schema version: {self.applicationSchemaVersion}"
            )

        try:
            if self.connection.dbName == "sqlite":
                self._rawCursor.execute("PRAGMA foreign_keys=off")
            if self.connection.dbName != "mysql":
                self._rawCursor.execute("BEGIN")

            for migration in MIGRATIONS[self.connection.dbName]:
                script = (
                    files("test_db._schemas")
                    .joinpath(migration)
                    .read_text(encoding="utf-8")
                )
                for statement in _migration_statements(script):
                    self._execute_migration_statement(statement)

            if not self._raw_schema_is_valid():
                raise ValueError("unable to upgrade")
            self._raw.commit()
        except KeyError as exc:
            raise ValueError(
                f"unsupported database engine: {self.connection.dbName}"
            ) from exc
        except Exception as exc:
            self._raw.rollback()
            if self.connection.dbName == "sqlite":
                self._rawCursor.execute("PRAGMA foreign_keys=on")
            raise ValueError("unable to upgrade test_db schema") from exc
        if self.connection.dbName == "sqlite":
            self._rawCursor.execute("PRAGMA foreign_keys=on")

        if not self.validSchema:
            raise ValueError("unable to upgrade")

        logger.debug("DatabaseController: Upgrade successful")

    def _raw_schema_is_valid(self) -> bool:
        """Validate the migrated schema using the migration connection."""
        if self.connection.dbName == "sqlite":
            self._rawCursor.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        elif self.connection.dbName == "postgres":
            self._rawCursor.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = current_schema()"
            )
        elif self.connection.dbName == "mysql":
            self._rawCursor.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = DATABASE()"
            )
        else:
            return False

        tables = {row[0] for row in self._rawCursor.fetchall()}

        self._rawCursor.execute(
            "SELECT key_name, value FROM key_value "
            "WHERE key_name IN "
            "('TestDB_ApplicationID', 'TestDB_ApplicationSchemaVersion')"
        )
        metadata = dict(self._rawCursor.fetchall())
        if metadata.get("TestDB_ApplicationID") != str(APPLICATION_ID):
            return False
        if metadata.get("TestDB_ApplicationSchemaVersion") != str(
            CURRENT_APPLICATION_SCHEMA_VERSION
        ):
            return False

        return self._schema_invariants(tables)

    def _execute_migration_statement(self, statement: str) -> None:
        """Execute one migration statement, tolerating resumed MariaDB DDL."""
        if self.connection.dbName == "mysql":
            drop = re.search(
                r"ALTER TABLE job DROP FOREIGN KEY (\w+)", statement, re.IGNORECASE
            )
            add = re.search(
                r"ALTER TABLE job ADD CONSTRAINT (\w+)", statement, re.IGNORECASE
            )
            constraint = drop or add
            if constraint:
                constraint_name = constraint.group(1)
                self._rawCursor.execute(
                    "SELECT delete_rule "
                    "FROM information_schema.referential_constraints "
                    "WHERE constraint_schema = DATABASE() "
                    "AND constraint_name = %s",
                    (constraint_name,),
                )
                row = self._rawCursor.fetchone()
                delete_rule = row[0].upper() if row else None
                if drop and delete_rule is None:
                    return
                if add and delete_rule == "CASCADE":
                    return

        self._rawCursor.execute(statement)

    def close(self):
        """Close the database"""
        try:
            if (
                not getattr(self, "_connection_was_cached", False)
                and sqlobject.sqlhub.processConnection == self.connection
            ):
                sqlobject.sqlhub.processConnection = None
        except AttributeError:
            pass
        if getattr(self, "_rawCursor", None) is not None:
            self._rawCursor.close()
            del self._rawCursor
        if getattr(self, "_raw", None) is not None:
            self.connection.releaseConnection(self._raw)
            del self._raw
        if not getattr(self, "_connection_was_cached", False):
            self.connection.close()
