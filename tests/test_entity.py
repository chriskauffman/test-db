import pytest

from test_db._address import Address
from test_db._bank_account import BankAccount
from test_db._debit_card import DebitCard
from test_db._entity import Entity


@pytest.fixture(scope="session", autouse=True)
def set_autoCreate_dependents():
    Entity._autoCreateDependents = True


def test_init(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)
    assert test_entity


def test_getAddressByName(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)

    test_address = test_entity.getAddressByName("test1")

    assert isinstance(test_address, Address)
    assert test_address.name == "test1"

    test_address = test_entity.getAddressByName("test2", street="123 Main")

    assert test_address.street == "123 Main"


def test_getBankAccountByName(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)

    test_bank_account = test_entity.getBankAccountByName("test1")

    assert isinstance(test_bank_account, BankAccount)
    assert test_bank_account.name == "test1"

    test_bank_account = test_entity.getBankAccountByName(
        "test2", routingNumber="987897897"
    )

    assert test_bank_account.routingNumber == "987897897"


def test_getDebitCardByName(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)

    test_debit_card = test_entity.getDebitCardByName("test1")

    assert isinstance(test_debit_card, DebitCard)
    assert test_debit_card.name == "test1"

    test_debit_card = test_entity.getDebitCardByName("test2", cvv="123")

    assert test_debit_card.cvv == "123"
