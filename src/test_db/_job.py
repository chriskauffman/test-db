import logging

import faker
from faker.providers import BaseProvider
import nanoid
from sqlobject import (  # type: ignore
    connectionForURI,
    DatabaseIndex,
    DateTimeCol,
    JSONCol,
    ForeignKey,
    SQLObject,
    StringCol,
)
from typeid import TypeID
from typing_extensions import Optional, Self, Union

from test_db._type_id_col import TypeIDCol
from test_db._gid import validGID
from test_db._organization import Organization
from test_db._person import Person

logger = logging.getLogger(__name__)


class FakeEmployment(BaseProvider):
    """Faker Employement Info for Testing"""

    def employee_id(self) -> str:
        """Generates fake employee ID"""
        return nanoid.generate(size=20)


fake = faker.Faker()
fake.add_provider(FakeEmployment)


class Job(SQLObject):
    """Job SQLObject

    Attributes:
        gID (TypeIDCol): global ID for the object
        attributes (JSONCol): JSON attributes for the object. **Note** - The DB
                              isn't updated until the object is saved (no DB updates
                              when individual fields are changed)
        description (StringCol): description of the object
        employeeID (StringCol): the person's employee ID
        location (StringCol): the job's location
        payGroup (StringCol): the job's pay group
        organization (ForeignKey): the DB ID of the organization
        person (ForeignKey): the DB ID of the person
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        employeeIDOrganizationIndex (DatabaseIndex):
    """

    _gIDPrefix: str = "j"

    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)
    attributes: JSONCol = JSONCol(default={}, notNull=True)
    description: StringCol = StringCol(default=None)

    employeeID: StringCol = StringCol(default=fake.employee_id)
    location: StringCol = StringCol(default=None)
    payGroup: StringCol = StringCol(default=None)

    organization: ForeignKey = ForeignKey("Organization", default=None)
    person: ForeignKey = ForeignKey("Person", default=None)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    employeeIDOrganizationIndex: DatabaseIndex = DatabaseIndex(
        employeeID, organization, unique=True
    )

    @property
    def visualID(self):
        viewItems = [
            str(self.gID),
            self.employeeID,
        ]
        if self.person:
            viewItems.append(self.person.lastName)
        if self.organization:
            viewItems.append(self.organization.name)
        return ", ".join(viewItems)

    def _set_gID(self, value):
        if value:
            if validGID(value, self._gIDPrefix):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(TypeID(self._gIDPrefix))

    # def _set_organizationID(self, value):
    #     if value:
    #         self._SO_set_organizationID(value)
    #     else:
    #         if self.createDependents:
    #             self._SO_set_organizationID(
    #                 Organization(connection=self._connection).id
    #             )

    # def _set_personID(self, value):
    #     if value:
    #         self._SO_set_personID(value)
    #     else:
    #         if self.createDependents:
    #             self._SO_set_personID(Person(connection=self._connection).id)

    @classmethod
    def byOrganizationAndPerson(
        cls,
        organization: Union[Organization, int],
        person: Union[Person, int],
        connection: Optional[connectionForURI] = None,
    ) -> Self:
        """Locate jobs using unique index properties

        Simulates SQLObject's automatic by{alternateID} functions

        Args:
            organization (Union[Organization, int]):
            person (Union[Person, int]):
            connection (Optional[connectionForURI]):

        Returns:
            Self: Job
        """
        return cls.selectBy(
            organization=organization, person=person, connection=connection
        ).getOne()
