import logging

from sqlobject import DateTimeCol, ForeignKey, DatabaseIndex, SQLObject, StringCol  # type: ignore

logger = logging.getLogger(__name__)


class JobKeyValue(SQLObject):
    """Job Key/Value SQLObject

    Attributes:
        job (ForeignKey): entity who owns the key/value pair
        key (StringCol): key name
        value (StringCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        jobKeyIndex (DatabaseIndex): unique index on (key, person)
    """

    job: ForeignKey = ForeignKey("Job", cascade=True, notNone=True)
    key: StringCol = StringCol(dbName="key_name", notNone=True)
    value: StringCol = StringCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    jobKeyIndex: DatabaseIndex = DatabaseIndex(job, key, unique=True)

    @property
    def ownerID(self):
        return self.job.gID

    @property
    def visualID(self):
        return f"{self.ownerID}, {self.key}"
