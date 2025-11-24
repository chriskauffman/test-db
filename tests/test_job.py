import pytest

from sqlobject.dberrors import DuplicateEntryError

from test_db._job import Job
from test_db._organization import Organization
from test_db._person import Person


def test_init(temporary_db):
    test_job = Job(connection=temporary_db.connection)

    assert test_job
    assert isinstance(test_job, Job)
    assert isinstance(test_job.organization, Organization)
    assert isinstance(test_job.person, Person)


def test_duplicate_employee_id(temporary_db):
    test_organization = Organization(connection=temporary_db.connection)
    Job(
        employeeID="test_duplicate_employee_id",
        organization=test_organization,
        connection=temporary_db.connection,
    )

    assert Job(
        employeeID="test_employee_id",
        organization=test_organization,
        connection=temporary_db.connection,
    )

    # Should get an error if I try to add a job with the same employee ID
    with pytest.raises(DuplicateEntryError):
        Job(
            employeeID="test_duplicate_employee_id",
            organization=test_organization,
            connection=temporary_db.connection,
        )
