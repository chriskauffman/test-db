import logging

import faker
from faker.providers import BaseProvider
import nanoid
from sqlobject import (  # type: ignore
    DateTimeCol,
    JSONCol,
    ForeignKey,
    StringCol,
)
import sqlobject.sqlbuilder  # type: ignore

from test_db._type_id_col import TypeIDCol
from test_db._gid_sqlobject import GID_SQLObject


logger = logging.getLogger(__name__)


class FakeEmployment(BaseProvider):
    """Faker Employement Info for Testing"""

    def employee_id(self) -> str:
        """Generates fake employee ID"""
        return nanoid.generate(size=20)


fake = faker.Faker()
fake.add_provider(FakeEmployment)


class Job(GID_SQLObject):
    """Job SQLObject

    Attributes:
        gID (TypeIDCol): global ID for the object
        attributes (JSONCol): JSON attributes for the object
                              Note: the DB isn't updated until the object is saved
                                    (no DB updates when individual fields are changed)
        description (StringCol): description of the object
        employeeID (StringCol): the person's employee ID
        location (StringCol): the job's location
        payGroup (StringCol): the job's pay group
        organization (ForeignKey): the DB ID of the employer
        person (ForeignKey): the DB ID of the employee
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    _gIDPrefix: str = "j"

    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)
    attributes: JSONCol = JSONCol(default=None)
    description: StringCol = StringCol(default=None)

    employeeID: StringCol = StringCol(default=fake.employee_id)
    location: StringCol = StringCol(default=None)
    payGroup: StringCol = StringCol(default=None)

    organization: ForeignKey = ForeignKey("Organization", cascade=True)
    person: ForeignKey = ForeignKey("Person", cascade=True)

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
