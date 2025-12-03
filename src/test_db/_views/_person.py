import logging

from typing_extensions import List, Union

from sqlobject import SQLObject  # type: ignore

from test_db import Person
from test_db._views._base_view import BaseView
from test_db._views._address import AddressView
from test_db._views._bank_account import BankAccountView
from test_db._views._debit_card import DebitCardView
from test_db._views._job import JobView
from test_db._views._personal_key_value_secure import PersonalKeyValueSecureView

logger = logging.getLogger(__name__)


class PersonView(BaseView):
    """Person views

    Args:
        person (Person):
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def add(cls, interactive: bool = True) -> Person:
        """Add a person"""
        new_person = Person()
        if interactive:
            PersonView(new_person).edit()
        print(new_person.gID)
        return new_person

    @classmethod
    def list(cls, people: Union[List[Person], SQLObject.select, None] = None):
        """List all people"""
        if people is None:
            people = Person.select()
        for person in people:
            PersonView(person).view()

    def __init__(self, person: Person, **kwargs):
        super().__init__(**kwargs)
        self._person = person

    def edit(self):
        """Edit the person"""
        self._person.firstName = self._getStrInput("First Name", self._person.firstName)
        self._person.lastName = self._getStrInput("Last Name", self._person.lastName)
        self._person.dateOfBirth = self._getDateInput(
            "Date of Birth",
            self._person.dateOfBirth.strftime("%m/%d/%Y"),
        )
        self._person.socialSecurityNumber = self._getStrInput(
            "SSN", self._person.socialSecurityNumber
        )
        self._person.email = self._getStrInput("Email", self._person.email)
        self._person.phoneNumber = self._getStrInput(
            "Phone Number", self._person.phoneNumber
        )

    def view(self):
        """Display brief details of the person"""
        print(
            f"{self._person.gID}, {self._person.firstName} {self._person.lastName}, {self._person.email}"
        )

    def viewDetails(self):
        """Display the person"""
        print(f"\nPerson ID: {self._person.gID}")
        print(f"\nFirst Name:\t{self._person.firstName}")
        print(f"Last Name:\t{self._person.lastName}")
        print(f"Description:\t{self._person.description}")
        print(f"Date of Birth:\t{self._person.dateOfBirth.strftime('%m/%d/%Y')}")
        print(f"SSN:\t\t{self._person.socialSecurityNumber}")
        print(f"Email:\t\t{self._person.email}")
        print(f"Phone Number:\t{self._person.phoneNumber}")
        print(f"Created At:\t{self._person.createdAt}")
        print(f"Updated At:\t{self._person.updatedAt}")
        print("\nAddresses:")
        AddressView.list(self._person.addresses)
        print("\nBank Accounts:")
        BankAccountView.list(self._person.bankAccounts)
        print("\nDebit Cards:")
        DebitCardView.list(self._person.debitCards)
        print("\nJobs:")
        JobView.list(self._person.jobs)
        print("\nPersonal Key Values:")
        PersonalKeyValueSecureView.list(self._person.secureKeyValues)
