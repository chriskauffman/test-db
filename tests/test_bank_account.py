from test_db._bank_account import PersonalBankAccount
from test_db._person import Person


def test_personal_bank_account(temporary_db):
    test_person = Person(connection=temporary_db.connection)
    test_personal_bank_account = PersonalBankAccount(
        name="test_personal_bank_account",
        person=test_person,
        connection=temporary_db.connection,
    )

    assert isinstance(test_personal_bank_account, PersonalBankAccount)
    assert isinstance(test_personal_bank_account.routingNumber, str)
    assert isinstance(int(test_personal_bank_account.accountNumber), int)
    assert isinstance(test_personal_bank_account.accountNumber, str)
    assert isinstance(int(test_personal_bank_account.accountNumber), int)
