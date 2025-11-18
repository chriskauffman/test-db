import logging

import faker
import nanoid
from sqlobject import MultipleJoin, RelatedJoin, SQLMultipleJoin, StringCol  # type: ignore

from test_db._full_sqlobject import FullSQLObject


fake = faker.Faker()
logger = logging.getLogger(__name__)


class Organization(FullSQLObject):
    """Organization SQLObject

    Attributes:
        name (StringCol): the name of the settings
        alternateID (StringCol): an alternate ID for the employer
        jobs (MultipleJoin): the jobs for the employer
        jobsSelect (SQLMultipleJoin): the jobs for the employer
        addresses (RelatedJoin): list of addresses related to the employer
        bankAccounts (RelatedJoin): list of bank accounts related to the employer
        debitCards (RelatedJoin): list of debit cards related to the employer
    """

    _gIDPrefix: str = "o"

    name: StringCol = StringCol(alternateID=True, default=fake.company)
    alternateID: StringCol = StringCol(alternateID=True, default=nanoid.generate)

    jobs: MultipleJoin = MultipleJoin("Job")
    jobsSelect: SQLMultipleJoin = SQLMultipleJoin("Job")

    addresses: RelatedJoin = RelatedJoin("Address")
    bankAccounts: RelatedJoin = RelatedJoin("BankAccount")
    debitCards: RelatedJoin = RelatedJoin("DebitCard")
