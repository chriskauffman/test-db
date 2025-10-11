import logging

from sqlobject import DatabaseIndex, ForeignKey, StringCol  # type: ignore

from test_db._base_sqlobject import BaseSQLObject


logger = logging.getLogger(__name__)


class PersonalKeyValue(BaseSQLObject):
    """KeyValue SQLObject

    Attributes:
        key (StringCol):
        value (StringCol):
        person (ForeignKey): the DB ID of the owner of the bank account
        keyPersonIndex (DatabaseIndex):
    """

    key: StringCol = StringCol()
    value: StringCol = StringCol(default=None)
    person: ForeignKey = ForeignKey("Person", cascade=True)

    keyPersonIndex: DatabaseIndex = DatabaseIndex(key, person, unique=True)
