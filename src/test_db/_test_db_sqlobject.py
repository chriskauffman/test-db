import logging

from sqlobject import DateTimeCol, JSONCol, SQLObject, StringCol  # type: ignore
import sqlobject.sqlbuilder  # type: ignore

from typeid import TypeID
from typeid.errors import (
    InvalidTypeIDStringException,
    PrefixValidationException,
    SuffixValidationException,
)


logger = logging.getLogger(__name__)


class BaseSQLObject(SQLObject):
    """TestDBSQLObject SQLObject

    Attributes:
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    createdAt: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )
    updatedAt: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )


class TestDBSQLObject(BaseSQLObject):
    """TestDBSQLObject SQLObject

    Attributes:
        gID (StringCol): global ID for the object
        attributes (JSONCol): JSON attributes for the object
                              Note: the DB isn't updated until the object is saved
                                    (no DB updates when individual fields are changed)
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

    def _set_gID(self, value):
        if value:
            if self.validGID(value):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(self._generateGID())
