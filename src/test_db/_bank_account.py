import logging
import random

import faker
from faker.providers import BaseProvider
from sqlobject import RelatedJoin, StringCol  # type: ignore

from test_db._full_sqlobject import FullSQLObject


logger = logging.getLogger(__name__)


class FakeBankAccount(BaseProvider):
    """Faker Bank Account Provider for Testing"""

    _account_number_range = (10**7, 10**12 - 1)

    # python faker doesn't seem to provide a bank account number
    def bank_account_number(self) -> str:
        """Generates fake bank account number"""
        # account numbers usually 8 - 12 digits
        return str(random.randint(*self._account_number_range))


fake = faker.Faker()
fake.add_provider(FakeBankAccount)


class BankAccount(FullSQLObject):
    """BankAccount SQLObject

    Attributes:
        routingNumber (StringCol): bank routing number (generated when not provided)
        accountNumber (StringCol): bank account (generated when not provided)
        organizations (RelatedJoin): list of employers related to the bank account
        people (RelatedJoin): list of people related to the bank account
    """

    _gIDPrefix: str = "ba"

    routingNumber: StringCol = StringCol(default=fake.aba)
    accountNumber: StringCol = StringCol(default=fake.bank_account_number)

    organizations: RelatedJoin = RelatedJoin("Organization")
    people: RelatedJoin = RelatedJoin("Person")

    # Note: A unique index on routingNumber and accountNumber is not used because
    # many test environments have a limited set of accounts that may be used,
    # requiring duplicate entries
