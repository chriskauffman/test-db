import logging

from sqlobject import DateTimeCol, ForeignKey, DatabaseIndex, SQLObject, StringCol  # type: ignore

logger = logging.getLogger(__name__)


class OrganizationKeyValue(SQLObject):
    """Organization Key/Value SQLObject

    Attributes:
        organization (ForeignKey): entity who owns the itemKey/value pair
        itemKey (StringCol): itemKey name
        itemValue (StringCol):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        organizationKeyIndex (DatabaseIndex): unique index on (itemKey, person)
    """

    organization: ForeignKey = ForeignKey("Organization", cascade=True, notNone=True)
    itemKey: StringCol = StringCol(notNone=True)
    itemValue: StringCol = StringCol(default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    organizationKeyIndex: DatabaseIndex = DatabaseIndex(
        organization, itemKey, unique=True
    )
