import logging

from sqlobject import DateTimeCol, ForeignKey, DatabaseIndex, SQLObject, StringCol  # type: ignore

logger = logging.getLogger(__name__)


class OrganizationKeyValue(SQLObject):
    """Organization Key/Value SQLObject

    Attributes:
        organization (ForeignKey): entity who owns the key/value pair
        key (StringCol): key name
        value (StringCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        organizationKeyIndex (DatabaseIndex): unique index on (key, person)
    """

    organization: ForeignKey = ForeignKey("Organization", cascade=True, notNone=True)
    key: StringCol = StringCol(dbName="key_name", notNone=True)
    value: StringCol = StringCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    organizationKeyIndex: DatabaseIndex = DatabaseIndex(organization, key, unique=True)

    @property
    def ownerID(self):
        return self.organization.gID

    @property
    def visualID(self):
        return f"{self.organization.gID}, {self.key}"
