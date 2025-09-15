import logging

from sqlobject import DatabaseIndex, ForeignKey, StringCol  # type: ignore

from ._test_db_sqlobject import FullSQLObject


logger = logging.getLogger(__name__)


class AppSettings(FullSQLObject):
    """AppSettings SQLObject

    Attributes:
        name (StringCol): the name of the settings
    """

    _gIDPrefix: str = "set"

    name: StringCol = StringCol(alternateID=True)


class PersonalAppSettings(FullSQLObject):
    """PersonalAppSettings SQLObject

    Attributes:
        name (StringCol): the name of the settings, must be unique for this user
        person (ForeignKey): the DB ID of the owner of the bank account
        namePersonIndex (DatabaseIndex):
    """

    _gIDPrefix: str = "pas"

    name: StringCol = StringCol()
    person: ForeignKey = ForeignKey("Person", cascade=True)

    namePersonIndex: DatabaseIndex = DatabaseIndex(name, person, unique=True)
