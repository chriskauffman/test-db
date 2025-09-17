import logging
import random

import faker
from faker.providers import BaseProvider
from sqlobject import DatabaseIndex, ForeignKey, StringCol  # type: ignore

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


class PersonalBankAccount(FullSQLObject):
    """PersonalBankAccount SQLObject

    Attributes:
        name (StringCol): the name of the bank account, must be unique for this user
        routingNumber (StringCol): bank routing number (generated when not provided)
        accountNumber (StringCol): bank account (generated when not provided)
        person (ForeignKey): the DB ID of the owner of the bank account
        namePersonIndex (DatabaseIndex):
    """

    _gIDPrefix: str = "pb"

    name: StringCol = StringCol()
    routingNumber: StringCol = StringCol(default=fake.aba)
    accountNumber: StringCol = StringCol(default=fake.bank_account_number)
    person: ForeignKey = ForeignKey("Person", cascade=True)

    namePersonIndex: DatabaseIndex = DatabaseIndex(name, person, unique=True)
