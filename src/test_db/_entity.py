import logging

import faker

from sqlobject import JSONCol, RelatedJoin, SQLRelatedJoin, StringCol  # type: ignore
from sqlobject.inheritance import InheritableSQLObject  # type: ignore

from typing_extensions import Optional

from test_db._address import Address
from test_db._bank_account import BankAccount
from test_db._debit_card import DebitCard

fake = faker.Faker()
logger = logging.getLogger(__name__)


class Entity(InheritableSQLObject):
    """Base Entity SQLObject

    This is a base class for all entities in the test database.
    It can be extended to include common attributes or methods
    that should be shared across all entity types.

    Attributes:
        attributes (JSONCol): JSON attributes for the entity
                              Note: the DB isn't updated until the object is saved
                                    (no DB updates when individual fields are changed)
        description (StringCol): description of the entity
        phoneNumber (StringCol): the entity's phone number
        addresses (RelatedJoin): list of addresses related to the entity
        addressesSelect (SQLRelatedJoin):
        bankAccounts (RelatedJoin): list of bank accounts related to the entity
        bankAccountsSelect (SQLRelatedJoin):
        debitCards (RelatedJoin): list of debit cards related to the entity
        debitCardsSelect (SQLRelatedJoin):
    """

    _autoCreateDependents: bool = True

    attributes: JSONCol = JSONCol(default=None)
    description: StringCol = StringCol(default=None)
    phoneNumber: StringCol = StringCol(default=fake.basic_phone_number)

    addresses: RelatedJoin = RelatedJoin("Address")
    addressesSelect: SQLRelatedJoin = SQLRelatedJoin("Address")
    bankAccounts: RelatedJoin = RelatedJoin("BankAccount")
    bankAccountsSelect: SQLRelatedJoin = SQLRelatedJoin("BankAccount")
    debitCards: RelatedJoin = RelatedJoin("DebitCard")
    debitCardsSelect: SQLRelatedJoin = SQLRelatedJoin("DebitCard")

    @property
    def defaultAddress(self) -> Optional[Address]:
        return self.getAddressByName("default")

    @property
    def defaultBankAccount(self) -> Optional[BankAccount]:
        return self.getBankAccountByName("default")

    @property
    def defaultDebitCard(self) -> Optional[DebitCard]:
        return self.getDebitCardByName("default")

    def getAddressByName(self, name: str, **kwargs) -> Optional[Address]:
        """Return the default address for the person

        Args:
            name (str): name of the item
            **kwargs:

        Returns:
            Optional[Address]: the default address or None
        """
        address = next(
            (address for address in self.addresses if address.name == name),
            None,
        )
        if address:
            return address
        else:
            if self._autoCreateDependents:
                address = Address(
                    connection=self._connection,
                    name=name,
                    **kwargs,
                )
                self.addAddress(address)
                return address
        return None

    def getBankAccountByName(self, name: str, **kwargs) -> Optional[BankAccount]:
        """Find and create bank account

        Args:
            name (str): name of the item
            **kwargs:

        Returns:
            Optional[BankAccount]:
        """
        bank_account = next(
            (
                bank_account
                for bank_account in self.bankAccounts
                if bank_account.name == name
            ),
            None,
        )
        if bank_account:
            return bank_account
        else:
            if self._autoCreateDependents:
                bank_account = BankAccount(
                    connection=self._connection,
                    name=name,
                    **kwargs,
                )
                self.addBankAccount(bank_account)
                return bank_account
        return None

    def getDebitCardByName(self, name: str, **kwargs) -> Optional[DebitCard]:
        """Find and create debit card

        Args:
            name (str): name of the item
            **kwargs:

        Returns:
            Optional[DebitCard]:
        """
        debit_card = next(
            (debit_card for debit_card in self.debitCards if debit_card.name == name),
            None,
        )
        if debit_card:
            return debit_card
        else:
            if self._autoCreateDependents:
                debit_card = DebitCard(
                    connection=self._connection,
                    name=name,
                    **kwargs,
                )
                self.addDebitCard(debit_card)
                return debit_card
        return None
