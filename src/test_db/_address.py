import logging

import faker

from sqlobject import RelatedJoin, StringCol  # type: ignore

from test_db._full_sqlobject import FullSQLObject


logger = logging.getLogger(__name__)


fake = faker.Faker()


class Address(FullSQLObject):
    """Basic address for use with other objects

    Attributes:
        street (StringCol): the person's residence street
        locality (StringCol): the person's residence city
        region (StringCol): the person's residence state
        postalCode (StringCol): the person's residence zip
        country (StringCol): the person's residence country
        organizations (RelatedJoin): list of employers related to the address
        people (RelatedJoin): list of people related to the address
    """

    _gIDPrefix: str = "addr"

    street: StringCol = StringCol(default=fake.street_address)
    locality: StringCol = StringCol(default=fake.city)
    region: StringCol = StringCol(default=fake.state_abbr)
    postalCode: StringCol = StringCol(default=fake.postcode)
    country: StringCol = StringCol(default=fake.country_code)

    organizations: RelatedJoin = RelatedJoin("Organization")
    people: RelatedJoin = RelatedJoin("Person")
