import logging

from typing_extensions import Any, List, Union

from sqlobject import SQLObject  # type: ignore

from test_db import EntityKeyValue, Organization, Person
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class EntityKeyValueView(BaseView):
    """Secure key value views

    Args:
        personal_key_value (EntityKeyValue):
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def add(
        cls,
        entity: Union[Organization, Person],
        key: str,
        value: Any,
        interactive: bool = True,
    ) -> EntityKeyValue:
        """Add a Secure Key Value to an entity"""
        return EntityKeyValue(entity=entity, key=key, value=value)

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

    def __init__(self, personal_key_value: EntityKeyValue, **kwargs):
        super().__init__(**kwargs)
        self._personal_key_value = personal_key_value

    def view(self):
        """Display brief details of the key value"""
        print(f"{self._personal_key_value.entity.gID}, {self._personal_key_value.key}")

    def viewDetails(self):
        print(
            f"{self._personal_key_value.entity.gID}, {self._personal_key_value.key} = {self._personal_key_value.value}"
        )
