import logging
import pickle
from typing_extensions import Any, Optional

from sqlobject.col import BLOBCol, BinaryValidator, SOBLOBCol  # type: ignore


PICKLE_PROTOCOL = 5  # selecting 5 for Python 3.8+

logger = logging.getLogger(__name__)


class EncryptedPickleValidator(BinaryValidator):
    """EncryptedPickleCol SQLObject"""

    # dbFernet: Optional[Fernet] = None

    def getDbFernet(self, state):
        try:
            return self.dbFernet
        except AttributeError:
            return self.soCol.getDbFernet(state)

    def to_python(self, value, state) -> Optional[Any]:
        if value is None:
            return None
        dbFernet = self.getDbFernet(state)
        if dbFernet:
            return pickle.loads(dbFernet.decrypt(value))
        else:
            raise ValueError("Invalid Fernet config, check dbFernet value")

    def from_python(self, value, state) -> Optional[Any]:
        if value is None:
            return None
        dbFernet = self.getDbFernet(state)
        if dbFernet:
            return dbFernet.encrypt(pickle.dumps(value, protocol=self.pickleProtocol))
        else:
            raise ValueError("Invalid Fernet config, check dbFernet value")


class SOEncryptedPickleCol(SOBLOBCol):
    # dbFernet: Optional[Fernet] = None

    def __init__(self, **kw):
        self.dbFernet = kw.pop("dbFernet", None)
        self.pickleProtocol = kw.pop("pickleProtocol", pickle.HIGHEST_PROTOCOL)
        super(SOEncryptedPickleCol, self).__init__(**kw)

    def createValidators(self):
        return [
            EncryptedPickleValidator(
                name=self.name,
                pickleProtocol=self.pickleProtocol,
            )
        ] + super(SOEncryptedPickleCol, self).createValidators()

    def getDbFernet(self, state):
        if self.dbFernet:
            return self.dbFernet
        try:
            dbFernet = state.soObject.sqlmeta.dbFernet
        except AttributeError:
            dbFernet = None
        if dbFernet:
            return dbFernet
        try:
            connection = state.connection or state.soObject._connection
        except AttributeError:
            dbFernet = None
        else:
            dbFernet = getattr(connection, "dbFernet", None)
        if not dbFernet:
            raise ValueError("Invalid Fernet config, check dbFernet value")
        return dbFernet


class EncryptedPickleCol(BLOBCol):
    baseClass = SOEncryptedPickleCol
