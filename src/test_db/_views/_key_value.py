import logging

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import List, Union

from sqlobject import SQLObject  # type: ignore

from test_db import (
    JobKeyValue,
    OrganizationKeyValue,
    PersonKeyValue,
    PersonSecureKeyValue,
)
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class KeyValueView(BaseView):
    """Key value views

    Args:
        key_value (Union[JobKeyValue, OrganizationKeyValue, PersonKeyValue, PersonSecureKeyValue]): The key value to view
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def list(
        cls,
        key_values: Union[
            List[JobKeyValue],
            List[OrganizationKeyValue],
            List[PersonKeyValue],
            List[PersonSecureKeyValue],
            SQLObject.select,
        ],
        **kwargs,
    ):
        """List all people"""
        try:
            for key_value in key_values:
                KeyValueView(key_value).view()
        except ValueError:
            print("Unable to decrypt - check database encryption key")

    def __init__(
        self,
        key_value: Union[
            JobKeyValue, OrganizationKeyValue, PersonKeyValue, PersonSecureKeyValue
        ],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._key_value = key_value

    def edit(self):
        """Edit a key value"""
        try:
            if self._key_value.value is None or isinstance(self._key_value.value, str):
                self._key_value.value = self._getStrInput(
                    f"{self._key_value.key}", self._key_value.value
                )
            else:
                raise NotImplementedError("Only string values are currently supported")
        except ValueError:
            print("Unable to decrypt - check database encryption key")

    def view(self):
        """Display brief details of the key value"""
        try:
            print(self._key_value.visualID)
        except ValueError:
            print("Unable to decrypt - check database encryption key")

    def viewDetails(self):
        """Display detailed information of the key value"""
        print(f"Owner ID: {self._key_value.ownerID}")
        try:
            print(f"Key: {self._key_value.key}")
            print(f"Value: {self._key_value.value}")
        except ValueError:
            print("Unable to decrypt - check database encryption key")
