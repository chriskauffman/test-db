from sqlobject import DateTimeCol, ForeignKey, DatabaseIndex, SQLObject, StringCol  # type: ignore


class EntityKeyValue(SQLObject):
    """Personal KeyValueSecure SQLObject

    Attributes:
        entity (ForeignKey): entity who owns the key/value pair
        key (StringCol): key name
        value (StringCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        entityKeyIndex (DatabaseIndex): unique index on (key, person)
    """

    entity: ForeignKey = ForeignKey("Entity", cascade=True, notNone=True)
    key: StringCol = StringCol(notNone=True)
    value: StringCol = StringCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    entityKeyIndex: DatabaseIndex = DatabaseIndex(entity, key, unique=True)
