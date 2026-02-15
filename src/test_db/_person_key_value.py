import logging

from sqlobject import (  # type: ignore
    events,
    DateTimeCol,
    ForeignKey,
    DatabaseIndex,
    SQLObject,
    StringCol,
)

from test_db._listeners import handleRowCreateSignal, handleRowUpdateSignal

logger = logging.getLogger(__name__)


class PersonKeyValue(SQLObject):
    """Job Key/Value SQLObject

    Attributes:
        person (ForeignKey): entity who owns the key/value pair
        key (StringCol): key name
        value (StringCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        personKeyIndex (DatabaseIndex): unique index on (key, person)
    """

    person: ForeignKey = ForeignKey("Person", cascade=True, notNone=True)
    key: StringCol = StringCol(dbName="key_name", notNone=True)
    value: StringCol = StringCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    personKeyIndex: DatabaseIndex = DatabaseIndex(person, key, unique=True)

    @property
    def ownerID(self):
        return self.person.gID

    @property
    def visualID(self):
        return f"{self.ownerID}, {self.key}"


events.listen(handleRowCreateSignal, PersonKeyValue, events.RowCreateSignal)
events.listen(handleRowUpdateSignal, PersonKeyValue, events.RowUpdateSignal)
