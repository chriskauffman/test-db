import logging

import sqlobject  # type: ignore
from typing_extensions import Optional

from test_db._address import PersonalAddress as PersonalAddress
from test_db._app_settings import AppSettings as AppSettings
from test_db._app_settings import PersonalAppSettings as PersonalAppSettings
from test_db._bank_account import PersonalBankAccount as PersonalBankAccount
from test_db._database_controller import (
    DatabaseController as DatabaseController,
)
from test_db._database_controller import (
    IN_MEMORY_DB_FILE as IN_MEMORY_DB_FILE,
)
from test_db._debit_card import PersonalDebitCard as PersonalDebitCard
from test_db._employer import Employer as Employer
from test_db._job import Job as Job
from test_db._person import Person as Person
from test_db._oauth2_token import PersonalOAuth2Token as PersonalOAuth2Token
from test_db._settings import Settings as Settings

from test_db._bank_account import FakeBankAccount as FakeBankAccount
from test_db._debit_card import FakeDebitCard as FakeDebitCard

from test_db._views._person import PersonView as PersonView

# Global database options
databaseEncryptionKey: Optional[str] = None
# Django recommendation from 2025
# https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
fernetIterations: int = 1_200_000

logger = logging.getLogger(__name__)


class _GlobalDatabaseOptions:
    @property
    def databaseEncryptionKey(self):
        return databaseEncryptionKey

    @property
    def fernetIterations(self):
        return fernetIterations


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
