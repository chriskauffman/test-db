import logging

from typing_extensions import List, Union

from sqlobject import SQLObject  # type: ignore

from test_db import Organization
from test_db._views._base_view import BaseView
from test_db._views._address import AddressView
from test_db._views._bank_account import BankAccountView
from test_db._views._debit_card import DebitCardView
from test_db._views._job import JobView

logger = logging.getLogger(__name__)


class OrganizationView(BaseView):
    """Organization views

    Args:
        organization (Organization):
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def add(cls) -> Organization:
        """Add a organization"""
        new_org = Organization()
        if BaseView.interactive:
            OrganizationView(new_org).edit()
        print(new_org.gID)
        return new_org

    @classmethod
    def list(
        cls, organizations: Union[List[Organization], SQLObject.select, None] = None
    ):
        """List all organizations"""
        if organizations is None:
            organizations = Organization.select()
        for organization in organizations:
            OrganizationView(organization).view()

    def __init__(self, organization: Organization, **kwargs):
        super().__init__(**kwargs)
        self._organization = organization

    def edit(self):
        """Edit the organization"""
        self._organization.name = self._getStrInput("Name", self._organization.name)
        self._organization.description = self._getStrInput(
            "Description", self._organization.description, acceptNull=True
        )
        self._organization.employerIdentificationNumber = self._getStrInput(
            "EIN", self._organization.employerIdentificationNumber
        )
        self._organization.externalID = self._getStrInput(
            "External ID", self._organization.externalID
        )
        self._organization.phoneNumber = self._getStrInput(
            "Phone Number", self._organization.phoneNumber
        )

    def view(self):
        """Display brief details of the person"""
        print(f"{self._organization.gID}, {self._organization.name}")

    def viewDetails(self):
        """Display brief details of the organization"""
        print(f"\nOrganization ID: {self._organization.gID}")
        print(f"\nName:\t\t{self._organization.name}")
        print(f"Description:\t{self._organization.description}")
        print(f"EIN:\t\t{self._organization.employerIdentificationNumber}")
        print(f"External ID:\t{self._organization.externalID}")
        print(f"Phone Number:\t{self._organization.phoneNumber}")
        print(f"Created At:\t{self._organization.createdAt}")
        print(f"Updated At:\t{self._organization.updatedAt}")
        print("\nAddresses:")
        AddressView.list(self._organization.addresses)
        print("\nBank Accounts:")
        BankAccountView.list(self._organization.bankAccounts)
        print("\nDebit Cards:")
        DebitCardView.list(self._organization.debitCards)
        print("\nJobs:")
        JobView.list(self._organization.jobs)
