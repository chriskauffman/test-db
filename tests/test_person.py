import random

import faker
import pytest
import sqlobject  # type: ignore

import test_db as db
from test_db._bank_account import PersonalBankAccount
from test_db._database_controller import DatabaseController
from test_db._debit_card import PersonalDebitCard
from test_db._oauth2_token import PersonalOAuth2Token
from test_db._person import Person
from test_db._settings import PersonalKeyJson


fake = faker.Faker()


def test_init(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    assert test_person


def test_deleteByEmail(temporary_db):
    test_email = fake.email()
    test_person = Person(email=test_email, connection=temporary_db.connection)

    assert test_person

    Person.deleteByEmail(test_email, connection=temporary_db.connection)

    with pytest.raises(sqlobject.main.SQLObjectNotFound):
        Person.byEmail(test_email, connection=temporary_db.connection)


def test_findByEmail(temporary_db):
    test_email = fake.email()
    test_person = Person(email=test_email, connection=temporary_db.connection)

    assert test_person
    assert Person.findByEmail(test_email, connection=temporary_db.connection)


def test_list(tmp_path_factory):
    test_db = DatabaseController(
        tmp_path_factory.mktemp("data") / "test_list.sqlite", create=True
    )

    number_of_users = random.randint(1, 10)
    for i in range(number_of_users):
        Person(connection=test_db.connection)

    assert len(Person.list(connection=test_db.connection)) == number_of_users


def test_as_dict(temporary_db):
    assert isinstance(Person(connection=temporary_db.connection).as_dict, dict)


def test_byEmail(temporary_db):
    test_email = fake.email()

    test_person = Person(email=test_email, connection=temporary_db.connection)

    assert test_person
    assert Person.byEmail(test_email, connection=temporary_db.connection)


def test__set_email(temporary_db):
    test_person = Person(
        email="test__set_email@example.com", connection=temporary_db.connection
    )

    assert test_person.email == "test__set_email@example.com"


def test_getBankAccountByName(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    test_bank_account = test_person.getBankAccountByName("test1")

    assert isinstance(test_bank_account, PersonalBankAccount)
    assert test_bank_account.name == "test1"

    test_bank_account = test_person.getBankAccountByName(
        "test2", routingNumber="987897897"
    )

    assert test_bank_account.routingNumber == "987897897"


def test_getDebitCardByName(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    test_debit_card = test_person.getDebitCardByName("test1")

    assert isinstance(test_debit_card, PersonalDebitCard)
    assert test_debit_card.name == "test1"

    test_debit_card = test_person.getDebitCardByName("test2", cvv="123")

    assert test_debit_card.cvv == "123"


def test_getJobByEmployerId(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    # Test automatic creation of employer
    test_job = test_person.getJobByEmployerId(22771)
    assert isinstance(test_job, db.Job)
    assert isinstance(
        db.Employer.get(22771, connection=temporary_db.connection), db.Employer
    )

    # Test Creating an employer and using that for the job
    test_employer = db.Employer(connection=temporary_db.connection, name="TestEmployer")
    test_job = test_person.getJobByEmployerId(test_employer.id)
    assert isinstance(test_job, db.Job)
    assert test_job.employer.name == "TestEmployer"


def test_getJobByEmployerAlternateId(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    # Test automatic creation of employer
    test_job = test_person.getJobByEmployerAlternateId("employer22771")
    assert isinstance(test_job, db.Job)
    assert isinstance(
        db.Employer.byAlternateID("employer22771", connection=temporary_db.connection),
        db.Employer,
    )

    # Test Creating an employer and using that for the job
    db.Employer(connection=temporary_db.connection, alternateID="employer22772")
    test_job = test_person.getJobByEmployerAlternateId("employer22772")
    assert isinstance(test_job, db.Job)
    assert test_job.employer.alternateID == "employer22772"


def test_getOAuth2TokenByClientId(temporary_db):
    test_person = Person(connection=temporary_db.connection)
    db.databaseEncryptionKey = "a really good key"

    test_oauth2_token = test_person.getOAuth2TokenByClientId("testClientId1")

    assert isinstance(test_oauth2_token, PersonalOAuth2Token)
    assert test_oauth2_token.clientID == "testClientId1"

    test_oauth2_token = test_person.getOAuth2TokenByClientId(
        "testClientId2", token={"access_token": "testAccessToken"}
    )

    assert test_oauth2_token.token == {"access_token": "testAccessToken"}


def test_getPersonalKeyJsonsByKey(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    test_person_app_settings = test_person.getPersonalKeyJsonsByKey(
        "test_getPersonalKeyJsonsByKey"
    )

    assert isinstance(test_person_app_settings, PersonalKeyJson)
    assert test_person_app_settings.key == "test_getPersonalKeyJsonsByKey"

    test_person_app_settings = test_person.getPersonalKeyJsonsByKey(
        "test_getPersonalKeyJsonsByKey_2",
        value={"default_bank_account_id": "testUUID"},
    )

    test_person_app_settings = test_person.getPersonalKeyJsonsByKey(
        "test_getPersonalKeyJsonsByKey_2"
    )

    assert test_person_app_settings.value["default_bank_account_id"] == "testUUID"


def test_resetAuth(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    assert len(test_person.oauth2Tokens) == 0

    test_person.getOAuth2TokenByClientId("testClientId1")

    assert len(test_person.oauth2Tokens) == 1

    test_person.resetAuth()

    assert len(test_person.oauth2Tokens) == 0


def test_resetPersonalKeyValues(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    assert len(test_person.PersonalKeyValues) == 0

    test_person.getPersonalKeyValuesByKey("test_resetPersonalKeyValues")

    assert len(test_person.PersonalKeyValues) == 1

    test_person.resetPersonalKeyValues()

    assert len(test_person.PersonalKeyValues) == 0


def test_resetPersonalKeyJsons(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    assert len(test_person.PersonalKeyJsons) == 0

    test_person.getPersonalKeyJsonsByKey("test_resetPersonalKeyJsons")

    assert len(test_person.PersonalKeyJsons) == 1

    test_person.resetPersonalKeyJsons()

    assert len(test_person.PersonalKeyJsons) == 0
