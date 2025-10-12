import datetime
import json
import logging

from pydantic import EmailStr
from typing_extensions import Optional

from test_db import Person
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class PersonView(BaseView):
    """Person views

    Args:
        person (Person):
        **kwargs:
            - user_inputs_required (bool):
    """

    _user_inputs_required: bool = True

    @classmethod
    def list(cls):
        """List all people"""
        for person in Person.select():
            PersonView(person).view()

    @classmethod
    def add(
        cls,
        email: Optional[EmailStr] = None,
        firstName: Optional[str] = None,
        lastName: Optional[str] = None,
    ) -> Optional[Person]:
        """Add a person"""
        if firstName and lastName and not email:
            email = f"{firstName.lower()}.{lastName.lower()}@example.com"
        if cls._user_inputs_required:
            firstName = cls._get_input("First Name", str, firstName)
            lastName = cls._get_input("Last Name", str, lastName)
            email = (
                email or f"{str(firstName).lower()}.{str(lastName).lower()}@example.com"
            )
            email = cls._get_input("Email", str, email)
        if not Person.findByEmail(str(email)):
            if email and firstName and lastName:
                if (
                    cls._user_inputs_required
                    and (
                        input(
                            f"Would you like to add {email}, "
                            f"{firstName} {lastName}? [y/n] "
                        )
                        .strip()
                        .lower()
                    )
                    != "y"
                ):
                    return None
                return Person(
                    email=email,
                    firstName=firstName,
                    lastName=lastName,
                )
            else:
                print("error: incorrect user info")
        else:
            print(f"error: User {email} exists, cannot add")
        return None

    def __init__(self, person: Person, **kwargs):
        super().__init__(**kwargs)
        self._person = person

    def edit(self):
        """Edit the person"""
        self._person.firstName = self._get_input(
            "First Name", str, self._person.firstName
        )
        self._person.lastName = self._get_input("Last Name", str, self._person.lastName)
        dob_input = self._get_input(
            "Date of Birth MM-DD-YYYY",
            str,
            self._person.dateOfBirth.strftime("%m/%d/%Y"),
        )
        if dob_input:
            try:
                self._person.dateOfBirth = datetime.datetime.strptime(
                    dob_input, "%m/%d/%Y"
                )
            except ValueError:
                logger.error("bad date - MM-DD-YYYY required")
        self._person.socialSecurityNumber = self._get_input(
            "SSN", str, self._person.socialSecurityNumber
        )
        self._person.defaultAddress.street = self._get_input(
            "Street", str, self._person.defaultAddress.street
        )
        self._person.defaultAddress.locality = self._get_input(
            "Locality", str, self._person.defaultAddress.locality
        )
        self._person.defaultAddress.region = self._get_input(
            "Region", str, self._person.defaultAddress.region
        )
        self._person.defaultAddress.postalCode = self._get_input(
            "Postal Code", str, self._person.defaultAddress.postalCode
        )
        self._person.defaultAddress.country = self._get_input(
            "Country", str, self._person.defaultAddress.country
        )
        self._person.phoneNumber = self._get_input(
            "Phone Number", str, self._person.phoneNumber
        )

    def view(self):
        """Display brief details of the person"""
        print(f"{self._person.firstName} {self._person.lastName}, {self._person.email}")

    def viewDetails(self):
        """Display the person"""
        print(f"\nFirst Name:\t{self._person.firstName}")
        print(f"Last Name:\t{self._person.lastName}")
        print(f"Date of Birth:\t{self._person.dateOfBirth.strftime('%m/%d/%Y')}")
        print(f"SSN:\t\t{self._person.socialSecurityNumber}")
        print(f"Email:\t\t{self._person.email}")
        print(f"Phone Number:\t{self._person.phoneNumber}")
        print(f"Created At:\t{self._person.createdAt}")
        print(f"Updated At:\t{self._person.updatedAt}")
        print("\nAddresses:")
        for item in self._person.addresses:
            print(
                f"\t{item.street}, {item.locality}, {item.region}, {item.postalCode}, {item.country}"
            )
        print("\nBank Accounts:")
        for item in self._person.bankAccounts:
            print(f"\t{item.name}, {item.routingNumber}, {item.accountNumber}")
        print("\nDebit Cards:")
        for item in self._person.debitCards:
            print(
                f"\t{item.name}, {item.cardNumber}, {item.cvv}, "
                f"{item.expirationMonth}/{item.expirationYear}"
            )
        print("\nJobs:")
        for item in self._person.jobs:
            print(f"\t{item.employeeID}, {item.payGroup}")
        print("\nPerson App KeyValue:")
        for item in self._person.PersonalKeyValues:
            print(f"\t{item.name} = {item.value}")
        print("\nPerson App KeyValue:")
        for item in self._person.PersonalKeyJsons:
            print(f"\t{item.name}")
            print("\t\tAttributes:")
            print(json.dumps(item.attributes, indent=4))
