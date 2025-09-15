import logging

import faker

from sqlobject import DatabaseIndex, ForeignKey, StringCol  # type: ignore

from ._test_db_sqlobject import TestDBSQLObject


logger = logging.getLogger(__name__)


fake = faker.Faker()


class PersonalAddress(TestDBSQLObject):
    """PersonalBankAccount SQLObject

    Attributes:
        name (StringCol): the name of the bank account, must be unique for this user
        street (StringCol): the person's residence street
        locality (StringCol): the person's residence city
        region (StringCol): the person's residence state
        postalCode (StringCol): the person's residence zip
        country (StringCol): the person's residence country
        person (ForeignKey): the DB ID of the owner of the bank account
        namePersonIndex (DatabaseIndex):
    """

    _gIDPrefix: str = "pa"

    name: StringCol = StringCol()
    street: StringCol = StringCol(default=fake.street_address)
    locality: StringCol = StringCol(default=fake.city)
    region: StringCol = StringCol(length=2, default=fake.state_abbr)
    postalCode: StringCol = StringCol(length=5, default=fake.postcode)
    country: StringCol = StringCol(length=2, default="US")

    person: ForeignKey = ForeignKey("Person", cascade=True)

    namePersonIndex: DatabaseIndex = DatabaseIndex(name, person, unique=True)
