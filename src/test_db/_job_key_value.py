import logging

from sqlobject import DateTimeCol, ForeignKey, DatabaseIndex, SQLObject, StringCol  # type: ignore

logger = logging.getLogger(__name__)


class JobKeyValue(SQLObject):
    """Job Key/Value SQLObject

    Attributes:
        job (ForeignKey): entity who owns the itemKey/value pair
        itemKey (StringCol): itemKey name
        itemValue (StringCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        jobKeyIndex (DatabaseIndex): unique index on (itemKey, person)
    """

    job: ForeignKey = ForeignKey("Job", cascade=True, notNone=True)
    itemKey: StringCol = StringCol(notNone=True)
    itemValue: StringCol = StringCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    jobKeyIndex: DatabaseIndex = DatabaseIndex(job, itemKey, unique=True)
