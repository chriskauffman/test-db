from test_db._bank_account import BankAccount


def test_bank_account(temporary_db):
    test_personal_bank_account = BankAccount(connection=temporary_db.connection)

    assert isinstance(test_personal_bank_account, BankAccount)
    assert isinstance(test_personal_bank_account.routingNumber, str)
    assert isinstance(int(test_personal_bank_account.accountNumber), int)
    assert isinstance(test_personal_bank_account.accountNumber, str)
    assert isinstance(int(test_personal_bank_account.accountNumber), int)


def test_byRoutingAndAccountNumber(temporary_db):
    test_bank_account = BankAccount(connection=temporary_db.connection)

    assert (
        BankAccount.byRoutingAndAccountNumber(
            test_bank_account.routingNumber,
            test_bank_account.accountNumber,
            connection=temporary_db.connection,
        )
        is test_bank_account
    )
