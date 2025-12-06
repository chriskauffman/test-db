import logging

import faker
from sqlobject import (  # type: ignore
    DateCol,
    DateTimeCol,
    MultipleJoin,
    SQLMultipleJoin,
    SQLObjectNotFound,
    StringCol,
)

from typeid import TypeID
from typing_extensions import Optional

from test_db._entity import Entity
from test_db._gid import validGID
from test_db._personal_key_value_secure import PersonalKeyValueSecure
from test_db._type_id_col import TypeIDCol

fake = faker.Faker()
logger = logging.getLogger(__name__)


class Person(Entity):
    """Person SQLObject

    Attributes:
        gID (TypeIDCol): global ID for the object
        firstName (StringCol): the person's first name
        lastName (StringCol): the person's last name
        dateOfBirth (DateCol): the person's birth date
        socialSecurityNumber (StringCol): the person's SSN
        email (StringCol): the person's email
        jobs (MultipleJoin): list of employments
        jobsSelect (SQLMultipleJoin):
        secureKeyValues (MultipleJoin): list of key/value pairs related to the person
        secureKeyValuesSelect (SQLMultipleJoin):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    _gIDPrefix: str = "p"

    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)

    firstName: StringCol = StringCol(default=fake.first_name)
    lastName: StringCol = StringCol(default=fake.last_name)
    dateOfBirth: DateCol = DateCol(
        default=lambda: fake.date_of_birth(minimum_age=18, maximum_age=90)
    )
    socialSecurityNumber: StringCol = StringCol(
        alternateID=True, length=9, default=fake.ssn, unique=True
    )
    email: StringCol = StringCol(alternateID=True, default=None, unique=True)

    jobs: MultipleJoin = MultipleJoin("Job")
    jobsSelect: SQLMultipleJoin = SQLMultipleJoin("Job")

    secureKeyValues: MultipleJoin = MultipleJoin("PersonalKeyValueSecure")
    secureKeyValuesSelect: SQLMultipleJoin = SQLMultipleJoin("PersonalKeyValueSecure")

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

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

    def getPersonalKeyValueSecureByKey(
        self, key: str, **kwargs
    ) -> Optional[PersonalKeyValueSecure]:
        """Find and create an PersonalOAuth2Token

        Args:
            key (str): name of the PersonalKeyValue
            **kwargs:

        Returns:
            Optional[PersonalKeyValueSecure]:
        """
        try:
            return self.secureKeyValuesSelect.filter(
                PersonalKeyValueSecure.q.key == key
            ).getOne()
        except SQLObjectNotFound:
            return PersonalKeyValueSecure(
                connection=self._connection, key=key, person=self.id, **kwargs
            )
        return None
