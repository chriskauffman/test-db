import logging

import faker
from sqlobject import (  # type: ignore
    DateTimeCol,
    MultipleJoin,
    SQLMultipleJoin,
    StringCol,
    SQLObject,
    SQLObjectNotFound,
)

from typeid import TypeID

from test_db._gid import validGID
from test_db._type_id_col import TypeIDCol
from test_db._organization_key_value import OrganizationKeyValue


fake = faker.Faker()
logger = logging.getLogger(__name__)


class Organization(SQLObject):
    """Organization SQLObject

    Attributes:
        gID (TypeIDCol): global ID for the object
        name (StringCol): the name of the settings
        description (StringCol): description of the entity
        employerIdentificationNumber (StringCol): the organization's EIN
        phoneNumber (StringCol): the entity's phone number
        addresses (MultipleJoin):
        addressesSelect (SQLMultipleJoin):
        bankAccounts (MultipleJoin): list of bank accounts related to the entity
        bankAccountsSelect (SQLMultipleJoin):
        jobs (MultipleJoin): the jobs for the organization
        jobsSelect (SQLMultipleJoin): the jobs for the organization
        keyValues (MultipleJoin):
        keyValuesSelect (SQLMultipleJoin):
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    _gIDPrefix: str = "o"

    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)
    name: StringCol = StringCol(alternateID=True, default=fake.company)
    description: StringCol = StringCol(default=None)
    employerIdentificationNumber: StringCol = StringCol(
        alternateID=True, default=fake.ein
    )
    phoneNumber: StringCol = StringCol(default=fake.basic_phone_number)

    addresses: MultipleJoin = MultipleJoin("OrganizationAddress")
    addressesSelect: SQLMultipleJoin = SQLMultipleJoin("OrganizationAddress")
    bankAccounts: MultipleJoin = MultipleJoin("OrganizationBankAccount")
    bankAccountsSelect: SQLMultipleJoin = SQLMultipleJoin("OrganizationBankAccount")
    jobs: MultipleJoin = MultipleJoin("Job")
    jobsSelect: SQLMultipleJoin = SQLMultipleJoin("Job")
    keyValues: MultipleJoin = MultipleJoin("OrganizationKeyValue")
    keyValuesSelect: SQLMultipleJoin = SQLMultipleJoin("OrganizationKeyValue")

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    @property
    def visualID(self):
        return f"{self.gID} {self.name} {self.externalID}"

    def _set_gID(self, value):
        if value:
            if validGID(value, self._gIDPrefix):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(TypeID(self._gIDPrefix))

    def getKeyValueByKey(self, key: str, **kwargs) -> OrganizationKeyValue:
        """Find and create an OrganizationKeyValue

        Args:
            key (str): name of the OrganizationKeyValue
            **kwargs:

        Returns:
            OrganizationKeyValue:
        """
        try:
            return self.keyValuesSelect.filter(
                OrganizationKeyValue.q.itemKey == key
            ).getOne()
        except SQLObjectNotFound:
            return OrganizationKeyValue(
                connection=self._connection, organization=self.id, itemKey=key, **kwargs
            )
