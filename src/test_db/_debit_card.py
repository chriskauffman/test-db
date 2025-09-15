import datetime
import logging
import random

import faker
from faker.providers import BaseProvider

from sqlobject import DatabaseIndex, ForeignKey, StringCol  # type: ignore

from ._test_db_sqlobject import FullSQLObject


logger = logging.getLogger(__name__)


VALID_DEBIT_CARD_YEAR = datetime.datetime.today().year + 1


class FakeDebitCard(BaseProvider):
    """Faker Debit Card Provider for Testing"""

    card_number_range = (10**15, 10**16 - 1)
    cvv_range = (100, 999)
    expiration_month_range = (1, 12)
    expiration_year_range = (VALID_DEBIT_CARD_YEAR, VALID_DEBIT_CARD_YEAR + 10)

    def debit_card_cvv(self) -> str:
        """Generates fake debit card cvv"""
        return str(random.randint(self.cvv_range[0], self.cvv_range[1])).zfill(3)

    def debit_card_expiration_month(self) -> str:
        """Generates fake debit card expiration month"""
        return str(
            random.randint(
                self.expiration_month_range[0], self.expiration_month_range[1]
            )
        ).zfill(2)

    def debit_card_expiration_year(self) -> str:
        """Generates fake debit card expiration year"""
        return str(
            random.randint(self.expiration_year_range[0], self.expiration_year_range[1])
        ).zfill(4)

    def debit_card_number(self) -> str:
        """Generates fake debit card cvv"""
        return str(
            random.randint(self.card_number_range[0], self.card_number_range[1])
        ).zfill(16)

    def debit_card_token(self) -> str:
        """Generates fake debit card token"""
        return str(random.getrandbits(512))


fake = faker.Faker()
fake.add_provider(FakeDebitCard)


class PersonalDebitCard(FullSQLObject):
    """PersonalDebitCard SQLObject

    Attributes:
        name (StringCol): the name of the debit card, must be unique for this user
        cardNumber (StringCol): debit card number (generated when not provided)
        cvv (StringCol): debit card security code (generated when not provided)
        expirationMonth (StringCol): two digit month (generated when not provided)
        expirationYear (StringCol): four digit year (generated when not provided)
        person (ForeignKey): the DB ID of the owner of the bank account
        namePersonIndex (DatabaseIndex):
    """

    _gIDPrefix: str = "pdc"

    name: StringCol = StringCol()
    cardNumber: StringCol = StringCol(length=16, default=fake.debit_card_number)
    cvv: StringCol = StringCol(length=3, default=fake.debit_card_cvv)
    expirationMonth: StringCol = StringCol(
        length=2, default=fake.debit_card_expiration_month
    )
    expirationYear: StringCol = StringCol(
        length=4, default=fake.debit_card_expiration_year
    )
    person: ForeignKey = ForeignKey("Person", cascade=True)

    namePersonIndex: DatabaseIndex = DatabaseIndex(name, person, unique=True)
