import logging

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import List, Union

from sqlobject import SQLObject  # type: ignore

from test_db import KeyValue
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class KeyValueView(BaseView):
    """Key value views

    Args:
        key_value (KeyValue): The key value to view
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def add(cls, key: str, value: str, interactive: bool = True) -> KeyValue:
        """Add a key value"""
        return KeyValue(key=key, value=value)

    @classmethod
    def list(
        cls, key_values: Union[List[KeyValue], SQLObject.select, None] = None, **kwargs
    ):
        """List all people"""
        if key_values is None:
            key_values = KeyValue.select(**kwargs)
        for key_value in key_values:
            KeyValueView(key_value).view()

    def __init__(self, key_value: KeyValue, **kwargs):
        super().__init__(**kwargs)
        self._key_value = key_value

    def edit(self):
        """Edit a key value"""
        self._key_value.value = self._getStrInput(
            f"{self._key_value.key}", self._key_value.value
        )

    def view(self):
        """Display brief details of the key value"""
        print(f"{self._key_value.key} = {self._key_value.value}")
