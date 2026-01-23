import logging

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Any, List, Union

from sqlobject import SQLObject  # type: ignore

from test_db import Job, JobKeyValue
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class JobKeyValueView(BaseView):
    """Secure key value views

    Args:
        job_key_value (JobKeyValue):
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def add(
        cls,
        job: Job,
        itemKey: str,
        itemValue: Any,
        interactive: bool = True,
    ) -> JobKeyValue:
        """Add a Secure Key Value to an entity"""
        return JobKeyValue(job=job, itemKey=itemKey, itemValue=itemValue)

    @classmethod
    def list(
        cls,
        key_values: Union[List[JobKeyValue], SQLObject.select, None] = None,
        **kwargs,
    ):
        """List all people"""
        if key_values is None:
            key_values = JobKeyValue.select(**kwargs)
        for key_value in key_values:
            JobKeyValueView(key_value).view()

    def __init__(self, job_key_value: JobKeyValue, **kwargs):
        super().__init__(**kwargs)
        self._job_key_value = job_key_value

    def edit(self):
        """Edit a key value"""
        self._job_key_value.itemValue = self._getStrInput(
            f"{self._job_key_value.itemKey}", self._job_key_value.itemValue
        )

    def view(self):
        """Display brief details of the key value"""
        print(f"{self._job_key_value.itemKey} = {self._job_key_value.itemValue}")
