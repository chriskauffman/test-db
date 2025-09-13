import logging

import faker
from faker.providers import BaseProvider
import nanoid
from sqlobject import (  # type: ignore
    ForeignKey,
    StringCol,
)
from typeid import TypeID
from typeid.errors import (
    InvalidTypeIDStringException,
    PrefixValidationException,
    SuffixValidationException,
)

from ._test_db_sqlobject import TestDBSQLObject


logger = logging.getLogger(__name__)


def generate_job_gid() -> str:
    """Generate a TypeID

    Returns:
        str: new TypeID
    """
    return str(TypeID("j"))


def valid_job_gid(gid: str) -> bool:
    """Determines if a string is a valid global ID

    Args:
        gid (str):

    Returns:
        bool: True when valid
    """
    try:
        global_type_id = TypeID.from_string(gid)
    except InvalidTypeIDStringException:
        return False
    except PrefixValidationException:
        return False
    except SuffixValidationException:
        return False
    if global_type_id.prefix != "j":
        return False
    return True


class FakeEmployment(BaseProvider):
    """Faker Employement Info for Testing"""

    def employee_id(self) -> str:
        """Generates fake employee ID"""
        return nanoid.generate(size=20)


fake = faker.Faker()
fake.add_provider(FakeEmployment)


class Job(TestDBSQLObject):
    """Job SQLObject

    Attributes:
        employee_id (StringCol): the person's employee ID
        location (StringCol): the job's location
        pay_group (StringCol): the job's pay group
        employer (ForeignKey): the DB ID of the employer
        person (ForeignKey): the DB ID of the employee
    """

    _gid_prefix: str = "j"

    employee_id: StringCol = StringCol(default=fake.employee_id)
    location: StringCol = StringCol(default=None)
    pay_group: StringCol = StringCol(default=None)

    employer: ForeignKey = ForeignKey("Employer", cascade=True)
    person: ForeignKey = ForeignKey("Person", cascade=True)
