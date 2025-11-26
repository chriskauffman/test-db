from sqlobject import DateTimeCol, ForeignKey, DatabaseIndex, SQLObject, StringCol  # type: ignore

from test_db._encrypted_pickle_col import EncryptedPickleCol


class PersonalKeyValueSecure(SQLObject):
    """Personal KeyValueSecure SQLObject

    Attributes:
        key (StringCol): key name
        person (ForeignKey): person who owns the key/value pair
        value (EncryptedPickleCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        keyPersonIndex (DatabaseIndex): unique index on (key, person)
    """

    key: StringCol = StringCol(notNone=True)
    person: ForeignKey = ForeignKey("Person", cascade=True, notNone=True)
    value: EncryptedPickleCol = EncryptedPickleCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    keyPersonIndex: DatabaseIndex = DatabaseIndex(key, person, unique=True)
