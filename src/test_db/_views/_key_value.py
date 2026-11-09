import logging

from sqlobject.sresults import SelectResults

from test_db import (
    JobKeyValue,
    OrganizationKeyValue,
    PersonKeyValue,
)
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class KeyValueView(BaseView):
    """Key value views

    Args:
        key_value (JobKeyValue | OrganizationKeyValue | PersonKeyValue): The key value to view
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def list(
        cls,
        key_values: list[JobKeyValue]
        | list[OrganizationKeyValue]
        | list[PersonKeyValue]
        | SelectResults,
        **kwargs,
    ):
        """List all key values"""
        for key_value in key_values:
            KeyValueView(key_value).view()

    def __init__(
        self,
        key_value: JobKeyValue | OrganizationKeyValue | PersonKeyValue,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._key_value = key_value

    def edit(self):
        """Edit a key value"""
        if self._key_value.value is None or isinstance(self._key_value.value, str):
            self._key_value.value = self._getStrInput(
                f"{self._key_value.key}", self._key_value.value, acceptNull=True
            )
        else:
            raise NotImplementedError("Only string values are currently supported")

    def view(self):
        """Display brief details of the key value"""
        print(self._key_value.visualID, str(self._key_value.value)[:20])

    def viewDetails(self):
        """Display detailed information of the key value"""
        print(f"Owner ID: {self._key_value.ownerID}")
        print(f"Key: {self._key_value.key}")
        print(f"Value: {self._key_value.value}")
