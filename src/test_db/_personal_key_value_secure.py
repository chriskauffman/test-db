from sqlobject import ForeignKey, DatabaseIndex, StringCol  # type: ignore

from test_db._base_sqlobject import BaseSQLObject
from test_db._encrypted_pickle_col import EncryptedPickleCol


class PersonalKeyValueSecure(BaseSQLObject):
    """Personal KeyValueSecure SQLObject

    Attributes:
        key (StringCol): key name
        person (ForeignKey): person who owns the key/value pair
        value (EncryptedPickleCol):
        keyPersonIndex (DatabaseIndex): unique index on (key, person)
    """

    key: StringCol = StringCol()
    person: ForeignKey = ForeignKey("Person", cascade=True, notNone=True)
    value: EncryptedPickleCol = EncryptedPickleCol(default=None)

    keyPersonIndex: DatabaseIndex = DatabaseIndex(key, person, unique=True)
