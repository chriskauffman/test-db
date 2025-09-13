import logging
import random

import faker
from faker.providers import BaseProvider
from sqlobject import DatabaseIndex, ForeignKey, StringCol  # type: ignore

from ._test_db_sqlobject import TestDBSQLObject


logger = logging.getLogger(__name__)


class FakeBankAccount(BaseProvider):
    """Faker Bank Account Provider for Testing"""

    account_number_range = (10**7, 10**12 - 1)
    routing_number_range = (10**8, 10**9 - 1)

    def bank_account_routing_number(self) -> str:
        """Generates fake bank account routing number"""
        # routing numbers are 9 digits long
        return str(
            random.randint(self.routing_number_range[0], self.routing_number_range[1])
        ).zfill(9)

    def bank_account_number(self) -> str:
        """Generates fake bank account number"""
        # account numbers usually 8 - 12 digits
        return str(
            random.randint(self.account_number_range[0], self.account_number_range[1])
        )


fake = faker.Faker()
fake.add_provider(FakeBankAccount)


class PersonalBankAccount(TestDBSQLObject):
    """PersonalBankAccount SQLObject

    Attributes:
        name (StringCol): the name of the bank account, must be unique for this user
        routing_number (StringCol): bank routing number (generated when not provided)
        account_number (StringCol): bank account (generated when not provided)
        person (ForeignKey): the DB ID of the owner of the bank account
        name_person_index (DatabaseIndex):
    """

    _gid_prefix: str = "pb"

    name: StringCol = StringCol()
    routing_number: StringCol = StringCol(
        default=fake.bank_account_routing_number
    )  # fake.aba
    account_number: StringCol = StringCol(default=fake.bank_account_number)
    person: ForeignKey = ForeignKey("Person", cascade=True)

    name_person_index: DatabaseIndex = DatabaseIndex(name, person, unique=True)
