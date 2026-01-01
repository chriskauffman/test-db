import logging

from sqlobject import DateTimeCol, ForeignKey, DatabaseIndex, SQLObject, StringCol  # type: ignore

from test_db._encrypted_pickle_col import EncryptedPickleCol

logger = logging.getLogger(__name__)


class EntitySecureKeyValue(SQLObject):
    """Personal KeyValueSecure SQLObject

    Attributes:
        entity (ForeignKey): entity who owns the itemKey/value pair
        itemKey (StringCol): itemKey name
        itemValue (EncryptedPickleCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        entityKeyIndex (DatabaseIndex): unique index on (itemKey, person)
    """

    entity: ForeignKey = ForeignKey("Entity", cascade=True, notNone=True)
    itemKey: StringCol = StringCol(notNone=True)
    itemValue: EncryptedPickleCol = EncryptedPickleCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    entityKeyIndex: DatabaseIndex = DatabaseIndex(entity, itemKey, unique=True)
