import logging
import random

import faker
from faker.providers.bank import Provider as BankProvider
from sqlobject import (  # type: ignore
    connectionForURI,
    DatabaseIndex,
    DateTimeCol,
    JSONCol,
    RelatedJoin,
    SQLObject,
    StringCol,
)
from typeid import TypeID
from typing_extensions import Optional, Self

from test_db._type_id_col import TypeIDCol
from test_db._gid import validGID


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


class BankAccount(SQLObject):
    """BankAccount SQLObject

    Attributes:
        gID (TypeIDCol): global ID for the object
        attributes (JSONCol): JSON attributes for the object. **Note** - The DB
                              isn't updated until the object is saved (no DB updates
                              when individual fields are changed)
        description (StringCol): name of the object
        routingNumber (StringCol): bank routing number (generated when not provided)
        accountNumber (StringCol): bank account (generated when not provided)
        entities (RelatedJoin): list of people related to the bank account
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        routingNumberAccountNumberIndex (DatabaseIndex):
    """

    _autoCreateDependents: bool = True
    _gIDPrefix: str = "ba"

    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)
    attributes: JSONCol = JSONCol(default=None)
    description: StringCol = StringCol(default=None)

    routingNumber: StringCol = StringCol(default=fake.aba)
    accountNumber: StringCol = StringCol(default=fake.bank_account_number)

    entities: RelatedJoin = RelatedJoin(
        "Entity", intermediateTable="bank_account_entity", createRelatedTable=False
    )

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    routingNumberAccountNumberIndex: DatabaseIndex = DatabaseIndex(
        routingNumber, accountNumber, unique=True
    )

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
