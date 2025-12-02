import logging

from typing_extensions import List, Optional, Union

from sqlobject import SQLObject  # type: ignore

from test_db import Job, Organization, Person
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class JobView(BaseView):
    """Debit card views

    Args:
        job (Job): The job to view
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def add(
        self,
        organization: Optional[Organization] = None,
        person: Optional[Person] = None,
    ) -> Job:
        """Add a Job"""
        new_job = Job(organization=organization, person=person)
        if BaseView.interactive:
            JobView(new_job).edit()
        print(new_job.gID)
        return new_job

    @classmethod
    def list(cls, jobs: Union[List[Job], SQLObject.select, None] = None):
        """List all jobs"""
        if jobs is None:
            jobs = Job.select()
        for job in jobs:
            JobView(job).view()

    def __init__(self, job: Job, **kwargs):
        super().__init__(**kwargs)
        self._job = job

    def edit(self):
        """Edit the job"""
        pass

    def view(self):
        """Display brief details of the debit card"""
        print(f"{self._job.gID}, {self._job.employeeID}, {self._job.payGroup}")

    def viewDetails(self):
        """Display brief details of the debit card"""
        print(f"\nJob ID: {self._job.gID}")
        print(f"\nEmployee ID:\t{self._job.employeeID}")
        print(f"Location:\t{self._job.location}")
        print(f"Pay Group:\t{self._job.payGroup}")
        if self._job.organization:
            print(
                f"\nEmployer:\t{self._job.organization.name}, {self._job.organization.gID}"
            )
        else:
            print(f"\nEmployer:\t{self._job.organization}")
        if self._job.person:
            print(
                f"Employee:\t{self._job.person.firstName} {self._job.person.lastName}, {self._job.person.gID}"
            )
        else:
            print(f"Employee:\t{self._job.person}")
        print(f"Created At:\t{self._job.createdAt}")
        print(f"Updated At:\t{self._job.updatedAt}")
