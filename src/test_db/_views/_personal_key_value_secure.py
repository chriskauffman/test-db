import logging

from typing_extensions import Any, List, Union

from sqlobject import SQLObject  # type: ignore

from test_db import Person, PersonalKeyValueSecure
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class PersonalKeyValueSecureView(BaseView):
    """Debit card views

    Args:
        personal_key_value (PersonalKeyValueSecure):
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def add(
        cls, person: Person, key: str, value: Any, interactive: bool = True
    ) -> PersonalKeyValueSecure:
        """Add a bank account"""
        return PersonalKeyValueSecure(person=person, key=key, value=value)

    @classmethod
    def list(
        cls,
        key_values: Union[List[PersonalKeyValueSecure], SQLObject.select, None] = None,
    ):
        """List all people"""
        if key_values is None:
            key_values = PersonalKeyValueSecure.select()
        for key_value in key_values:
            PersonalKeyValueSecureView(key_value).view()

    def __init__(self, personal_key_value: PersonalKeyValueSecure, **kwargs):
        super().__init__(**kwargs)
        self._personal_key_value = personal_key_value

    def view(self):
        """Display brief details of the key value"""
        print(f"{self._personal_key_value.person.gID}, {self._personal_key_value.key}")

    def viewDetails(self):
        print(
            f"{self._personal_key_value.person.gID}, {self._personal_key_value.key} = {self._personal_key_value.value}"
        )
