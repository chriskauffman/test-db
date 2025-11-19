import logging

from sqlobject import SQLObject  # type: ignore

from typeid import TypeID
from typeid.errors import (
    InvalidTypeIDStringException,
    PrefixValidationException,
    SuffixValidationException,
)

logger = logging.getLogger(__name__)


class FullSQLObject(SQLObject):
    """FullSQLObject SQLObject"""

    _gIDPrefix: str = "tdb"

    @classmethod
    def _generateGID(cls) -> str:
        """Generate a TypeID

        Returns:
            str: new TypeID
        """
        return str(TypeID(cls._gIDPrefix))

    @classmethod
    def validGID(cls, gID: str) -> bool:
        """Determines if a string is a valid global ID

        Args:
            gID (str):

        Returns:
            bool: True when valid
        """
        try:
            globalTypeID = TypeID.from_string(gID)
        except InvalidTypeIDStringException:
            return False
        except PrefixValidationException:
            return False
        except SuffixValidationException:
            return False
        if globalTypeID.prefix != cls._gIDPrefix:
            return False
        return True
