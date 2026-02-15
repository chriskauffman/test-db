import logging

import faker
from sqlobject import (  # type: ignore
    events,
    DateTimeCol,
    ForeignKey,
    SQLObject,
    SQLObjectNotFound,
    StringCol,
)
from typeid import TypeID

from test_db._type_id_col import TypeIDCol
from test_db._gid import validGID
from test_db._listeners import handleRowCreateSignal, handleRowUpdateSignal


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

    person: ForeignKey = ForeignKey("Person", cascade=True, default=None)
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
        if self.person:
            return self.person.gID
        return None

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


def handlePersonAddressRowCreateSignal(instance, kwargs, post_funcs):
    handleRowCreateSignal(instance, kwargs, post_funcs)
    if (
        kwargs.get("street") is None
        and kwargs.get("locality") is None
        and kwargs.get("region") is None
        and kwargs.get("postalCode") is None
    ):
        while True:
            kwargs["street"] = fake.street_address()
            kwargs["locality"] = fake.city()
            kwargs["region"] = fake.state_abbr()
            kwargs["postalCode"] = fake.postcode()
            try:
                if kwargs.get("connection"):
                    PersonAddress.selectBy(
                        street=kwargs["street"],
                        locality=kwargs["locality"],
                        region=kwargs["region"],
                        postalCode=kwargs["postalCode"],
                        connection=kwargs["connection"],
                    ).getOne()
                else:
                    PersonAddress.selectBy(
                        street=kwargs["street"],
                        locality=kwargs["locality"],
                        region=kwargs["region"],
                        postalCode=kwargs["postalCode"],
                    ).getOne()
            except SQLObjectNotFound:
                break


events.listen(handlePersonAddressRowCreateSignal, PersonAddress, events.RowCreateSignal)
events.listen(handleRowUpdateSignal, PersonAddress, events.RowUpdateSignal)
