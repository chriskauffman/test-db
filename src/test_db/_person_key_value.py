import logging

from sqlobject import DateTimeCol, ForeignKey, DatabaseIndex, SQLObject, StringCol  # type: ignore

logger = logging.getLogger(__name__)


class PersonKeyValue(SQLObject):
    """Job Key/Value SQLObject

    Attributes:
        person (ForeignKey): entity who owns the itemKey/value pair
        itemKey (StringCol): itemKey name
        itemValue (StringCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        personKeyIndex (DatabaseIndex): unique index on (itemKey, person)
    """

    person: ForeignKey = ForeignKey("Person", cascade=True, notNone=True)
    itemKey: StringCol = StringCol(notNone=True)
    itemValue: StringCol = StringCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    personKeyIndex: DatabaseIndex = DatabaseIndex(person, itemKey, unique=True)

    @property
    def ownerID(self):
        return self.person.gID

    @property
    def visualID(self):
        return f"{self.person.gID}, {self.itemKey}"
