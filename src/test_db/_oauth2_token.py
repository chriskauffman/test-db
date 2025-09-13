import base64
import json
import logging
import secrets
from typing_extensions import Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from sqlobject import (  # type: ignore
    BLOBCol,
    DatabaseIndex,
    ForeignKey,
    SQLObject,
    SQLObjectNotFound,
    StringCol,
)

import test_db as test_db
from ._settings import Settings
from ._test_db_sqlobject import TestDBSQLObject

ENCODING = "utf-8"

logger = logging.getLogger(__name__)


class _GlobalDatabaseEncryptionOptions:
    @property
    def database_encryption_key(self):
        return test_db.database_encryption_key


class PersonalOAuth2Token(TestDBSQLObject):
    """PersonalOAuth2Token SQLObject

    Attributes:
        client_id (StringCol): OAUth client ID
        person (ForeignKey): the DB ID of the owner of the bank account
        encrypted_token (BLOBCol): the token
        client_id_person_index (DatabaseIndex):
    """

    # Class seems to need a base definitions
    _kdf = None
    _key = None
    _global_database_encryption_options = None
    __fernet = None
    __password = None
    __salt = None

    _gid_prefix: str = "pot"

    client_id: StringCol = StringCol()
    person: ForeignKey = ForeignKey("Person", cascade=True)
    encrypted_token: BLOBCol = BLOBCol(default=None)

    client_id_person_index: DatabaseIndex = DatabaseIndex(
        client_id, person, unique=True
    )

    def _init(self, *args, **kw):
        SQLObject._init(self, *args, **kw)
        self._global_database_encryption_options = None
        self._kdf = None
        self._key = None
        self.__fernet = None
        self.__password = None
        self.__salt = None

    @property
    def _fernet(self):
        """Fernet encryption"""
        if not self.__fernet:
            self._kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self._salt,
                iterations=1_000_000,
            )
            self._key = base64.urlsafe_b64encode(self._kdf.derive(self._password))
            self.__fernet = Fernet(self._key)
        return self.__fernet

    @property
    def _password(self):
        """Encryption password"""
        if not self.__password:
            self._global_database_encryption_options = (
                _GlobalDatabaseEncryptionOptions()
            )
            if not self._global_database_encryption_options.database_encryption_key:
                raise ValueError("database_encryption_key not set")
            self.__password = (
                self._global_database_encryption_options.database_encryption_key.encode(
                    ENCODING
                )
            )
        return self.__password

    @property
    def _salt(self):
        """Encryption salt"""
        try:
            self.__salt = Settings.byKey(
                "oauth2_token_encryption_salt", connection=self._connection
            ).value.encode(ENCODING)
        except SQLObjectNotFound:
            self.__salt = Settings(
                key="oauth2_token_encryption_salt",
                value=secrets.token_hex(16),
                connection=self._connection,
            ).value.encode(ENCODING)
        return self.__salt

    @property
    def token(self) -> Optional[dict]:
        """Returns OAuth 2 token - converts encrypted blob to dict"""
        if self.encrypted_token is None:
            return None
        json_string = self._fernet.decrypt(self.encrypted_token).decode(ENCODING)
        return json.loads(json_string)

    @token.setter
    def token(self, new_token: Optional[dict]):
        """Sets OAuth 2 token - converts dict to encrypted blob"""
        if new_token is None:
            self.encrypted_token = None
        else:
            json_string = json.dumps(new_token)
            self.encrypted_token = self._fernet.encrypt(json_string.encode(ENCODING))
