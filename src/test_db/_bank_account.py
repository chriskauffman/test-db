import logging
import random

import faker
from faker.providers.bank import Provider as BankProvider
from sqlobject import DateTimeCol, JSONCol, RelatedJoin, SQLObject, StringCol  # type: ignore
from typeid import TypeID

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
        attributes (JSONCol): JSON attributes for the object
                              Note: the DB isn't updated until the object is saved
                                    (no DB updates when individual fields are changed)
        name (StringCol): name of the object
        routingNumber (StringCol): bank routing number (generated when not provided)
        accountNumber (StringCol): bank account (generated when not provided)
        entities (RelatedJoin): list of people related to the bank account
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    _autoCreateDependents: bool = True
    _gIDPrefix: str = "ba"

    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)
    attributes: JSONCol = JSONCol(default=None)
    name: StringCol = StringCol(default=None)

    # Note: A unique index on routingNumber and accountNumber is not used because
    # many test environments have a limited set of accounts that may be used,
    # requiring duplicate entries

    routingNumber: StringCol = StringCol(default=fake.aba)
    accountNumber: StringCol = StringCol(default=fake.bank_account_number)

    entities: RelatedJoin = RelatedJoin("Entity")

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    def _set_gID(self, value):
        if value:
            if validGID(value, self._gIDPrefix):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(TypeID(self._gIDPrefix))
