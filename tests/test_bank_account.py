from test_db._organization import Organization
from test_db._organization_bank_account import OrganizationBankAccount
from test_db._person import Person
from test_db._person_bank_account import PersonBankAccount


def bank_account_validation(test_bank_account):
    assert isinstance(test_bank_account.routingNumber, str)
    assert isinstance(int(test_bank_account.accountNumber), int)
    assert isinstance(test_bank_account.accountNumber, str)
    assert isinstance(int(test_bank_account.accountNumber), int)


def test_organization_bank_account(temporary_db):
    test_bank_account = OrganizationBankAccount(
        organization=Organization(connection=temporary_db.connection),
        connection=temporary_db.connection,
    )

    assert isinstance(test_bank_account, OrganizationBankAccount)
    bank_account_validation(test_bank_account)


def test_person_bank_account(temporary_db):
    test_bank_account = PersonBankAccount(
        person=Person(connection=temporary_db.connection),
        connection=temporary_db.connection,
    )

    assert isinstance(test_bank_account, PersonBankAccount)
    bank_account_validation(test_bank_account)
