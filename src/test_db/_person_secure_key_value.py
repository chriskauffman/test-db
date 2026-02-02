import logging

from sqlobject import DateTimeCol, ForeignKey, DatabaseIndex, SQLObject, StringCol  # type: ignore

from test_db._encrypted_pickle_col import EncryptedPickleCol

logger = logging.getLogger(__name__)


class PersonSecureKeyValue(SQLObject):
    """Personal KeyValueSecure SQLObject

    Attributes:
        person (ForeignKey): entity who owns the key/value pair
        key (StringCol): key name
        value (EncryptedPickleCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        personKeyIndex (DatabaseIndex): unique index on (key, person)
    """

    person: ForeignKey = ForeignKey("Person", cascade=True, notNone=True)
    key: StringCol = StringCol(dbName="key_name", notNone=True)
    value: EncryptedPickleCol = EncryptedPickleCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    personKeyIndex: DatabaseIndex = DatabaseIndex(person, key, unique=True)

    @property
    def ownerID(self):
        return self.person.gID

    @property
    def visualID(self):
        return f"{self.person.gID}, {self.key}"
