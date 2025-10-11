import logging

from sqlobject import StringCol  # type: ignore

from test_db._base_sqlobject import BaseSQLObject
from test_db._encrypted_pickle_col import EncryptedPickleCol


logger = logging.getLogger(__name__)


class KeyValueSecure(BaseSQLObject):
    """PersonalOAuth2Token SQLObject

    Attributes:
        key (StringCol):
        value (EncryptedPickleCol):
    """

    key: StringCol = StringCol(alternateID=True, unique=True)
    value: EncryptedPickleCol = EncryptedPickleCol(default=None)
