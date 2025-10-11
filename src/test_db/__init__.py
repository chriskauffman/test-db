import logging

import sqlobject  # type: ignore
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
from test_db._job import Job as Job
from test_db._key_value_secure import KeyValueSecure as KeyValueSecure
from test_db._key_json import KeyJson as KeyJson
from test_db._key_value import KeyValue as KeyValue
from test_db._organization import Organization as Organization
from test_db._person import Person as Person
from test_db._personal_key_json import PersonalKeyJson as PersonalKeyJson
from test_db._personal_key_value import PersonalKeyValue as PersonalKeyValue
from test_db._personal_key_value_secure import (
    PersonalKeyValueSecure as PersonalKeyValueSecure,
)
from test_db._views._person import PersonView as PersonView

# Global database options
databaseEncryptionKey: Optional[str] = None
# Django recommendation from 2025
# https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
fernetIterations: int = 1_200_000

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
