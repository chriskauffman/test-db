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
        created_at (DateTimeCol): creation date
        updated_at (DateTimeCol): last updated date
    """

    created_at: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )
    updated_at: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )


class TestDBSQLObject(BaseSQLObject):
    """TestDBSQLObject SQLObject

    Attributes:
        gid (StringCol): global ID for the object
        attributes (JSONCol): JSON attributes for the object
                              Note: the DB isn't updated until the object is saved
                                    (no DB updates when individual fields are changed)
    """

    _gid_prefix: str = "tdb"

    @classmethod
    def _generate_gid(cls) -> str:
        """Generate a TypeID

        Returns:
            str: new TypeID
        """
        return str(TypeID(cls._gid_prefix))

    @classmethod
    def valid_gid(cls, gid: str) -> bool:
        """Determines if a string is a valid global ID

        Args:
            gid (str):

        Returns:
            bool: True when valid
        """
        try:
            global_type_id = TypeID.from_string(gid)
        except InvalidTypeIDStringException:
            return False
        except PrefixValidationException:
            return False
        except SuffixValidationException:
            return False
        if global_type_id.prefix != cls._gid_prefix:
            return False
        return True

    gid: StringCol = StringCol(alternateID=True, default=None)
    attributes: JSONCol = JSONCol(default=None)

    def _set_gid(self, value):
        if value:
            if self.valid_gid(value):
                self._SO_set_gid(value)
            else:
                raise ValueError(f"Invalid gid value: {value}")
        else:
            self._SO_set_gid(self._generate_gid())
