import faker

import test_db as db
from test_db._address import Address
from test_db._bank_account import BankAccount
from test_db._debit_card import DebitCard

# from test_db._oauth2_token import PersonalOAuth2Token
from test_db._person import Person
from test_db._personal_key_value_secure import PersonalKeyValueSecure


fake = faker.Faker()


def test_init(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    assert test_person


def test__set_email(temporary_db):
    test_person = Person(
        email="test__set_email@example.com", connection=temporary_db.connection
    )

    assert test_person.email == "test__set_email@example.com"


def test_getPersonalKeyValueSecureByKey(temporary_db):
    test_person = Person(connection=temporary_db.connection)
    db.databaseEncryptionKey = "a really good key"

    test_oauth2_token = test_person.getPersonalKeyValueSecureByKey("testClientId1")

    assert isinstance(test_oauth2_token, PersonalKeyValueSecure)
    assert test_oauth2_token.key == "testClientId1"

    test_oauth2_token = test_person.getPersonalKeyValueSecureByKey(
        "testClientId2", value={"access_token": "testAccessToken"}
    )

    assert test_oauth2_token.value == {"access_token": "testAccessToken"}


def test_locate_related_objects(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    test_address = Address(connection=temporary_db.connection, name="test_address")
    test_person.addAddress(test_address)
    test_person.addAddress(
        Address(connection=temporary_db.connection, name="other_address")
    )
    assert (
        next(
            (item for item in test_person.addresses if item.name == "test_address"),
            None,
        )
        is test_address
    )
    assert (
        test_person.addressesSelect.filter(Address.q.name == "test_address").getOne()
        is test_address
    )

    test_bank_account = BankAccount(
        connection=temporary_db.connection, name="test_bank_account"
    )
    test_person.addBankAccount(test_bank_account)
    test_person.addBankAccount(
        BankAccount(connection=temporary_db.connection, name="other_bank_account")
    )
    assert (
        next(
            (
                item
                for item in test_person.bankAccounts
                if item.name == "test_bank_account"
            ),
            None,
        )
        is test_bank_account
    )
    assert (
        test_person.bankAccountsSelect.filter(
            BankAccount.q.name == "test_bank_account"
        ).getOne()
        is test_bank_account
    )

    test_debit_card = DebitCard(
        connection=temporary_db.connection, name="test_debit_card"
    )
    test_person.addDebitCard(test_debit_card)
    test_person.addDebitCard(
        DebitCard(connection=temporary_db.connection, name="other_debit_card")
    )
    assert (
        next(
            (item for item in test_person.debitCards if item.name == "test_debit_card"),
            None,
        )
        is test_debit_card
    )
    assert (
        test_person.debitCardsSelect.filter(
            DebitCard.q.name == "test_debit_card"
        ).getOne()
        is test_debit_card
    )

    test_organization = db.Organization(
        connection=temporary_db.connection, externalID="test_employer"
    )
    test_job = db.Job(
        connection=temporary_db.connection,
        organization=test_organization,
        person=test_person,
    )
    db.Job(
        connection=temporary_db.connection,
        organization=db.Organization(
            connection=temporary_db.connection, externalID="other_employer"
        ),
        person=test_person,
    )
    assert (
        next(
            (
                item
                for item in test_person.jobs
                if item.organization.externalID == "test_employer"
            ),
            None,
        )
        is test_job
    )
    # assert (
    #     test_person.jobsSelect.throughTo.organization.filter(
    #         db.Job.q.organization.q.externalID == "test_employer"
    #     ).getOne()
    #     is test_job
    # )
