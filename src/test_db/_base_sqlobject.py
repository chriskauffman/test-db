import logging

from sqlobject import DateTimeCol, SQLObject  # type: ignore
import sqlobject.sqlbuilder  # type: ignore


logger = logging.getLogger(__name__)


class BaseSQLObject(SQLObject):
    """FullSQLObject SQLObject

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
