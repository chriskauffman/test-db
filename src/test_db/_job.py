import logging

import faker
from faker.providers import BaseProvider
import nanoid
from sqlobject import (  # type: ignore
    ForeignKey,
    StringCol,
)

from ._test_db_sqlobject import FullSQLObject


logger = logging.getLogger(__name__)


class FakeEmployment(BaseProvider):
    """Faker Employement Info for Testing"""

    def employee_id(self) -> str:
        """Generates fake employee ID"""
        return nanoid.generate(size=20)


fake = faker.Faker()
fake.add_provider(FakeEmployment)


class Job(FullSQLObject):
    """Job SQLObject

    Attributes:
        employeeID (StringCol): the person's employee ID
        location (StringCol): the job's location
        payGroup (StringCol): the job's pay group
        employer (ForeignKey): the DB ID of the employer
        person (ForeignKey): the DB ID of the employee
    """

    _gIDPrefix: str = "j"

    employeeID: StringCol = StringCol(default=fake.employee_id)
    location: StringCol = StringCol(default=None)
    payGroup: StringCol = StringCol(default=None)

    employer: ForeignKey = ForeignKey("Employer", cascade=True)
    person: ForeignKey = ForeignKey("Person", cascade=True)
