import faker

import test_db
from test_db._address import Address
from test_db._bank_account import BankAccount
from test_db._debit_card import DebitCard
from test_db._person import Person


fake = faker.Faker()


def test_init(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    assert test_person


def test__set_email(temporary_db):
    test_person = Person(
        email="test__set_email@example.com", connection=temporary_db.connection
    )

    assert test_person.email == "test__set_email@example.com"


def test_locate_related_objects(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    test_address = Address(
        connection=temporary_db.connection, description="test_address"
    )
    test_person.addAddress(test_address)
    test_person.addAddress(
        Address(connection=temporary_db.connection, description="other_address")
    )
    assert (
        next(
            (
                item
                for item in test_person.addresses
                if item.description == "test_address"
            ),
            None,
        )
        is test_address
    )
    assert (
        test_person.addressesSelect.filter(
            Address.q.description == "test_address"
        ).getOne()
        is test_address
    )

    test_bank_account = BankAccount(
        connection=temporary_db.connection, description="test_bank_account"
    )
    test_person.addBankAccount(test_bank_account)
    test_person.addBankAccount(
        BankAccount(
            connection=temporary_db.connection, description="other_bank_account"
        )
    )
    assert (
        next(
            (
                item
                for item in test_person.bankAccounts
                if item.description == "test_bank_account"
            ),
            None,
        )
        is test_bank_account
    )
    assert (
        test_person.bankAccountsSelect.filter(
            BankAccount.q.description == "test_bank_account"
        ).getOne()
        is test_bank_account
    )

    test_debit_card = DebitCard(
        connection=temporary_db.connection, description="test_debit_card"
    )
    test_person.addDebitCard(test_debit_card)
    test_person.addDebitCard(
        DebitCard(connection=temporary_db.connection, description="other_debit_card")
    )
    assert (
        next(
            (
                item
                for item in test_person.debitCards
                if item.description == "test_debit_card"
            ),
            None,
        )
        is test_debit_card
    )
    assert (
        test_person.debitCardsSelect.filter(
            DebitCard.q.description == "test_debit_card"
        ).getOne()
        is test_debit_card
    )

    test_organization = test_db.Organization(
        connection=temporary_db.connection, externalID="test_employer"
    )
    test_job = test_db.Job(
        connection=temporary_db.connection,
        organization=test_organization,
        person=test_person,
    )
    test_db.Job(
        connection=temporary_db.connection,
        organization=test_db.Organization(
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
    #         test_db.Job.q.organization.q.externalID == "test_employer"
    #     ).getOne()
    #     is test_job
    # )


def test_autoCreateDependents_children(temporary_db):
    test_db.autoCreateDependents = False
    test_person = Person(connection=temporary_db.connection)
    assert len(test_person.addresses) == 0
    assert len(test_person.bankAccounts) == 0
    assert len(test_person.bankAccounts) == 0

    test_db.autoCreateDependents = True
    test_person = Person(connection=temporary_db.connection)
    assert len(test_person.addresses) == 1
    assert isinstance(test_person.addresses[0], Address)
    assert len(test_person.bankAccounts) == 1
    assert isinstance(test_person.bankAccounts[0], BankAccount)
    assert len(test_person.debitCards) == 1
    assert isinstance(test_person.debitCards[0], DebitCard)
