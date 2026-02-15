import logging

import faker
from sqlobject import (  # type: ignore
    events,
    DatabaseIndex,
    DateCol,
    DateTimeCol,
    MultipleJoin,
    SQLMultipleJoin,
    SQLObject,
    SQLObjectNotFound,
    StringCol,
)

from typeid import TypeID

from test_db._gid import validGID
from test_db._listeners import handleRowCreateSignal, handleRowUpdateSignal
from test_db._person_address import PersonAddress
from test_db._person_bank_account import PersonBankAccount
from test_db._person_debit_card import PersonDebitCard
from test_db._person_key_value import PersonKeyValue
from test_db._person_secure_key_value import PersonSecureKeyValue
from test_db._type_id_col import TypeIDCol

fake = faker.Faker()
logger = logging.getLogger(__name__)


class Person(SQLObject):
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
        secureKeyValues (MultipleJoin):
        secureKeyValuesSelect (SQLMultipleJoin):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        ownerID (str): owner ID for the object
    """

    _gIDPrefix: str = "p"

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

    secureKeyValues: MultipleJoin = MultipleJoin("PersonSecureKeyValue")
    secureKeyValuesSelect: SQLMultipleJoin = SQLMultipleJoin("PersonSecureKeyValue")

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

    def _set_gID(self, value):
        if value:
            if validGID(value, self._gIDPrefix):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(TypeID(self._gIDPrefix))

    def getKeyValueByKey(self, key: str, **kwargs) -> PersonKeyValue:
        """Find and create an PersonKeyValue

        Args:
            key (str): name of the PersonKeyValue
            **kwargs:

        Returns:
            PersonKeyValue:
        """
        try:
            return self.keyValuesSelect.filter(PersonKeyValue.q.key == key).getOne()
        except SQLObjectNotFound:
            return PersonKeyValue(
                connection=self._connection, person=self.id, key=key, **kwargs
            )

    def getSecureKeyValueByKey(self, key: str, **kwargs) -> PersonSecureKeyValue:
        """Find and create an PersonSecureKeyValue

        Args:
            key (str): name of the PersonSecureKeyValue
            **kwargs:

        Returns:
            PersonSecureKeyValue:
        """
        try:
            return self.secureKeyValuesSelect.filter(
                PersonSecureKeyValue.q.key == key
            ).getOne()
        except SQLObjectNotFound:
            return PersonSecureKeyValue(
                connection=self._connection, person=self.id, key=key, **kwargs
            )


def handlePersonRowCreateSignal(instance, kwargs, post_funcs):
    handleRowCreateSignal(instance, kwargs, post_funcs)
    if (
        kwargs.get("firstName") is None
        and kwargs.get("lastName") is None
        and kwargs.get("email") is None
    ):
        while True:
            kwargs["firstName"] = fake.first_name()
            kwargs["lastName"] = fake.last_name()
            kwargs["email"] = (
                f"{kwargs['firstName'].lower()}.{kwargs['lastName'].lower()}@example.com"
            )
            try:
                if kwargs.get("connection"):
                    Person.selectBy(
                        firstName=kwargs["firstName"],
                        lastName=kwargs["lastName"],
                        email=kwargs["email"],
                        connection=kwargs["connection"],
                    ).getOne()
                else:
                    Person.selectBy(
                        firstName=kwargs["firstName"],
                        lastName=kwargs["lastName"],
                        email=kwargs["email"],
                    ).getOne()
            except SQLObjectNotFound:
                break
    if kwargs.get("socialSecurityNumber") is None:
        while True:
            kwargs["socialSecurityNumber"] = fake.ssn()
            try:
                if kwargs.get("connection"):
                    Person.bySocialSecurityNumber(
                        kwargs["socialSecurityNumber"], connection=kwargs["connection"]
                    )
                else:
                    Person.bySocialSecurityNumber(kwargs["socialSecurityNumber"])
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
    if instance._connection.tdbGlobalDatabaseOptions.autoCreateDependents:
        if not instance.person:
            instance.person = Person(connection=instance._connection)


events.listen(
    handlePersonAddressRowCreatedSignal,
    PersonAddress,
    events.RowCreatedSignal,
)


def handlePersonBankAccountRowCreatedSignal(instance, kwargs, post_funcs):
    if instance._connection.tdbGlobalDatabaseOptions.autoCreateDependents:
        if not instance.person:
            instance.person = Person(connection=instance._connection)


events.listen(
    handlePersonBankAccountRowCreatedSignal,
    PersonBankAccount,
    events.RowCreatedSignal,
)


def handlePersonDebitCardRowCreatedSignal(instance, kwargs, post_funcs):
    if instance._connection.tdbGlobalDatabaseOptions.autoCreateDependents:
        if not instance.person:
            instance.person = Person(connection=instance._connection)


events.listen(
    handlePersonDebitCardRowCreatedSignal,
    PersonDebitCard,
    events.RowCreatedSignal,
)
