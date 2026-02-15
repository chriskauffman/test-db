import pytest
import uuid

from sqlobject.dberrors import DuplicateEntryError

import test_db
from test_db._job import Job
from test_db._job_key_value import JobKeyValue
from test_db._organization import Organization
from test_db._person import Person


def test_init(temporary_db):
    test_job = Job(connection=temporary_db.connection)

    assert test_job
    assert isinstance(test_job, Job)
    assert isinstance(test_job.organization, Organization)
    assert isinstance(test_job.person, Person)


def test_autoCreateDependents_children(temporary_db):
    test_db.autoCreateDependents = False
    test_job = Job(connection=temporary_db.connection)
    assert test_job.organization is None
    assert test_job.person is None

    test_db.autoCreateDependents = True
    test_job = Job(connection=temporary_db.connection)
    assert isinstance(test_job.organization, Organization)
    assert isinstance(test_job.person, Person)


def test_duplicate_employee_id(temporary_db):
    test_organization = Organization(connection=temporary_db.connection)
    employee_id = str(uuid.uuid4())
    Job(
        employeeID=employee_id,
        organization=test_organization,
        connection=temporary_db.connection,
    )

    # Should get an error if I try to add a job with the same employee ID
    with pytest.raises(DuplicateEntryError):
        Job(
            employeeID=employee_id,
            organization=test_organization,
            connection=temporary_db.connection,
        )


def test_byOrganizationAndPerson(temporary_db):
    test_job = Job(connection=temporary_db.connection)

    assert (
        Job.byOrganizationAndPerson(
            test_job.organization, test_job.person, connection=temporary_db.connection
        )
        is test_job
    )


def test_getKeyValueByKey(temporary_db):
    test_job = Job(connection=temporary_db.connection)
    test_key_value = test_job.getKeyValueByKey("test_getKeyValueByKey")

    assert isinstance(test_key_value, JobKeyValue)
    assert test_key_value.key == "test_getKeyValueByKey"

    test_key_value = test_job.getKeyValueByKey(
        "test_getKeyValueByKey_2", value="test_getKeyValueByKey_value"
    )

    assert test_key_value.value == "test_getKeyValueByKey_value"


def test_cascade_delete(temporary_db):
    test_job = Job(connection=temporary_db.connection)

    initial_count_of_all_job_key_values = JobKeyValue.select(
        connection=temporary_db.connection
    ).count()
    for item in range(5):
        JobKeyValue(
            key=f"cascadeTest{item}",
            job=test_job,
            connection=temporary_db.connection,
        )

    assert (
        JobKeyValue.select(connection=temporary_db.connection).count()
        == initial_count_of_all_job_key_values + 5
    )
    assert (
        JobKeyValue.select(
            JobKeyValue.q.job == test_job.id,
            connection=temporary_db.connection,
        ).count()
        == 5
    )
    assert len(test_job.keyValues) == 5

    test_job.destroySelf()
    assert (
        JobKeyValue.select(connection=temporary_db.connection).count()
        == initial_count_of_all_job_key_values
    )
    assert (
        JobKeyValue.select(
            JobKeyValue.q.job == test_job.id,
            connection=temporary_db.connection,
        ).count()
        == 0
    )
