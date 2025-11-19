from sqlobject import ForeignKey, DatabaseIndex, StringCol  # type: ignore
from sqlobject import DateTimeCol, SQLObject  # type: ignore
import sqlobject.sqlbuilder  # type: ignore

from test_db._encrypted_pickle_col import EncryptedPickleCol


class PersonalKeyValueSecure(SQLObject):
    """Personal KeyValueSecure SQLObject

    Attributes:
        key (StringCol): key name
        person (ForeignKey): person who owns the key/value pair
        value (EncryptedPickleCol):
        keyPersonIndex (DatabaseIndex): unique index on (key, person)
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    key: StringCol = StringCol()
    person: ForeignKey = ForeignKey("Person", cascade=True, notNone=True)
    value: EncryptedPickleCol = EncryptedPickleCol(default=None)

    keyPersonIndex: DatabaseIndex = DatabaseIndex(key, person, unique=True)

    createdAt: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )
    updatedAt: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )
