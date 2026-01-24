import faker

import test_db
from test_db._person import Person
from test_db._person_address import PersonAddress
from test_db._person_bank_account import PersonBankAccount
from test_db._person_debit_card import PersonDebitCard
from test_db._person_key_value import PersonKeyValue
from test_db._person_secure_key_value import PersonSecureKeyValue

fake = faker.Faker()


def test_init(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    assert test_person


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


def test_getKeyValueByKey(temporary_db):
    test_person = Person(connection=temporary_db.connection)
    test_key_value = test_person.getKeyValueByKey("test_getKeyValueByKey")

    assert isinstance(test_key_value, PersonKeyValue)
    assert test_key_value.itemKey == "test_getKeyValueByKey"

    test_key_value = test_person.getKeyValueByKey(
        "test_getKeyValueByKey_2", itemValue="testAccessToken"
    )

    assert test_key_value.itemValue == "testAccessToken"


def test_getSecureKeyValueByKey(temporary_db):
    test_db.databaseEncryptionKey = "a really good key"
    test_person = Person(connection=temporary_db.connection)
    test_secure_key_value = test_person.getSecureKeyValueByKey(
        "test_getSecureKeyValueByKey"
    )

    assert isinstance(test_secure_key_value, PersonSecureKeyValue)
    assert test_secure_key_value.itemKey == "test_getSecureKeyValueByKey"

    test_secure_key_value = test_person.getSecureKeyValueByKey(
        "test_getSecureKeyValueByKey_2", itemValue={"secret_data": "testSecretData"}
    )

    assert test_secure_key_value.itemValue == {"secret_data": "testSecretData"}


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
            itemKey=f"cascadeTest{item}",
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
