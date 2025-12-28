from sqlobject import DateTimeCol, ForeignKey, DatabaseIndex, SQLObject, StringCol  # type: ignore


class EntityKeyValue(SQLObject):
    """Personal KeyValueSecure SQLObject

    Attributes:
        entity (ForeignKey): entity who owns the itemKey/value pair
        itemKey (StringCol): itemKey name
        itemValue (StringCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        entityKeyIndex (DatabaseIndex): unique index on (itemKey, person)
    """

    entity: ForeignKey = ForeignKey("Entity", cascade=True, notNone=True)
    itemKey: StringCol = StringCol(notNone=True)
    itemValue: StringCol = StringCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    entityKeyIndex: DatabaseIndex = DatabaseIndex(entity, itemKey, unique=True)
