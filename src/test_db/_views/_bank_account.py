import logging

from typing_extensions import List, Union

from sqlobject import SQLObject  # type: ignore

from test_db import BankAccount, Organization, Person
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class BankAccountView(BaseView):
    """Debit card views

    Args:
        bank_account (BankAccount): The bank account to view
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def add(
        cls,
        entity: Union[Organization, Person, None] = None,
        interactive: bool = True,
        **kwargs,
    ) -> BankAccount:
        """Add a bank account"""
        bank_account = BankAccount(**kwargs)
        if entity:
            bank_account.addEntity(entity)
        if interactive:
            BankAccountView(bank_account).edit()
        print(bank_account.gID)
        return bank_account

    @classmethod
    def list(
        cls, bank_accounts: Union[List[BankAccount], SQLObject.select, None] = None
    ):
        """List all people"""
        if bank_accounts is None:
            bank_accounts = BankAccount.select()
        for bank_account in bank_accounts:
            BankAccountView(bank_account).view()

    def __init__(self, bank_account: BankAccount, **kwargs):
        super().__init__(**kwargs)
        self._bank_account = bank_account

    def delete(self, interactive: bool = True):
        """Delete the card"""
        if (
            interactive
            and input(f"Delete {self._bank_account.visualID}? [y/n] ").strip().lower()
            != "y"
        ):
            return
        self._bank_account.destroySelf()

    def edit(self):
        """Edit the bank account"""
        self._bank_account.description = self._getStrInput(
            "Description", self._bank_account.description, acceptNull=True
        )
        self._bank_account.accountNumber = self._getStrInput(
            "Account Number", self._bank_account.accountNumber, numeric=True
        )
        self._bank_account.routingNumber = self._getStrInput(
            "Routing Number", self._bank_account.routingNumber, numeric=True
        )

    def view(self):
        """Display brief details of the debit card"""
        print(f"{self._bank_account.visualID}")
