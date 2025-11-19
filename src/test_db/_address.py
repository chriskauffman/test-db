import logging

import faker

from sqlobject import DateTimeCol, JSONCol, RelatedJoin, StringCol  # type: ignore
import sqlobject.sqlbuilder  # type: ignore

from test_db._full_sqlobject import FullSQLObject


logger = logging.getLogger(__name__)


fake = faker.Faker()


class Address(FullSQLObject):
    """Basic address for use with other objects

    Attributes:
        gID (StringCol): global ID for the object
        attributes (JSONCol): JSON attributes for the object
                              Note: the DB isn't updated until the object is saved
                                    (no DB updates when individual fields are changed)
        description (StringCol): description of the object
        street (StringCol): the person's residence street
        locality (StringCol): the person's residence city
        region (StringCol): the person's residence state
        postalCode (StringCol): the person's residence zip
        country (StringCol): the person's residence country
        organizations (RelatedJoin): list of employers related to the address
        people (RelatedJoin): list of people related to the address
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    _gIDPrefix: str = "addr"

    gID: StringCol = StringCol(alternateID=True, default=None)
    attributes: JSONCol = JSONCol(default=None)
    description: StringCol = StringCol(default=None)

    street: StringCol = StringCol(default=fake.street_address)
    locality: StringCol = StringCol(default=fake.city)
    region: StringCol = StringCol(default=fake.state_abbr)
    postalCode: StringCol = StringCol(default=fake.postcode)
    country: StringCol = StringCol(default=fake.country_code)

    organizations: RelatedJoin = RelatedJoin("Organization")
    people: RelatedJoin = RelatedJoin("Person")

    createdAt: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )
    updatedAt: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )

    def _set_gID(self, value):
        if value:
            if self.validGID(value):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(self._generateGID())
