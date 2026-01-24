import logging

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import List, Union

from sqlobject import SQLObject  # type: ignore
from sqlobject.dberrors import DuplicateEntryError  # type: ignore

from test_db import OrganizationBankAccount, PersonBankAccount
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class BankAccountView(BaseView):
    """Debit card views

    Args:
        bank_account (Union[OrganizationBankAccount, PersonBankAccount]): The bank account to view
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def list(
        cls,
        bank_accounts: Union[
            List[OrganizationBankAccount], List[PersonBankAccount], SQLObject.select
        ],
        **kwargs,
    ):
        """List all bank accounts"""
        for bank_account in bank_accounts:
            BankAccountView(bank_account).view()

    def __init__(
        self, bank_account: Union[OrganizationBankAccount, PersonBankAccount], **kwargs
    ):
        super().__init__(**kwargs)
        self._bank_account = bank_account

    def delete(self, interactive: bool = True):
        """Delete the bank account"""
        if (
            interactive
            and input(f"Delete {self._bank_account.visualID}? [y/n] ").strip().lower()
            != "y"
        ):
            return
        self._bank_account.destroySelf()

    def edit(self):
        """Edit the bank account"""
        while True:
            try:
                self._bank_account.gID = self._getTypeIDInput(
                    "gID", self._bank_account.gID
                )
                break
            except DuplicateEntryError:
                print("gID already exists. Please enter a different gID.")
            except ValueError:
                print("Invalid gID. Check prefix and suffix. Please try again.")

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
        """Display brief details of the bank account"""
        print(f"{self._bank_account.visualID}")
