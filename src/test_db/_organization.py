import logging

import faker
import nanoid
from sqlobject import (  # type: ignore
    DateTimeCol,
    JSONCol,
    MultipleJoin,
    RelatedJoin,
    SQLMultipleJoin,
    StringCol,
)  # type: ignore
import sqlobject.sqlbuilder  # type: ignore

from test_db._type_id_col import TypeIDCol
from test_db._gid_sqlobject import GID_SQLObject


fake = faker.Faker()
logger = logging.getLogger(__name__)


class Organization(GID_SQLObject):
    """Organization SQLObject

    Attributes:
        gID (TypeIDCol): global ID for the object
        attributes (JSONCol): JSON attributes for the object
                              Note: the DB isn't updated until the object is saved
                                    (no DB updates when individual fields are changed)
        description (StringCol): description of the object
        name (StringCol): the name of the settings
        alternateID (StringCol): an alternate ID for the employer
        jobs (MultipleJoin): the jobs for the employer
        jobsSelect (SQLMultipleJoin): the jobs for the employer
        addresses (RelatedJoin): list of addresses related to the employer
        bankAccounts (RelatedJoin): list of bank accounts related to the employer
        debitCards (RelatedJoin): list of debit cards related to the employer
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    _gIDPrefix: str = "o"

    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)
    attributes: JSONCol = JSONCol(default=None)
    description: StringCol = StringCol(default=None)

    name: StringCol = StringCol(alternateID=True, default=fake.company)
    alternateID: StringCol = StringCol(alternateID=True, default=nanoid.generate)

    jobs: MultipleJoin = MultipleJoin("Job")
    jobsSelect: SQLMultipleJoin = SQLMultipleJoin("Job")

    addresses: RelatedJoin = RelatedJoin("Address")
    bankAccounts: RelatedJoin = RelatedJoin("BankAccount")
    debitCards: RelatedJoin = RelatedJoin("DebitCard")

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
