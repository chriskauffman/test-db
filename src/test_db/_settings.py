import logging

from sqlobject import DatabaseIndex, ForeignKey, JSONCol, StringCol  # type: ignore

from test_db._base_sqlobject import BaseSQLObject


logger = logging.getLogger(__name__)


class KeyValue(BaseSQLObject):
    """KeyValue SQLObject

    Attributes:
        key (StringCol):
        value (StringCol):
    """

    key: StringCol = StringCol(alternateID=True, unique=True)
    value: StringCol = StringCol(default=None)


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


class KeyJson(BaseSQLObject):
    """KeyJson SQLObject

    Attributes:
        key (StringCol):
        value (JSONCol):
    """

    key: StringCol = StringCol(alternateID=True, unique=True)
    value: JSONCol = JSONCol(default=None)


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
