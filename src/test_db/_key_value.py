import logging

from sqlobject import DateTimeCol, SQLObject, StringCol  # type: ignore


logger = logging.getLogger(__name__)


class KeyValue(SQLObject):
    """Basic key value storage

    Designed for simple data storage needs such as database or app configuration

    Attributes:
        itemKey (StringCol):
        itemValue (StringCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    itemKey: StringCol = StringCol(alternateID=True, unique=True)
    itemValue: StringCol = StringCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()
