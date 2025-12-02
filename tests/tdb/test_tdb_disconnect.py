import test_db as db
from test_db.main import main as tdb


def test_disconnect_address(capsys, monkeypatch, db_file, temporary_db):
    test_address = db.Address(connection=temporary_db.connection)

    test_person = db.Person(connection=temporary_db.connection)
    test_person.addAddress(test_address)

    assert test_address in test_person.addresses

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            db_file,
            "disconnect",
            "address",
            str(test_address.gID),
            str(test_person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.Address.get(test_address.id)
    assert db.Person.get(test_person.id)
    assert test_address not in test_person.addresses

    test_organization = db.Organization(connection=temporary_db.connection)
    test_organization.addAddress(test_address)

    assert test_address in test_organization.addresses

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            db_file,
            "disconnect",
            "address",
            str(test_address.gID),
            str(test_organization.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.Address.get(test_address.id)
    assert db.Organization.get(test_organization.id)
    assert test_address not in test_organization.addresses


def test_disconnect_bank_account(capsys, monkeypatch, db_file, temporary_db):
    test_bank_account = db.BankAccount(connection=temporary_db.connection)

    test_person = db.Person(connection=temporary_db.connection)
    test_person.addBankAccount(test_bank_account)

    assert test_bank_account in test_person.bankAccounts

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            db_file,
            "disconnect",
            "bank-account",
            str(test_bank_account.gID),
            str(test_person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.BankAccount.get(test_bank_account.id)
    assert db.Person.get(test_person.id)
    assert test_bank_account not in test_person.bankAccounts

    test_organization = db.Organization(connection=temporary_db.connection)
    test_organization.addBankAccount(test_bank_account)

    assert test_bank_account in test_organization.bankAccounts

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            db_file,
            "disconnect",
            "bank-account",
            str(test_bank_account.gID),
            str(test_organization.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.BankAccount.get(test_bank_account.id)
    assert db.Organization.get(test_organization.id)
    assert test_bank_account not in test_organization.bankAccounts


def test_disconnect_debit_card(capsys, monkeypatch, db_file, temporary_db):
    test_debit_card = db.DebitCard(connection=temporary_db.connection)

    test_person = db.Person(connection=temporary_db.connection)
    test_person.addDebitCard(test_debit_card)

    assert test_debit_card in test_person.debitCards

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            db_file,
            "disconnect",
            "debit-card",
            str(test_debit_card.gID),
            str(test_person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.DebitCard.get(test_debit_card.id)
    assert db.Person.get(test_person.id)
    assert test_debit_card not in test_person.debitCards

    test_organization = db.Organization(connection=temporary_db.connection)
    test_organization.addDebitCard(test_debit_card)

    assert test_debit_card in test_organization.debitCards

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            db_file,
            "disconnect",
            "debit-card",
            str(test_debit_card.gID),
            str(test_organization.gID),
        ],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    assert db.DebitCard.get(test_debit_card.id)
    assert db.Organization.get(test_organization.id)
    assert test_debit_card not in test_organization.debitCards
