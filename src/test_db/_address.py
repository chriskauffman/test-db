import logging

import faker
from sqlobject import DateTimeCol, JSONCol, RelatedJoin, SQLObject, StringCol  # type: ignore
from typeid import TypeID

from test_db._type_id_col import TypeIDCol
from test_db._gid import validGID


logger = logging.getLogger(__name__)


fake = faker.Faker()


class Address(SQLObject):
    """Basic address for use with other objects

    Attributes:
        gID (TypeIDCol): global ID for the object
        attributes (JSONCol): JSON attributes for the object
                              Note: the DB isn't updated until the object is saved
                                    (no DB updates when individual fields are changed)
        description (StringCol): name of the object
        street (StringCol): the person's residence street
        locality (StringCol): the person's residence city
        region (StringCol): the person's residence state
        postalCode (StringCol): the person's residence zip
        country (StringCol): the person's residence country, defaults to US
        entities (RelatedJoin): Entity that occupies the address
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    _autoCreateDependents: bool = True
    _gIDPrefix: str = "addr"

    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)
    attributes: JSONCol = JSONCol(default=None)
    description: StringCol = StringCol(default=None)

    street: StringCol = StringCol(default=fake.street_address)
    locality: StringCol = StringCol(default=fake.city)
    region: StringCol = StringCol(default=fake.state_abbr)
    postalCode: StringCol = StringCol(default=fake.postcode)
    country: StringCol = StringCol(default="US")

    entities: RelatedJoin = RelatedJoin(
        "Entity", intermediateTable="address_entity", createRelatedTable=False
    )

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    def _set_gID(self, value):
        if value:
            if validGID(value, self._gIDPrefix):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(TypeID(self._gIDPrefix))
