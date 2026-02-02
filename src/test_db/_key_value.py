import logging

from sqlobject import DateTimeCol, SQLObject, StringCol  # type: ignore


logger = logging.getLogger(__name__)


class KeyValue(SQLObject):
    """Basic key value storage

    Designed for simple data storage needs such as database or app configuration

    Attributes:
        key (StringCol):
        value (StringCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        ownerID (str): identifier for the owner of the key/value pair
    """

    key: StringCol = StringCol(alternateID=True, dbName="key_name", unique=True)
    value: StringCol = StringCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    ownerID: str = "global"

    @property
    def visualID(self):
        return f"{self.ownerID}, {self.key}"
