import logging
import random

import faker
from faker.providers.bank import Provider as BankProvider
from sqlobject import (  # type: ignore
    connectionForURI,
    events,
    DatabaseIndex,
    DateTimeCol,
    ForeignKey,
    SQLObject,
    StringCol,
)
from typeid import TypeID

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Optional, Self

from test_db._type_id_col import TypeIDCol
from test_db._gid import validGID
from test_db._listeners import handleRowCreateSignal, handleRowUpdateSignal


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


class PersonBankAccount(SQLObject):
    """BankAccount SQLObject

    Attributes:
        person (ForeignKey): person this bank account belongs to
        gID (TypeIDCol): global ID for the object
        description (StringCol): name of the object
        routingNumber (StringCol): bank routing number (generated when not provided)
        accountNumber (StringCol): bank account (generated when not provided)
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        personRoutingNumberAccountNumberIndex (DatabaseIndex):
    """

    _gIDPrefix: str = "ba"

    person: ForeignKey = ForeignKey("Person", cascade=True, default=None)
    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)
    description: StringCol = StringCol(default=None)
    routingNumber: StringCol = StringCol(default=fake.aba)
    accountNumber: StringCol = StringCol(default=fake.bank_account_number)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    personRoutingNumberAccountNumberIndex: DatabaseIndex = DatabaseIndex(
        person, routingNumber, accountNumber, unique=True
    )

    @property
    def ownerID(self):
        if self.person:
            return self.person.gID
        return None

    @property
    def visualID(self):
        return f"{self.gID}, {self.routingNumber}, ...{self.accountNumber[-4:]}, {self.ownerID}"

    def _set_gID(self, value):
        if value:
            if validGID(value, self._gIDPrefix):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(TypeID(self._gIDPrefix))

    @classmethod
    def byRoutingAndAccountNumber(
        cls,
        routingNumber: str,
        accountNumber: str,
        connection: Optional[connectionForURI] = None,
    ) -> Self:
        """Locate bank accounts using unique index properties

        Simulates SQLObject's automatic by{alternateID} functions

        Args:
            routingNumber (str):
            accountNumber (str):
            connection (Optional[connectionForURI]):

        Returns:
            Self: BankAccount
        """
        return cls.selectBy(
            routingNumber=routingNumber,
            accountNumber=accountNumber,
            connection=connection,
        ).getOne()


events.listen(handleRowCreateSignal, PersonBankAccount, events.RowCreateSignal)
events.listen(handleRowUpdateSignal, PersonBankAccount, events.RowUpdateSignal)
