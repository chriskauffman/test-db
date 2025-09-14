import logging

import faker
from sqlobject import (  # type: ignore
    DateCol,
    MultipleJoin,
    SQLMultipleJoin,
    SQLObjectNotFound,
    StringCol,
)


# from sqlobject.main import SQLObjectNotFound
from typing_extensions import Any, Self, Union

from test_db._address import PersonalAddress
from test_db._bank_account import PersonalBankAccount
from test_db._debit_card import PersonalDebitCard
from test_db._employer import Employer
from test_db._job import Job
from test_db._oauth2_token import PersonalOAuth2Token
from test_db._app_settings import PersonalAppSettings
from test_db._test_db_sqlobject import TestDBSQLObject

fake = faker.Faker()
logger = logging.getLogger(__name__)


class Person(TestDBSQLObject):
    """Person SQLObject

    Note: All attributes are generated when not provided

    Attributes:
        first_name (StringCol): the person's first name
        last_name (StringCol): the person's last name
        date_of_birth (DateCol): the person's birth date
        social_security_number (StringCol): the person's SSN
        email (StringCol): the person's email
        phone_number (StringCol): the person's phone number
        addresses (MultipleJoin): list of addresses
        addresses_select (SQLMultipleJoin):
        bank_accounts (MultipleJoin): list of bank accounts
        bank_accounts_select (SQLMultipleJoin):
        debit_cards (MultipleJoin): list of debit cards
        debit_cards_select (SQLMultipleJoin):
        jobs (MultipleJoin): list of employments
        jobs_select (SQLMultipleJoin):
        oauth2_tokens (MultipleJoin):
        oauth2_tokens_select (SQLMultipleJoin):
        person_app_settings (MultipleJoin):
        person_app_settings_select (SQLMultipleJoin):
    """

    _gid_prefix: str = "p"

    first_name: StringCol = StringCol(default=fake.first_name)
    last_name: StringCol = StringCol(default=fake.last_name)
    date_of_birth: DateCol = DateCol(
        default=fake.date_of_birth(minimum_age=18, maximum_age=70)
    )
    social_security_number: StringCol = StringCol(
        alternateID=True, length=9, default=fake.ssn, unique=True
    )
    email: StringCol = StringCol(alternateID=True, default=None, unique=True)
    phone_number: StringCol = StringCol(
        alternateID=True, default=fake.basic_phone_number, unique=True
    )

    addresses: MultipleJoin = MultipleJoin("PersonalAddress")
    addresses_select: SQLMultipleJoin = SQLMultipleJoin("PersonalAddress")
    bank_accounts: MultipleJoin = MultipleJoin("PersonalBankAccount")
    bank_accounts_select: SQLMultipleJoin = SQLMultipleJoin("PersonalBankAccount")
    debit_cards: MultipleJoin = MultipleJoin("PersonalDebitCard")
    debit_cards_select: SQLMultipleJoin = SQLMultipleJoin("PersonalDebitCard")
    jobs: MultipleJoin = MultipleJoin("Job")
    jobs_select: SQLMultipleJoin = SQLMultipleJoin("Job")
    oauth2_tokens: MultipleJoin = MultipleJoin("PersonalOAuth2Token")
    oauth2_tokens_select: SQLMultipleJoin = SQLMultipleJoin("PersonalOAuth2Token")
    person_app_settings: MultipleJoin = MultipleJoin("PersonalAppSettings")
    person_app_settings_select: SQLMultipleJoin = SQLMultipleJoin("PersonalAppSettings")

    @classmethod
    def deleteByEmail(cls, email: str, **kwargs):
        """Delete a person in the database using email

        Note: Delete cascades to all related objects

        Args:
            email (str): email address
            **kwargs:
        """
        cls.deleteBy(email=email, **kwargs)

    @classmethod
    def findByEmail(cls, email: str, **kwargs) -> Union[Self, None]:
        try:
            return Person.byEmail(email, **kwargs)
        except SQLObjectNotFound:
            return None

    @classmethod
    def list(cls, **kwargs: dict[str, Any]) -> list:
        """List all of the people in the database

        Args:
            **kwargs (dict[str, Any]):

        Returns:
            list: of people
        """
        people_list = []
        for person in cls.select(**kwargs).orderBy("email"):
            people_list.append(person.as_dict)
        return people_list

    @property
    def as_dict(self) -> dict:
        """Return object as dict"""
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "social_security_number": self.social_security_number,
            "phone_number": self.phone_number,
        }

    @property
    def defaultAddress(self) -> PersonalAddress:
        return self.getAddressByName("default")

    @property
    def defaultBankAccount(self) -> PersonalAddress:
        return self.getBankAccountByName("default")

    @property
    def defaultDebitCard(self) -> PersonalAddress:
        return self.getDebitCardByName("default")

    def _set_email(self, value=None):
        """Handle email generation when names provided"""
        self.first_name = self.first_name or self.fake.first_name()
        self.last_name = self.last_name or self.fake.last_name()
        if value:
            self._SO_set_email(value)
        else:
            self._SO_set_email(
                f"{self.first_name.lower()}.{self.last_name.lower()}@example.com"
            )

    def getAddressByName(self, name: str, **kwargs) -> PersonalAddress:
        """Return the default address for the person

        Args:
            name (str): name of the item
            **kwargs:

        Returns:
            PersonalAddress: the default address or None
        """
        try:
            return self.addresses_select.filter(PersonalAddress.q.name == name).getOne()
        except SQLObjectNotFound:
            return PersonalAddress(
                connection=self._connection,
                person=self.id,
                name=name,
                **kwargs,
            )

    def getBankAccountByName(self, name: str, **kwargs) -> PersonalBankAccount:
        """Find and create bank account

        Args:
            name (str): name of the item
            **kwargs:

        Returns:
            PersonalBankAccount:
        """
        try:
            return self.bank_accounts_select.filter(
                PersonalBankAccount.q.name == name
            ).getOne()
        except SQLObjectNotFound:
            return PersonalBankAccount(
                connection=self._connection,
                person=self.id,
                name=name,
                **kwargs,
            )

    def getDebitCardByName(self, name: str, **kwargs) -> PersonalDebitCard:
        """Find and create debit card

        Args:
            name (str): name of the item
            **kwargs:

        Returns:
            PersonalDebitCard:
        """
        try:
            return self.debit_cards_select.filter(
                PersonalDebitCard.q.name == name
            ).getOne()
        except SQLObjectNotFound:
            return PersonalDebitCard(
                connection=self._connection,
                person=self.id,
                name=name,
                **kwargs,
            )

    def getJobByEmployerId(self, employer_id: str, **kwargs) -> "Job":
        """Find and create an Job

        Args:
            employer_id (str): employer_id of the job
            **kwargs:

        Returns:
            Job:

        Raises:
            ValueError: when employer not found
        """
        try:
            return self.jobs_select.filter(Job.q.employer == employer_id).getOne()
        except SQLObjectNotFound:
            try:
                employer = Employer.get(employer_id, connection=self._connection)
            except SQLObjectNotFound:
                raise ValueError(f"Employer {employer_id} not found")
            return Job(
                connection=self._connection,
                person=self.id,
                employer=employer.id,
                **kwargs,
            )

    def getJobByEmployerAlternateId(
        self, employer_alternate_id: str, **kwargs
    ) -> "Job":
        """Find and create an Job

        Args:
            employer_alternate_id (str): employer alternate_id of the job
            **kwargs:

        Returns:
            Job:

        Raises:
            ValueError: when employer not found
        """
        try:
            return self.jobs_select.throughTo.employer.filter(
                Employer.q.alternate_id == employer_alternate_id
            ).getOne()
        except SQLObjectNotFound:
            try:
                employer = Employer.select(
                    Employer.q.alternate_id == employer_alternate_id,
                    connection=self._connection,
                ).getOne()
            except SQLObjectNotFound:
                raise ValueError(f"Employer {employer_alternate_id} not found")
            return Job(
                connection=self._connection,
                person=self.id,
                employer=employer.id,
                **kwargs,
            )

    def getOAuth2TokenByClientId(self, client_id: str, **kwargs) -> PersonalOAuth2Token:
        """Find and create an PersonalOAuth2Token

        Args:
            client_id (str): client ID used to generate token
            **kwargs:

        Returns:
            PersonalOAuth2Token:
        """
        try:
            return self.oauth2_tokens_select.filter(
                PersonalOAuth2Token.q.client_id == client_id
            ).getOne()
        except SQLObjectNotFound:
            return PersonalOAuth2Token(
                connection=self._connection,
                client_id=client_id,
                person=self.id,
                **kwargs,
            )

    def getPersonAppSettingsByName(self, name: str, **kwargs) -> PersonalAppSettings:
        """Find and create an PersonalAppSettings

        Args:
            name (str): name of the PersonalAppSettings
            **kwargs:

        Returns:
            PersonalAppSettings:
        """
        try:
            return self.person_app_settings_select.filter(
                PersonalAppSettings.q.name == name
            ).getOne()
        except SQLObjectNotFound:
            return PersonalAppSettings(
                connection=self._connection, name=name, person=self.id, **kwargs
            )

    def resetAuth(self) -> None:
        """Reset all Auth values for the person"""
        PersonalOAuth2Token.deleteMany(
            PersonalOAuth2Token.q.person == self.id, connection=self._connection
        )

    def resetPersonAppSettings(self) -> None:
        """Reset all PersonalAppSettings for the person"""
        PersonalAppSettings.deleteMany(
            PersonalAppSettings.q.person == self.id, connection=self._connection
        )
