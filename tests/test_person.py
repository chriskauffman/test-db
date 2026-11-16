from unittest.mock import Mock

import faker
import pytest
from typeid import TypeID

import test_db
from test_db._person import Person
from test_db._person_address import PersonAddress
from test_db._person_bank_account import PersonBankAccount
from test_db._person_debit_card import PersonDebitCard
from test_db._person_key_value import PersonKeyValue

fake = faker.Faker()


def test_init(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    assert test_person


def test_bulk_generation_uses_cached_values(temporary_db, monkeypatch):
    test_db.autoCreateDependents = False
    Person(
        firstName="First",
        lastName="Last",
        email="first.last@example.com",
        phoneNumber="555-0100",
        socialSecurityNumber="111-11-1111",
        connection=temporary_db.connection,
    )
    options = temporary_db.connection.tdbGlobalDatabaseOptions
    options.bulkAdd = True
    options.bulkUniqueValues.clear()
    first_names = iter(("First", "Fresh"))
    last_names = iter(("Last", "Name"))
    monkeypatch.setattr("test_db._person.fake.first_name", lambda: next(first_names))
    monkeypatch.setattr("test_db._person.fake.last_name", lambda: next(last_names))
    monkeypatch.setattr(
        Person,
        "selectBy",
        lambda *args, **kwargs: pytest.fail("bulk generation queried selectBy"),
    )
    select = Mock(wraps=Person.select)
    monkeypatch.setattr(Person, "select", select)

    try:
        person = Person(connection=temporary_db.connection)
    finally:
        options.bulkAdd = False
        options.bulkUniqueValues.clear()

    assert (person.firstName, person.lastName) == ("Fresh", "Name")
    assert select.call_count == 1


@pytest.mark.parametrize(
    "names",
    [
        {"firstName": "Jane"},
        {"lastName": "Doe"},
        {"firstName": "Jane", "lastName": None},
        {"firstName": None, "lastName": "Doe"},
    ],
)
@pytest.mark.parametrize("supplied_email", [False, True])
def test_partial_names(temporary_db, names, supplied_email):
    email = fake.unique.email() if supplied_email else None
    test_person = Person(**names, email=email, connection=temporary_db.connection)
    test_person.sync()

    assert test_person.firstName
    assert test_person.lastName
    for field, value in names.items():
        if value is not None:
            assert getattr(test_person, field) == value
    if supplied_email:
        assert test_person.email == email
    else:
        assert test_person.email.startswith(test_person.firstName[:1].lower())
        assert test_person.email.endswith("@example.com")


def test_string_gID(temporary_db):
    gID = TypeID("p")
    test_person = Person(gID=str(gID), connection=temporary_db.connection)
    assert test_person.gID == gID

    new_gID = TypeID("p")
    test_person.gID = str(new_gID)
    test_person.sync()
    assert test_person.gID == new_gID


def test__set_email(temporary_db):
    email = fake.email()
    test_person = Person(email=email, connection=temporary_db.connection)

    assert test_person.email == email


def test_autoCreateDependents_children(temporary_db):
    test_db.autoCreateDependents = False
    test_person = Person(connection=temporary_db.connection)
    assert len(test_person.addresses) == 0
    assert len(test_person.bankAccounts) == 0
    assert len(test_person.bankAccounts) == 0

    test_db.autoCreateDependents = True
    test_person = Person(connection=temporary_db.connection)
    assert len(test_person.addresses) == 1
    assert isinstance(test_person.addresses[0], PersonAddress)
    assert len(test_person.bankAccounts) == 1
    assert isinstance(test_person.bankAccounts[0], PersonBankAccount)
    assert len(test_person.debitCards) == 1
    assert isinstance(test_person.debitCards[0], PersonDebitCard)


def test_cascade_delete(temporary_db):
    test_db.autoCreateDependents = False
    test_person = Person(connection=temporary_db.connection)

    initial_count_of_all_person_addresses = PersonAddress.select(
        connection=temporary_db.connection
    ).count()
    for item in range(5):
        PersonAddress(
            person=test_person,
            connection=temporary_db.connection,
        )

    assert (
        PersonAddress.select(connection=temporary_db.connection).count()
        == initial_count_of_all_person_addresses + 5
    )
    assert (
        PersonAddress.select(
            PersonAddress.q.person == test_person.id,
            connection=temporary_db.connection,
        ).count()
        == 5
    )
    assert len(test_person.addresses) == 5

    initial_count_of_all_person_bank_accounts = PersonBankAccount.select(
        connection=temporary_db.connection
    ).count()
    for item in range(5):
        PersonBankAccount(
            person=test_person,
            connection=temporary_db.connection,
        )

    assert (
        PersonBankAccount.select(connection=temporary_db.connection).count()
        == initial_count_of_all_person_bank_accounts + 5
    )
    assert (
        PersonBankAccount.select(
            PersonBankAccount.q.person == test_person.id,
            connection=temporary_db.connection,
        ).count()
        == 5
    )
    assert len(test_person.bankAccounts) == 5

    initial_count_of_all_person_key_values = PersonKeyValue.select(
        connection=temporary_db.connection
    ).count()
    for item in range(5):
        PersonKeyValue(
            key=f"cascadeTest{item}",
            person=test_person,
            connection=temporary_db.connection,
        )

    assert (
        PersonKeyValue.select(connection=temporary_db.connection).count()
        == initial_count_of_all_person_key_values + 5
    )
    assert (
        PersonKeyValue.select(
            PersonKeyValue.q.person == test_person.id,
            connection=temporary_db.connection,
        ).count()
        == 5
    )
    assert len(test_person.keyValues) == 5

    test_person.destroySelf()
    assert (
        PersonAddress.select(connection=temporary_db.connection).count()
        == initial_count_of_all_person_addresses
    )
    assert (
        PersonAddress.select(
            PersonAddress.q.person == test_person.id,
            connection=temporary_db.connection,
        ).count()
        == 0
    )
    assert (
        PersonBankAccount.select(connection=temporary_db.connection).count()
        == initial_count_of_all_person_bank_accounts
    )
    assert (
        PersonBankAccount.select(
            PersonBankAccount.q.person == test_person.id,
            connection=temporary_db.connection,
        ).count()
        == 0
    )
    assert (
        PersonKeyValue.select(connection=temporary_db.connection).count()
        == initial_count_of_all_person_key_values
    )
    assert (
        PersonKeyValue.select(
            PersonKeyValue.q.person == test_person.id,
            connection=temporary_db.connection,
        ).count()
        == 0
    )
    test_db.autoCreateDependents = True
