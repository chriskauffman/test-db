import logging

import faker
from sqlobject import (  # type: ignore
    DateCol,
    DateTimeCol,
    JSONCol,
    MultipleJoin,
    RelatedJoin,
    SQLMultipleJoin,
    SQLObject,
    SQLObjectNotFound,
    StringCol,
)
import sqlobject.sqlbuilder  # type: ignore


# from sqlobject.main import SQLObjectNotFound
from typing_extensions import Any, Self, Union

from test_db._address import Address
from test_db._bank_account import BankAccount
from test_db._debit_card import DebitCard
from test_db._organization import Organization
from test_db._job import Job
from test_db._personal_key_value_secure import PersonalKeyValueSecure
from test_db._type_id_col import TypeIDCol
from test_db._gid_sqlobject import GID_SQLObject

fake = faker.Faker()
logger = logging.getLogger(__name__)


class Person(GID_SQLObject):
    """Person SQLObject

    Note: All attributes are generated when not provided

    Attributes:
        gID (TypeIDCol): global ID for the object
        attributes (JSONCol): JSON attributes for the object
                              Note: the DB isn't updated until the object is saved
                                    (no DB updates when individual fields are changed)
        description (StringCol): description of the object
        firstName (StringCol): the person's first name
        lastName (StringCol): the person's last name
        dateOfBirth (DateCol): the person's birth date
        socialSecurityNumber (StringCol): the person's SSN
        email (StringCol): the person's email
        phoneNumber (StringCol): the person's phone number
        jobs (MultipleJoin): list of employments
        jobsSelect (SQLMultipleJoin):
        addresses (RelatedJoin): list of addresses related to the person
        bankAccounts (RelatedJoin): list of bank accounts related to the person
        debitCards (RelatedJoin): list of debit cards related to the person
        secureKeyValues (MultipleJoin): list of key/value pairs related to the person
        secureKeyValuesSelect (SQLMultipleJoin):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    _gIDPrefix: str = "p"

    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)
    attributes: JSONCol = JSONCol(default=None)
    description: StringCol = StringCol(default=None)

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

    jobs: MultipleJoin = MultipleJoin("Job")
    jobsSelect: SQLMultipleJoin = SQLMultipleJoin("Job")

    addresses: RelatedJoin = RelatedJoin("Address")
    bankAccounts: RelatedJoin = RelatedJoin("BankAccount")
    debitCards: RelatedJoin = RelatedJoin("DebitCard")
    secureKeyValues: MultipleJoin = MultipleJoin("PersonalKeyValueSecure")
    secureKeyValuesSelect: SQLMultipleJoin = SQLMultipleJoin("PersonalKeyValueSecure")

    createdAt: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )
    updatedAt: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )

    def _set_gID(self, value):
        if value:
            if self.validGID(value):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(self._generateGID())

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
    def defaultAddress(self) -> Address:
        return self.getAddressByName("default")

    @property
    def defaultBankAccount(self) -> BankAccount:
        return self.getBankAccountByName("default")

    @property
    def defaultDebitCard(self) -> DebitCard:
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

    def getAddressByName(self, name: str, **kwargs) -> Address:
        """Return the default address for the person

        Args:
            name (str): name of the item
            **kwargs:

        Returns:
            Address: the default address or None
        """
        address = next(
            (address for address in self.addresses if address.description == name),
            None,
        )
        if address:
            return address
        else:
            address = Address(
                connection=self._connection,
                description=name,
                **kwargs,
            )
            self.addAddress(address)
            return address

    def getBankAccountByName(self, name: str, **kwargs) -> BankAccount:
        """Find and create bank account

        Args:
            name (str): name of the item
            **kwargs:

        Returns:
            BankAccount:
        """
        bank_account = next(
            (
                bank_account
                for bank_account in self.bankAccounts
                if bank_account.description == name
            ),
            None,
        )
        if bank_account:
            return bank_account
        else:
            bank_account = BankAccount(
                connection=self._connection,
                description=name,
                **kwargs,
            )
            self.addBankAccount(bank_account)
            return bank_account

    def getDebitCardByName(self, name: str, **kwargs) -> DebitCard:
        """Find and create debit card

        Args:
            name (str): name of the item
            **kwargs:

        Returns:
            DebitCard:
        """
        debit_card = next(
            (
                debit_card
                for debit_card in self.debitCards
                if debit_card.description == name
            ),
            None,
        )
        if debit_card:
            return debit_card
        else:
            debit_card = DebitCard(
                connection=self._connection,
                description=name,
                **kwargs,
            )
            self.addDebitCard(debit_card)
            return debit_card

    def getJobByOrganizationId(self, employer_id: int, **kwargs) -> "Job":
        """Find and create an Job

        Args:
            employer_id (int): employer_id of the job
            **kwargs:

        Returns:
            Job:
        """
        try:
            return self.jobsSelect.filter(Job.q.organization == employer_id).getOne()
        except SQLObjectNotFound:
            try:
                employer = Organization.get(employer_id, connection=self._connection)
            except SQLObjectNotFound:
                employer = Organization(connection=self._connection, id=employer_id)
            return Job(
                connection=self._connection,
                person=self.id,
                organization=employer.id,
                **kwargs,
            )

    def getJobByOrganizationAlternateId(
        self, employerAlternateID: str, **kwargs
    ) -> "Job":
        """Find and create an Job

        Args:
            employerAlternateID (str): employer alternateID of the job
            **kwargs:

        Returns:
            Job:
        """
        try:
            return self.jobsSelect.throughTo.organization.filter(
                Organization.q.alternateID == employerAlternateID
            ).getOne()
        except SQLObjectNotFound:
            try:
                employer = Organization.select(
                    Organization.q.alternateID == employerAlternateID,
                    connection=self._connection,
                ).getOne()
            except SQLObjectNotFound:
                employer = Organization(
                    connection=self._connection, alternateID=employerAlternateID
                )
            return Job(
                connection=self._connection,
                person=self.id,
                organization=employer.id,
                **kwargs,
            )

    def getOAuth2TokenByClientId(
        self, clientID: str, **kwargs
    ) -> PersonalKeyValueSecure:
        """Find and create an PersonalOAuth2Token

        Args:
            clientID (str): client ID used to generate token
            **kwargs:

        Returns:
            PersonalKeyValueSecure:
        """
        return self.getPersonalKeyValueSecureByKey(clientID, **kwargs)

    def getPersonalKeyValueSecureByKey(
        self, key: str, **kwargs
    ) -> PersonalKeyValueSecure:
        """Find and create an PersonalOAuth2Token

        Args:
            key (str): name of the PersonalKeyValue
            **kwargs:

        Returns:
            PersonalKeyValueSecure:
        """
        return self.getByKey(
            self.secureKeyValuesSelect, PersonalKeyValueSecure, key, **kwargs
        )

    def getByKey(
        self, collection: SQLMultipleJoin, object: SQLObject, key: str, **kwargs
    ) -> SQLObject:
        """Find and create an PersonalKeyJson

        Args:
            collection (SQLMultipleJoin):
            object (SQLObject):
            key (str): name of the PersonalKeyJson
            **kwargs:

        Returns:
            SQLObject:
        """
        try:
            return collection.filter(object.q.key == key).getOne()
        except SQLObjectNotFound:
            return object(
                connection=self._connection, key=key, person=self.id, **kwargs
            )
