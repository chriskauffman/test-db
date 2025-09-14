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
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> Optional[Person]:
        """Add a person"""
        if first_name and last_name and not email:
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"
        if cls._user_inputs_required:
            first_name = cls._get_input("First Name", str, first_name)
            last_name = cls._get_input("Last Name", str, last_name)
            email = (
                email
                or f"{str(first_name).lower()}.{str(last_name).lower()}@example.com"
            )
            email = cls._get_input("Email", str, email)
        if not Person.findByEmail(str(email)):
            if email and first_name and last_name:
                if (
                    cls._user_inputs_required
                    and (
                        input(
                            f"Would you like to add {email}, "
                            f"{first_name} {last_name}? [y/n] "
                        )
                        .strip()
                        .lower()
                    )
                    != "y"
                ):
                    return None
                return Person(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
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
        self._person.first_name = self._get_input(
            "First Name", str, self._person.first_name
        )
        self._person.last_name = self._get_input(
            "Last Name", str, self._person.last_name
        )
        dob_input = self._get_input(
            "Date of Birth MM-DD-YYYY",
            str,
            self._person.date_of_birth.strftime("%m/%d/%Y"),
        )
        if dob_input:
            try:
                self._person.date_of_birth = datetime.datetime.strptime(
                    dob_input, "%m/%d/%Y"
                )
            except ValueError:
                logger.error("bad date - MM-DD-YYYY required")
        self._person.social_security_number = self._get_input(
            "SSN", str, self._person.social_security_number
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
        self._person.defaultAddress.postal_code = self._get_input(
            "Postal Code", str, self._person.defaultAddress.postal_code
        )
        self._person.defaultAddress.country = self._get_input(
            "Country", str, self._person.defaultAddress.country
        )
        self._person.phone_number = self._get_input(
            "Phone Number", str, self._person.phone_number
        )

    def view(self):
        """Display brief details of the person"""
        print(
            f"{self._person.first_name} {self._person.last_name}, {self._person.email}"
        )

    def view_details(self):
        """Display the person"""
        print(f"\nFirst Name:\t{self._person.first_name}")
        print(f"Last Name:\t{self._person.last_name}")
        print(f"Date of Birth:\t{self._person.date_of_birth.strftime('%m/%d/%Y')}")
        print(f"SSN:\t\t{self._person.social_security_number}")
        print(f"Email:\t\t{self._person.email}")
        print(f"Phone Number:\t{self._person.phone_number}")
        print(f"Created At:\t{self._person.created_at}")
        print(f"Updated At:\t{self._person.updated_at}")
        print("\nAddresses:")
        for item in self._person.addresses:
            print(
                f"\t{item.street}, {item.locality}, {item.region}, {item.postal_code}, {item.country}"
            )
        print("\nBank Accounts:")
        for item in self._person.bank_accounts:
            print(f"\t{item.name}, {item.routing_number}, {item.account_number}")
        print("\nDebit Cards:")
        for item in self._person.debit_cards:
            print(
                f"\t{item.name}, {item.card_number}, {item.cvv}, "
                f"{item.expiration_month}/{item.expiration_year}"
            )
        print("\nJobs:")
        for item in self._person.jobs:
            print(f"\t{item.employee_id}, {item.pay_group}")
        print("\nOAuth2 Tokens:")
        for item in self._person.oauth2_tokens:
            print(f"\t{item.client_id}")
        print("\nPerson App Settings:")
        for item in self._person.person_app_settings:
            print(f"\t{item.name}")
            print("\t\tAttributes:")
            print(json.dumps(item.attributes, indent=4))
