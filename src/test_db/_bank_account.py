import logging
import random

import faker
from faker.providers.bank import Provider as BankProvider
from sqlobject import DateTimeCol, JSONCol, RelatedJoin, StringCol  # type: ignore
import sqlobject.sqlbuilder  # type: ignore

from test_db._gid_sqlobject import GID_SQLObject


logger = logging.getLogger(__name__)


class TestDBBankAccount(BankProvider):
    """Faker Bank Account Provider for Testing"""

    # account numbers usually 8 - 12 digits
    _account_number_range = (10**7, 10**12 - 1)

    # python faker doesn't seem to provide a bank account number
    def bank_account_number(self) -> str:
        """Generates fake integers-only bank account number"""
        return str(random.randint(*self._account_number_range))


fake = faker.Faker()
fake.add_provider(TestDBBankAccount)


class BankAccount(GID_SQLObject):
    """BankAccount SQLObject

    Attributes:
        gID (StringCol): global ID for the object
        attributes (JSONCol): JSON attributes for the object
                              Note: the DB isn't updated until the object is saved
                                    (no DB updates when individual fields are changed)
        description (StringCol): description of the object
        routingNumber (StringCol): bank routing number (generated when not provided)
        accountNumber (StringCol): bank account (generated when not provided)
        organizations (RelatedJoin): list of employers related to the bank account
        people (RelatedJoin): list of people related to the bank account
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    _gIDPrefix: str = "ba"

    gID: StringCol = StringCol(alternateID=True, default=None)
    attributes: JSONCol = JSONCol(default=None)
    description: StringCol = StringCol(default=None)

    routingNumber: StringCol = StringCol(default=fake.aba)
    accountNumber: StringCol = StringCol(default=fake.bank_account_number)

    organizations: RelatedJoin = RelatedJoin("Organization")
    people: RelatedJoin = RelatedJoin("Person")

    # Note: A unique index on routingNumber and accountNumber is not used because
    # many test environments have a limited set of accounts that may be used,
    # requiring duplicate entries

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
