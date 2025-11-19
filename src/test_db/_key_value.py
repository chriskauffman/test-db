import logging

from sqlobject import DateTimeCol, SQLObject, StringCol  # type: ignore
import sqlobject.sqlbuilder  # type: ignore


logger = logging.getLogger(__name__)


class KeyValue(SQLObject):
    """Basic key value storage

    Designed for simple data storage needs such as database or app configuration

    Attributes:
        key (StringCol):
        value (StringCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    key: StringCol = StringCol(alternateID=True, unique=True)
    value: StringCol = StringCol(default=None)

    createdAt: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )
    updatedAt: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )
