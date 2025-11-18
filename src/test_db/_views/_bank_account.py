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

    _user_inputs_required: bool = True

    @classmethod
    def add(self, owner: Union[Organization, Person, None] = None) -> BankAccount:
        """Add a bank account"""
        bank_account = BankAccount()
        if owner:
            bank_account.addPerson(owner)
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

    def edit(self):
        """Edit the bank account"""
        self._bank_account.description = self._get_str_input(
            "Description", self._bank_account.description
        )
        self._bank_account.accountNumber = self._get_str_input(
            "Account Number", self._bank_account.accountNumber
        )
        self._bank_account.routingNumber = self._get_str_input(
            "Routing Number", self._bank_account.routingNumber
        )

    def view(self):
        """Display brief details of the debit card"""
        print(
            f"{self._bank_account.gID}, {self._bank_account.routingNumber}, {self._bank_account.accountNumber}, {str(self._bank_account.description)[:10]}"
        )
