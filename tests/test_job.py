from test_db._job import Job
from test_db._organization import Organization
from test_db._person import Person


def test_init(temporary_db):
    test_job = Job(connection=temporary_db.connection)

    assert test_job
    assert isinstance(test_job, Job)
    assert isinstance(test_job.organization, Organization)
    assert isinstance(test_job.person, Person)
