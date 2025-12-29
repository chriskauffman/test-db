import logging

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Any, List, Union

from sqlobject import SQLObject  # type: ignore

from test_db import EntityKeyValue, Organization, Person
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class EntityKeyValueView(BaseView):
    """Secure key value views

    Args:
        entity_key_value (EntityKeyValue):
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def add(
        cls,
        entity: Union[Organization, Person],
        itemKey: str,
        itemValue: Any,
        interactive: bool = True,
    ) -> EntityKeyValue:
        """Add a Secure Key Value to an entity"""
        return EntityKeyValue(entity=entity, itemKey=itemKey, itemValue=itemValue)

    @classmethod
    def list(
        cls,
        key_values: Union[List[EntityKeyValue], SQLObject.select, None] = None,
        **kwargs,
    ):
        """List all people"""
        if key_values is None:
            key_values = EntityKeyValue.select(**kwargs)
        for key_value in key_values:
            EntityKeyValueView(key_value).view()

    def __init__(self, entity_key_value: EntityKeyValue, **kwargs):
        super().__init__(**kwargs)
        self._entity_key_value = entity_key_value

    def edit(self):
        """Edit a key value"""
        self._entity_key_value.itemValue = self._getStrInput(
            f"{self._entity_key_value.itemKey}", self._entity_key_value.itemValue
        )

    def view(self):
        """Display brief details of the key value"""
        print(f"{self._entity_key_value.itemKey} = {self._entity_key_value.itemValue}")
