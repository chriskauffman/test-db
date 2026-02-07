import logging

import faker
from sqlobject import DateTimeCol, ForeignKey, SQLObject, StringCol  # type: ignore
from typeid import TypeID

from test_db._type_id_col import TypeIDCol
from test_db._gid import validGID


logger = logging.getLogger(__name__)


fake = faker.Faker()


class PersonAddress(SQLObject):
    """Basic address for use with other objects

    Attributes:
        person (ForeignKey): person this address belongs to
        gID (TypeIDCol): global ID for the object
        description (StringCol): name of the object
        street (StringCol): the person's residence street
        locality (StringCol): the person's residence city
        region (StringCol): the person's residence state
        postalCode (StringCol): the person's residence zip
        country (StringCol): the person's residence country, defaults to US
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    _gIDPrefix: str = "addr"

    person: ForeignKey = ForeignKey("Person", cascade=True, notNone=True)
    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)
    description: StringCol = StringCol(default=None)
    street: StringCol = StringCol(default=fake.street_address)
    locality: StringCol = StringCol(default=fake.city)
    region: StringCol = StringCol(default=fake.state_abbr)
    postalCode: StringCol = StringCol(default=fake.postcode)
    country: StringCol = StringCol(default="US")

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    @property
    def ownerID(self):
        return self.person.gID

    @property
    def visualID(self):
        return f"{self.gID}, {self.region}, {self.postalCode}, {self.ownerID}"

    def _set_gID(self, value):
        if value:
            if validGID(value, self._gIDPrefix):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(TypeID(self._gIDPrefix))
