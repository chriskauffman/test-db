import logging

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import List, Optional, Union

from sqlobject import SQLObject  # type: ignore
from sqlobject.dberrors import DuplicateEntryError  # type: ignore

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
        cls,
        organization: Optional[Organization] = None,
        person: Optional[Person] = None,
        interactive: bool = True,
        **kwargs,
    ) -> Job:
        """Add a Job"""
        new_job = Job(organization=organization, person=person, **kwargs)
        if interactive:
            JobView(new_job).edit()
        print(new_job.gID)
        return new_job

    @classmethod
    def list(cls, jobs: Union[List[Job], SQLObject.select, None] = None, **kwargs):
        """List all jobs"""
        if jobs is None:
            jobs = Job.select(**kwargs)
        for job in jobs:
            JobView(job).view()

    def __init__(self, job: Job, **kwargs):
        super().__init__(**kwargs)
        self._job = job

    def delete(self, interactive: bool = True):
        """Delete the job"""
        if (
            interactive
            and input(f"Delete {self._job.visualID}? [y/n] ").strip().lower() != "y"
        ):
            return
        self._job.destroySelf()

    def edit(self):
        """Edit the job"""
        while True:
            try:
                self._job.gID = self._getTypeIDInput("gID", self._job.gID)
                break
            except DuplicateEntryError:
                print("gID already exists. Please enter a different gID.")
            except ValueError:
                print("Invalid gID. Check prefix and suffix. Please try again.")

        self._job.employeeID = self._getStrInput("Employee ID", self._job.employeeID)
        self._job.location = self._getStrInput(
            "Location", self._job.location, acceptNull=True
        )
        self._job.payGroup = self._getStrInput(
            "Pay Group", self._job.payGroup, acceptNull=True
        )

    def view(self):
        """Display brief details of the job"""
        print(f"{self._job.visualID}")

    def viewDetails(self):
        """Display brief details of the job"""
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
