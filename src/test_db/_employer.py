import logging

import faker
import nanoid
from sqlobject import MultipleJoin, SQLMultipleJoin, StringCol  # type: ignore

from ._test_db_sqlobject import FullSQLObject


fake = faker.Faker()
logger = logging.getLogger(__name__)


class Employer(FullSQLObject):
    """AppSettings SQLObject

    Attributes:
        name (StringCol): the name of the settings
        alternateID (StringCol): an alternate ID for the employer
        jobs (MultipleJoin): the jobs for the employer
        jobsSelect (SQLMultipleJoin): the jobs for the employer
    """

    _gIDPrefix: str = "e"

    name: StringCol = StringCol(alternateID=True, default=fake.company)
    alternateID: StringCol = StringCol(alternateID=True, default=nanoid.generate)

    jobs: MultipleJoin = MultipleJoin("Job")
    jobsSelect: SQLMultipleJoin = SQLMultipleJoin("Job")
