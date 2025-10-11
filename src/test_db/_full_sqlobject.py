import logging

from sqlobject import JSONCol, StringCol  # type: ignore

from typeid import TypeID
from typeid.errors import (
    InvalidTypeIDStringException,
    PrefixValidationException,
    SuffixValidationException,
)

from test_db._base_sqlobject import BaseSQLObject

logger = logging.getLogger(__name__)


class FullSQLObject(BaseSQLObject):
    """FullSQLObject SQLObject

    Attributes:
        gID (StringCol): global ID for the object
        attributes (JSONCol): JSON attributes for the object
                              Note: the DB isn't updated until the object is saved
                                    (no DB updates when individual fields are changed)
        description (StringCol): description of the object
    """

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

    gID: StringCol = StringCol(alternateID=True, default=None)
    attributes: JSONCol = JSONCol(default=None)
    description: StringCol = StringCol(default=None)

    def _set_gID(self, value):
        if value:
            if self.validGID(value):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(self._generateGID())
