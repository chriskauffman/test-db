"""test-db package

Provides a simple test database with various entities and
views to assist applications and utilities in managing test data.

Example:
    import test_db

    db = test_db.DatabaseController("sqlite:test_db.sqlite", autoCreate=True)
    new_person = test_db.PersonView.add()
"""

import logging

import sqlobject  # type: ignore
from sqlobject import SQLObjectNotFound as SQLObjectNotFound
from sqlobject.dberrors import DuplicateEntryError as DuplicateEntryError  # type: ignore

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Optional

from test_db._address import Address as Address
from test_db._bank_account import BankAccount as BankAccount
from test_db._database_controller import (
    DatabaseController as DatabaseController,
)
from test_db._database_controller import (
    IN_MEMORY_DB_FILE as IN_MEMORY_DB_FILE,
)
from test_db._debit_card import DebitCard as DebitCard
from test_db._entity_key_value import EntityKeyValue as EntityKeyValue
from test_db._entity_secure_key_value import (
    EntitySecureKeyValue as EntitySecureKeyValue,
)
from test_db._job import Job as Job
from test_db._job_key_value import JobKeyValue as JobKeyValue
from test_db._key_value import KeyValue as KeyValue
from test_db._organization import Organization as Organization
from test_db._person import Person as Person

from test_db._views._address import AddressView as AddressView
from test_db._views._bank_account import BankAccountView as BankAccountView
from test_db._views._debit_card import DebitCardView as DebitCardView
from test_db._views._entity_key_value import EntityKeyValueView as EntityKeyValueView
from test_db._views._entity_secure_key_value import (
    EntitySecureKeyValueView as EntitySecureKeyValueView,
)
from test_db._views._job import JobView as JobView
from test_db._views._key_value import KeyValueView as KeyValueView
from test_db._views._organization import OrganizationView as OrganizationView
from test_db._views._person import PersonView as PersonView

# Global database options
autoCreateDependents: bool = True
databaseEncryptionKey: Optional[str] = None
# Django recommendation from 2025
# https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
fernetIterations: int = 1_200_000

RESTRICTED_KEYS = (
    "TestDB_ApplicationID",
    "TestDB_ApplicationSchemaVersion",
    "TestDB_EncryptedPickleColSalt",
)

logger = logging.getLogger(__name__)


def validConnection(connection: sqlobject.connectionForURI = None) -> bool:
    """Checks for valid caonnection to DatabaseController, if connection not supplied checks
    default connection

    Args:
        connection (sqlobject.connectionForURI, optional):

    Returns:
        bool: True if connection is valid
    """
    if connection:
        return isinstance(
            connection, sqlobject.sqlite.sqliteconnection.SQLiteConnection
        )
    try:
        return isinstance(
            sqlobject.sqlhub.processConnection,
            sqlobject.sqlite.sqliteconnection.SQLiteConnection,
        )
    except AttributeError:
        return False
