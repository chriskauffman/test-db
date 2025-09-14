import logging

import faker
import nanoid
from sqlobject import MultipleJoin, SQLMultipleJoin, StringCol  # type: ignore

from ._test_db_sqlobject import TestDBSQLObject


fake = faker.Faker()
logger = logging.getLogger(__name__)


class Employer(TestDBSQLObject):
    """AppSettings SQLObject

    Attributes:
        name (StringCol): the name of the settings
        alternate_id (StringCol): an alternate ID for the employer
        jobs (MultipleJoin): the jobs for the employer
        jobs_select (SQLMultipleJoin): the jobs for the employer
    """

    _gid_prefix: str = "e"

    name: StringCol = StringCol(alternateID=True, default=fake.company)
    alternate_id: StringCol = StringCol(alternateID=True, default=nanoid.generate)

    jobs: MultipleJoin = MultipleJoin("Job")
    jobs_select: SQLMultipleJoin = SQLMultipleJoin("Job")
