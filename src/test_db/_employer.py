import logging

import faker
from sqlobject import StringCol  # type: ignore

from ._test_db_sqlobject import TestDBSQLObject


fake = faker.Faker()
logger = logging.getLogger(__name__)


class Employer(TestDBSQLObject):
    """AppSettings SQLObject

    Attributes:
        name (StringCol): the name of the settings
        alternate_id (StringCol): an alternate ID for the employer
    """

    _gid_prefix: str = "e"

    name: StringCol = StringCol(alternateID=True, default=fake.company)
    alternate_id: StringCol = StringCol(default=None)
