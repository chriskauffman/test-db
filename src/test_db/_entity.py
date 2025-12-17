import logging

import faker

from sqlobject import (  # type: ignore
    JSONCol,
    MultipleJoin,
    RelatedJoin,
    SQLMultipleJoin,
    SQLObjectNotFound,
    SQLRelatedJoin,
    StringCol,
)
from sqlobject.inheritance import InheritableSQLObject  # type: ignore

from test_db._entity_key_value import EntityKeyValue
from test_db._entity_secure_key_value import EntitySecureKeyValue


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
        keyValues (MultipleJoin):
        keyValuesSelect (SQLMultipleJoin):
        secureKeyValues (MultipleJoin):
        secureKeyValuesSelect (SQLMultipleJoin):
    """

    attributes: JSONCol = JSONCol(default={}, notNull=True)
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

    keyValues: MultipleJoin = MultipleJoin("EntityKeyValue")
    keyValuesSelect: SQLMultipleJoin = SQLMultipleJoin("EntityKeyValue")

    secureKeyValues: MultipleJoin = MultipleJoin("EntitySecureKeyValue")
    secureKeyValuesSelect: SQLMultipleJoin = SQLMultipleJoin("EntitySecureKeyValue")

    def getKeyValueByKey(self, key: str, **kwargs) -> EntityKeyValue:
        """Find and create an EntityKeyValue

        Args:
            key (str): name of the EntityKeyValue
            **kwargs:

        Returns:
            EntityKeyValue:
        """
        try:
            return self.keyValuesSelect.filter(EntityKeyValue.q.key == key).getOne()
        except SQLObjectNotFound:
            return EntityKeyValue(
                connection=self._connection, entity=self.id, key=key, **kwargs
            )

    def getSecureKeyValueByKey(self, key: str, **kwargs) -> EntitySecureKeyValue:
        """Find and create an EntitySecureKeyValue

        Args:
            key (str): name of the EntitySecureKeyValue
            **kwargs:

        Returns:
            EntitySecureKeyValue:
        """
        try:
            return self.secureKeyValuesSelect.filter(
                EntitySecureKeyValue.q.key == key
            ).getOne()
        except SQLObjectNotFound:
            return EntitySecureKeyValue(
                connection=self._connection, entity=self.id, key=key, **kwargs
            )
