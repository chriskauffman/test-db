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
from test_db._full_sqlobject import FullSQLObject
from test_db._settings import PersonalKeyJson, PersonalKeyValue

fake = faker.Faker()
logger = logging.getLogger(__name__)


class Person(FullSQLObject):
    """Person SQLObject

    Note: All attributes are generated when not provided

    Attributes:
        firstName (StringCol): the person's first name
        lastName (StringCol): the person's last name
        dateOfBirth (DateCol): the person's birth date
        socialSecurityNumber (StringCol): the person's SSN
        email (StringCol): the person's email
        phoneNumber (StringCol): the person's phone number
        addresses (MultipleJoin): list of addresses
        addressesSelect (SQLMultipleJoin):
        bankAccounts (MultipleJoin): list of bank accounts
        bankAccountsSelect (SQLMultipleJoin):
        debitCards (MultipleJoin): list of debit cards
        debitCardsSelect (SQLMultipleJoin):
        jobs (MultipleJoin): list of employments
        jobsSelect (SQLMultipleJoin):
        oauth2Tokens (MultipleJoin):
        oauth2TokensSelect (SQLMultipleJoin):
        PersonalKeyValues (MultipleJoin):
        PersonalKeyValuesSelect (SQLMultipleJoin):
        PersonalKeyJsons (MultipleJoin):
        PersonalKeyJsonsSelect (SQLMultipleJoin):
    """

    _gIDPrefix: str = "p"

    firstName: StringCol = StringCol(default=fake.first_name)
    lastName: StringCol = StringCol(default=fake.last_name)
    dateOfBirth: DateCol = DateCol(
        default=fake.date_of_birth(minimum_age=18, maximum_age=70)
    )
    socialSecurityNumber: StringCol = StringCol(
        alternateID=True, length=9, default=fake.ssn, unique=True
    )
    email: StringCol = StringCol(alternateID=True, default=None, unique=True)
    phoneNumber: StringCol = StringCol(
        alternateID=True, default=fake.basic_phone_number, unique=True
    )

    addresses: MultipleJoin = MultipleJoin("PersonalAddress")
    addressesSelect: SQLMultipleJoin = SQLMultipleJoin("PersonalAddress")
    bankAccounts: MultipleJoin = MultipleJoin("PersonalBankAccount")
    bankAccountsSelect: SQLMultipleJoin = SQLMultipleJoin("PersonalBankAccount")
    debitCards: MultipleJoin = MultipleJoin("PersonalDebitCard")
    debitCardsSelect: SQLMultipleJoin = SQLMultipleJoin("PersonalDebitCard")
    jobs: MultipleJoin = MultipleJoin("Job")
    jobsSelect: SQLMultipleJoin = SQLMultipleJoin("Job")
    oauth2Tokens: MultipleJoin = MultipleJoin("PersonalOAuth2Token")
    oauth2TokensSelect: SQLMultipleJoin = SQLMultipleJoin("PersonalOAuth2Token")
    PersonalKeyValues: MultipleJoin = MultipleJoin("PersonalKeyValue")
    PersonalKeyValuesSelect: SQLMultipleJoin = SQLMultipleJoin("PersonalKeyValue")
    PersonalKeyJsons: MultipleJoin = MultipleJoin("PersonalKeyJson")
    PersonalKeyJsonsSelect: SQLMultipleJoin = SQLMultipleJoin("PersonalKeyJson")

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
            "firstName": self.firstName,
            "lastName": self.lastName,
            "dateOfBirth": self.dateOfBirth,
            "socialSecurityNumber": self.socialSecurityNumber,
            "phoneNumber": self.phoneNumber,
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
        self.firstName = self.firstName or self.fake.first_name()
        self.lastName = self.lastName or self.fake.last_name()
        if value:
            self._SO_set_email(value)
        else:
            self._SO_set_email(
                f"{self.firstName.lower()}.{self.lastName.lower()}@example.com"
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
            return self.addressesSelect.filter(PersonalAddress.q.name == name).getOne()
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
            return self.bankAccountsSelect.filter(
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
            return self.debitCardsSelect.filter(
                PersonalDebitCard.q.name == name
            ).getOne()
        except SQLObjectNotFound:
            return PersonalDebitCard(
                connection=self._connection,
                person=self.id,
                name=name,
                **kwargs,
            )

    def getJobByEmployerId(self, employer_id: int, **kwargs) -> "Job":
        """Find and create an Job

        Args:
            employer_id (int): employer_id of the job
            **kwargs:

        Returns:
            Job:
        """
        try:
            return self.jobsSelect.filter(Job.q.employer == employer_id).getOne()
        except SQLObjectNotFound:
            try:
                employer = Employer.get(employer_id, connection=self._connection)
            except SQLObjectNotFound:
                employer = Employer(connection=self._connection, id=employer_id)
            return Job(
                connection=self._connection,
                person=self.id,
                employer=employer.id,
                **kwargs,
            )

    def getJobByEmployerAlternateId(self, employerAlternateID: str, **kwargs) -> "Job":
        """Find and create an Job

        Args:
            employerAlternateID (str): employer alternateID of the job
            **kwargs:

        Returns:
            Job:
        """
        try:
            return self.jobsSelect.throughTo.employer.filter(
                Employer.q.alternateID == employerAlternateID
            ).getOne()
        except SQLObjectNotFound:
            try:
                employer = Employer.select(
                    Employer.q.alternateID == employerAlternateID,
                    connection=self._connection,
                ).getOne()
            except SQLObjectNotFound:
                employer = Employer(
                    connection=self._connection, alternateID=employerAlternateID
                )
            return Job(
                connection=self._connection,
                person=self.id,
                employer=employer.id,
                **kwargs,
            )

    def getOAuth2TokenByClientId(self, clientID: str, **kwargs) -> PersonalOAuth2Token:
        """Find and create an PersonalOAuth2Token

        Args:
            clientID (str): client ID used to generate token
            **kwargs:

        Returns:
            PersonalOAuth2Token:
        """
        try:
            return self.oauth2TokensSelect.filter(
                PersonalOAuth2Token.q.clientID == clientID
            ).getOne()
        except SQLObjectNotFound:
            return PersonalOAuth2Token(
                connection=self._connection,
                clientID=clientID,
                person=self.id,
                **kwargs,
            )

    def getPersonalKeyValuesByKey(self, key: str, **kwargs) -> PersonalKeyValue:
        """Find and create an PersonalKeyValue

        Args:
            key (str): name of the PersonalKeyValue
            **kwargs:

        Returns:
            PersonalKeyValue:
        """
        try:
            return self.PersonalKeyValuesSelect.filter(
                PersonalKeyValue.q.key == key
            ).getOne()
        except SQLObjectNotFound:
            return PersonalKeyValue(
                connection=self._connection, key=key, person=self.id, **kwargs
            )

    def getPersonalKeyJsonsByKey(self, key: str, **kwargs) -> PersonalKeyJson:
        """Find and create an PersonalKeyJson

        Args:
            key (str): name of the PersonalKeyJson
            **kwargs:

        Returns:
            PersonalKeyJson:
        """
        try:
            return self.PersonalKeyJsonsSelect.filter(
                PersonalKeyJson.q.key == key
            ).getOne()
        except SQLObjectNotFound:
            return PersonalKeyJson(
                connection=self._connection, key=key, person=self.id, **kwargs
            )

    def resetAuth(self) -> None:
        """Reset all Auth values for the person"""
        PersonalOAuth2Token.deleteMany(
            PersonalOAuth2Token.q.person == self.id, connection=self._connection
        )

    def resetPersonalKeyValues(self) -> None:
        """Reset all PersonalKeyJson for the person"""
        PersonalKeyValue.deleteMany(
            PersonalKeyValue.q.person == self.id, connection=self._connection
        )

    def resetPersonalKeyJsons(self) -> None:
        """Reset all PersonalKeyJson for the person"""
        PersonalKeyJson.deleteMany(
            PersonalKeyJson.q.person == self.id, connection=self._connection
        )
