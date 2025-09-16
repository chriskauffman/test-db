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

from test_db._database_options import _GlobalDatabaseOptions
from test_db._full_sqlobject import FullSQLObject
from test_db._settings import KeyValue

ENCODING = "utf-8"

logger = logging.getLogger(__name__)


class PersonalOAuth2Token(FullSQLObject):
    """PersonalOAuth2Token SQLObject

    Attributes:
        clientID (StringCol): OAUth client ID
        person (ForeignKey): the DB ID of the owner of the bank account
        encryptedToken (BLOBCol): the token
        clientIDPersonIndex (DatabaseIndex):
    """

    # Class seems to need a base definitions
    _kdf = None
    _key = None
    _globalDatabaseOptions = None
    __fernet = None
    __fernetIterations = None
    __password = None
    __salt = None

    _gIDPrefix: str = "pot"

    clientID: StringCol = StringCol()
    person: ForeignKey = ForeignKey("Person", cascade=True)
    encryptedToken: BLOBCol = BLOBCol(default=None)

    clientIDPersonIndex: DatabaseIndex = DatabaseIndex(clientID, person, unique=True)

    def _init(self, *args, **kw):
        SQLObject._init(self, *args, **kw)
        self._globalDatabaseOptions = None
        self._kdf = None
        self._key = None
        self.__fernet = None
        self.__fernetIterations = None
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
                iterations=self._fernetIterations,
            )
            self._key = base64.urlsafe_b64encode(self._kdf.derive(self._password))
            self.__fernet = Fernet(self._key)
        return self.__fernet

    @property
    def _fernetIterations(self):
        """Fernet iterations"""
        if not self.__fernetIterations:
            if not self._globalDatabaseOptions:
                self._globalDatabaseOptions = _GlobalDatabaseOptions()
            if not self._globalDatabaseOptions.fernetIterations:
                raise ValueError("fernetIterations not set")
            self.__fernetIterations = self._globalDatabaseOptions.fernetIterations
        return self.__fernetIterations

    @property
    def _password(self):
        """Encryption password"""
        if not self.__password:
            if not self._globalDatabaseOptions:
                self._globalDatabaseOptions = _GlobalDatabaseOptions()
            if not self._globalDatabaseOptions.databaseEncryptionKey:
                raise ValueError("databaseEncryptionKey not set")
            self.__password = self._globalDatabaseOptions.databaseEncryptionKey.encode(
                ENCODING
            )
        return self.__password

    @property
    def _salt(self):
        """Encryption salt"""
        try:
            self.__salt = KeyValue.byKey(
                "oauth2_token_encryption_salt", connection=self._connection
            ).value.encode(ENCODING)
        except SQLObjectNotFound:
            self.__salt = KeyValue(
                key="oauth2_token_encryption_salt",
                value=secrets.token_hex(16),
                connection=self._connection,
            ).value.encode(ENCODING)
        return self.__salt

    @property
    def token(self) -> Optional[dict]:
        """Returns OAuth 2 token - converts encrypted blob to dict"""
        if self.encryptedToken is None:
            return None
        json_string = self._fernet.decrypt(self.encryptedToken).decode(ENCODING)
        return json.loads(json_string)

    @token.setter
    def token(self, newToken: Optional[dict]):
        """Sets OAuth 2 token - converts dict to encrypted blob"""
        if newToken is None:
            self.encryptedToken = None
        else:
            json_string = json.dumps(newToken)
            self.encryptedToken = self._fernet.encrypt(json_string.encode(ENCODING))
