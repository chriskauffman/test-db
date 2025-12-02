import logging

import faker
import nanoid
from sqlobject import (  # type: ignore
    DateTimeCol,
    MultipleJoin,
    SQLMultipleJoin,
    StringCol,
)

from typeid import TypeID

from test_db._entity import Entity
from test_db._gid import validGID
from test_db._type_id_col import TypeIDCol


fake = faker.Faker()
logger = logging.getLogger(__name__)


class Organization(Entity):
    """Organization SQLObject

    Attributes:
        gID (TypeIDCol): global ID for the object
        name (StringCol): the name of the settings
        employerIdentificationNumber (StringCol): the organization's EIN
        externalID (StringCol): an alternate ID for the organization
        jobs (MultipleJoin): the jobs for the organization
        jobsSelect (SQLMultipleJoin): the jobs for the organization
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    _gIDPrefix: str = "o"

    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)

    name: StringCol = StringCol(alternateID=True, default=fake.company)
    employerIdentificationNumber: StringCol = StringCol(
        alternateID=True, default=fake.ein
    )
    externalID: StringCol = StringCol(alternateID=True, default=nanoid.generate)

    jobs: MultipleJoin = MultipleJoin("Job")
    jobsSelect: SQLMultipleJoin = SQLMultipleJoin("Job")

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    def _set_gID(self, value):
        if value:
            if validGID(value, self._gIDPrefix):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(TypeID(self._gIDPrefix))
