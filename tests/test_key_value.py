import uuid
from test_db._key_value import KeyValue
from test_db._job import Job
from test_db._job_key_value import JobKeyValue
from test_db._organization import Organization
from test_db._organization_key_value import OrganizationKeyValue
from test_db._person import Person
from test_db._person_key_value import PersonKeyValue


def key_value_validation(test_key_value, test_key, test_value):
    assert test_key_value.key == test_key
    assert test_key_value.value == test_value

    test_key_value.value = "updated_value"
    assert test_key_value.value == "updated_value"


def test_key_value(temporary_db):
    test_key = str(uuid.uuid4())
    test_key_value = KeyValue(
        key=test_key,
        value="test_value",
        connection=temporary_db.connection,
    )

    assert isinstance(test_key_value, KeyValue)
    key_value_validation(test_key_value, test_key, "test_value")


def test_job_key_value(temporary_db):
    test_job = Job(connection=temporary_db.connection)
    test_key_value = JobKeyValue(
        job=test_job,
        key="test_job_key_value",
        value="test_value",
        connection=temporary_db.connection,
    )

    assert isinstance(test_key_value, JobKeyValue)
    key_value_validation(test_key_value, "test_job_key_value", "test_value")


def test_organization_key_value(temporary_db):
    test_organization = Organization(connection=temporary_db.connection)
    test_key_value = OrganizationKeyValue(
        organization=test_organization,
        key="test_organization_key_value",
        value="test_value",
        connection=temporary_db.connection,
    )

    assert isinstance(test_key_value, OrganizationKeyValue)
    key_value_validation(test_key_value, "test_organization_key_value", "test_value")


def test_person_key_value(temporary_db):
    test_person = Person(connection=temporary_db.connection)
    test_key_value = PersonKeyValue(
        person=test_person,
        key="test_person_key_value",
        value="test_value",
        connection=temporary_db.connection,
    )

    assert isinstance(test_key_value, PersonKeyValue)
    key_value_validation(test_key_value, "test_person_key_value", "test_value")
