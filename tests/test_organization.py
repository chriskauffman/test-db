import test_db
from test_db._address import Address
from test_db._bank_account import BankAccount
from test_db._debit_card import DebitCard
from test_db._organization import Organization


def test_organization(temporary_db):
    test_organization = Organization(
        name="test_organization",
        connection=temporary_db.connection,
    )

    assert isinstance(test_organization, Organization)


def test_autoCreateDependents_children(temporary_db):
    test_db.autoCreateDependents = False
    test_person = Organization(connection=temporary_db.connection)
    assert len(test_person.addresses) == 0
    assert len(test_person.bankAccounts) == 0
    assert len(test_person.bankAccounts) == 0

    test_db.autoCreateDependents = True
    test_person = Organization(connection=temporary_db.connection)
    assert len(test_person.addresses) == 1
    assert isinstance(test_person.addresses[0], Address)
    assert len(test_person.bankAccounts) == 1
    assert isinstance(test_person.bankAccounts[0], BankAccount)
    assert len(test_person.debitCards) == 1
    assert isinstance(test_person.debitCards[0], DebitCard)
