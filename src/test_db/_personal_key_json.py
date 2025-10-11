import logging

from sqlobject import DatabaseIndex, ForeignKey, JSONCol, StringCol  # type: ignore

from test_db._base_sqlobject import BaseSQLObject


logger = logging.getLogger(__name__)


class PersonalKeyJson(BaseSQLObject):
    """PersonalKeyJson SQLObject

    Attributes:
        key (StringCol):
        value (JSONCol):
        person (ForeignKey): the DB ID of the owner of the bank account
        keyPersonIndex (DatabaseIndex):
    """

    key: StringCol = StringCol()
    value: JSONCol = JSONCol(default=None)
    person: ForeignKey = ForeignKey("Person", cascade=True)

    keyPersonIndex: DatabaseIndex = DatabaseIndex(key, person, unique=True)
