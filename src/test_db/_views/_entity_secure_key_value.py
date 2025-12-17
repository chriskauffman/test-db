import logging

from typing_extensions import Any, List, Union

from sqlobject import SQLObject  # type: ignore

from test_db import EntitySecureKeyValue, Organization, Person
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class EntitySecureKeyValueView(BaseView):
    """Secure key value views

    Args:
        personal_key_value (EntitySecureKeyValue):
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
    ) -> EntitySecureKeyValue:
        """Add a Secure Key Value to an entity"""
        return EntitySecureKeyValue(entity=entity, key=key, value=value)

    @classmethod
    def list(
        cls,
        key_values: Union[List[EntitySecureKeyValue], SQLObject.select, None] = None,
        **kwargs,
    ):
        """List all people"""
        if key_values is None:
            key_values = EntitySecureKeyValue.select(**kwargs)
        for key_value in key_values:
            EntitySecureKeyValueView(key_value).view()

    def __init__(self, personal_key_value: EntitySecureKeyValue, **kwargs):
        super().__init__(**kwargs)
        self._personal_key_value = personal_key_value

    def view(self):
        """Display brief details of the key value"""
        print(f"{self._personal_key_value.entity.gID}, {self._personal_key_value.key}")

    def viewDetails(self):
        print(
            f"{self._personal_key_value.entity.gID}, {self._personal_key_value.key} = {self._personal_key_value.value}"
        )
