from sqlobject import DateTimeCol, ForeignKey, DatabaseIndex, SQLObject, StringCol  # type: ignore

from test_db._encrypted_pickle_col import EncryptedPickleCol


class EntitySecureKeyValue(SQLObject):
    """Personal KeyValueSecure SQLObject

    Attributes:
        entity (ForeignKey): entity who owns the key/value pair
        key (StringCol): key name
        value (EncryptedPickleCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        entityKeyIndex (DatabaseIndex): unique index on (key, person)
    """

    entity: ForeignKey = ForeignKey("Entity", cascade=True, notNone=True)
    key: StringCol = StringCol(notNone=True)
    value: EncryptedPickleCol = EncryptedPickleCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    entityKeyIndex: DatabaseIndex = DatabaseIndex(entity, key, unique=True)
