import logging

import faker
import nanoid
from sqlobject import (
    DateCol,
    DateTimeCol,
    MultipleJoin,
    SQLMultipleJoin,
    SQLObject,
    SQLObjectNotFound,
    StringCol,
    events,
)

from test_db._gid import GIDMixin
from test_db._listeners import handleRowCreateSignal, handleRowUpdateSignal
from test_db._person_address import PersonAddress
from test_db._person_bank_account import PersonBankAccount
from test_db._person_debit_card import PersonDebitCard
from test_db._type_id_col import TypeIDCol

fake = faker.Faker()
logger = logging.getLogger(__name__)


class Person(GIDMixin, SQLObject):
    """Person SQLObject

    Attributes:
        gID (TypeIDCol): global ID for the object
        firstName (StringCol): the person's first name
        lastName (StringCol): the person's last name
        description (StringCol): description of the entity
        dateOfBirth (DateCol): the person's birth date
        socialSecurityNumber (StringCol): the person's SSN
        email (StringCol): the person's email
        phoneNumber (StringCol): the entity's phone number
        addresses (MultipleJoin): list of addresses related to the entity
        addressesSelect (SQLMultipleJoin):
        bankAccounts (MultipleJoin): list of bank accounts related to the entity
        bankAccountsSelect (SQLMultipleJoin):
        debitCards (MultipleJoin): list of debit cards related to the entity
        debitCardsSelect (SQLMultipleJoin):
        jobs (MultipleJoin): list of employments
        jobsSelect (SQLMultipleJoin):
        keyValues (MultipleJoin):
        keyValuesSelect (SQLMultipleJoin):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        ownerID (str): owner ID for the object
    """

    _gIDPrefix: str = "p"
    _set_gID = GIDMixin._set_gID

    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)

    firstName: StringCol = StringCol(default=fake.first_name)
    lastName: StringCol = StringCol(default=fake.last_name)
    description: StringCol = StringCol(default=None)
    dateOfBirth: DateCol = DateCol(
        default=lambda: fake.date_of_birth(minimum_age=18, maximum_age=90)
    )
    socialSecurityNumber: StringCol = StringCol(
        alternateID=True, default=fake.ssn, unique=True
    )
    email: StringCol = StringCol(alternateID=True, default=None, unique=True)
    phoneNumber: StringCol = StringCol(default=fake.basic_phone_number)

    addresses: MultipleJoin = MultipleJoin("PersonAddress")
    addressesSelect: SQLMultipleJoin = SQLMultipleJoin("PersonAddress")
    bankAccounts: MultipleJoin = MultipleJoin("PersonBankAccount")
    bankAccountsSelect: SQLMultipleJoin = SQLMultipleJoin("PersonBankAccount")
    debitCards: MultipleJoin = MultipleJoin("PersonDebitCard")
    debitCardsSelect: SQLMultipleJoin = SQLMultipleJoin("PersonDebitCard")

    jobs: MultipleJoin = MultipleJoin("Job")
    jobsSelect: SQLMultipleJoin = SQLMultipleJoin("Job")

    keyValues: MultipleJoin = MultipleJoin("PersonKeyValue")
    keyValuesSelect: SQLMultipleJoin = SQLMultipleJoin("PersonKeyValue")

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    ownerID: str = "global"

    @property
    def name(self):
        return f"{self.firstName} {self.lastName}"

    @property
    def visualID(self) -> str:
        """Easy representation of the object"""
        return f"{self.gID} {self.name} {self.email}"

    def _set_email(self, value=None):
        """Handle email generation when names provided"""
        self.firstName = self.firstName or fake.first_name()
        self.lastName = self.lastName or fake.last_name()
        if value:
            self._SO_set_email(value)
        else:
            self._SO_set_email(
                f"{self.firstName.lower()}.{self.lastName.lower()}@example.com"
            )


def handlePersonRowCreateSignal(instance, kwargs, post_funcs):
    handleRowCreateSignal(instance, kwargs, post_funcs)
    if kwargs.get("firstName") is None and kwargs.get("lastName") is None:
        while True:
            kwargs["firstName"] = fake.first_name()
            kwargs["lastName"] = fake.last_name()
            try:
                Person.selectBy(
                    firstName=kwargs["firstName"],
                    lastName=kwargs["lastName"],
                    connection=kwargs.get("connection"),
                ).getOne()
            except SQLObjectNotFound:
                break
    if kwargs.get("firstName") is None:
        kwargs["firstName"] = fake.first_name()
    if kwargs.get("lastName") is None:
        kwargs["lastName"] = fake.last_name()
    if kwargs.get("email") is None:
        for email in (
            f"{kwargs['firstName'].lower()}.{kwargs['lastName'].lower()}@example.com",
            f"{kwargs['firstName'][:1].lower()}{kwargs['lastName'].lower()}@example.com",
            f"{kwargs['firstName'].lower()}{kwargs['lastName'][:1].lower()}@example.com",
            f"{kwargs['firstName'].lower()}.{kwargs['lastName'].lower()}.{nanoid.generate(size=5)}@example.com",
        ):
            try:
                Person.byEmail(email, connection=kwargs.get("connection"))
            except SQLObjectNotFound:
                kwargs["email"] = email
                break
    if kwargs.get("phoneNumber") is None:
        while True:
            kwargs["phoneNumber"] = fake.basic_phone_number()
            try:
                Person.selectBy(
                    phoneNumber=kwargs["phoneNumber"],
                    connection=kwargs.get("connection"),
                ).getOne()
            except SQLObjectNotFound:
                break
    if kwargs.get("socialSecurityNumber") is None:
        while True:
            kwargs["socialSecurityNumber"] = fake.ssn()
            try:
                Person.bySocialSecurityNumber(
                    kwargs["socialSecurityNumber"],
                    connection=kwargs.get("connection"),
                )
            except SQLObjectNotFound:
                break


events.listen(handlePersonRowCreateSignal, Person, events.RowCreateSignal)
events.listen(handleRowUpdateSignal, Person, events.RowUpdateSignal)


def handlePersonRowCreatedSignal(instance, kwargs, post_funcs):
    if instance._connection.tdbGlobalDatabaseOptions.autoCreateDependents:
        if not instance.addresses:
            PersonAddress(person=instance, connection=instance._connection)
        if not instance.bankAccounts:
            PersonBankAccount(person=instance, connection=instance._connection)
        if not instance.debitCards:
            PersonDebitCard(person=instance, connection=instance._connection)


events.listen(handlePersonRowCreatedSignal, Person, events.RowCreatedSignal)


def handlePersonAddressRowCreatedSignal(instance, kwargs, post_funcs):
    if (
        instance._connection.tdbGlobalDatabaseOptions.autoCreateDependents
        and not instance.person
    ):
        instance.person = Person(connection=instance._connection)


events.listen(
    handlePersonAddressRowCreatedSignal,
    PersonAddress,
    events.RowCreatedSignal,
)


def handlePersonBankAccountRowCreatedSignal(instance, kwargs, post_funcs):
    if (
        instance._connection.tdbGlobalDatabaseOptions.autoCreateDependents
        and not instance.person
    ):
        instance.person = Person(connection=instance._connection)


events.listen(
    handlePersonBankAccountRowCreatedSignal,
    PersonBankAccount,
    events.RowCreatedSignal,
)


def handlePersonDebitCardRowCreatedSignal(instance, kwargs, post_funcs):
    if (
        instance._connection.tdbGlobalDatabaseOptions.autoCreateDependents
        and not instance.person
    ):
        instance.person = Person(connection=instance._connection)


events.listen(
    handlePersonDebitCardRowCreatedSignal,
    PersonDebitCard,
    events.RowCreatedSignal,
)
