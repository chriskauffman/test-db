import logging

import faker

from sqlobject import JSONCol, RelatedJoin, SQLRelatedJoin, StringCol  # type: ignore
from sqlobject.inheritance import InheritableSQLObject  # type: ignore


fake = faker.Faker()
logger = logging.getLogger(__name__)


class Entity(InheritableSQLObject):
    """Base Entity SQLObject

    This is a base class for Organization and Person in the test database.
    It can be extended to include common attributes or methods that should
    be shared across all entity types.

    Attributes:
        attributes (JSONCol): JSON attributes for the object. **Note** - The DB
                              isn't updated until the object is saved (no DB updates
                              when individual fields are changed)
        description (StringCol): description of the entity
        phoneNumber (StringCol): the entity's phone number
        addresses (RelatedJoin): list of addresses related to the entity
        addressesSelect (SQLRelatedJoin):
        bankAccounts (RelatedJoin): list of bank accounts related to the entity
        bankAccountsSelect (SQLRelatedJoin):
        debitCards (RelatedJoin): list of debit cards related to the entity
        debitCardsSelect (SQLRelatedJoin):
    """

    attributes: JSONCol = JSONCol(default=None)
    description: StringCol = StringCol(default=None)
    phoneNumber: StringCol = StringCol(default=fake.basic_phone_number)

    addresses: RelatedJoin = RelatedJoin(
        "Address", intermediateTable="address_entity", createRelatedTable=False
    )
    addressesSelect: SQLRelatedJoin = SQLRelatedJoin(
        "Address", intermediateTable="address_entity", createRelatedTable=False
    )
    bankAccounts: RelatedJoin = RelatedJoin(
        "BankAccount", intermediateTable="bank_account_entity", createRelatedTable=False
    )
    bankAccountsSelect: SQLRelatedJoin = SQLRelatedJoin(
        "BankAccount", intermediateTable="bank_account_entity", createRelatedTable=False
    )
    debitCards: RelatedJoin = RelatedJoin(
        "DebitCard", intermediateTable="debit_card_entity", createRelatedTable=False
    )
    debitCardsSelect: SQLRelatedJoin = SQLRelatedJoin(
        "DebitCard", intermediateTable="debit_card_entity", createRelatedTable=False
    )
