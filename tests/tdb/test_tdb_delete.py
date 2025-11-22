import pytest
from sqlobject import SQLObjectNotFound

import test_db as db
from test_db.main import main as tdb


def test_delete_address(capsys, monkeypatch, db_file, temporary_db):
    test_address = db.Address(connection=temporary_db.connection)
    assert (
        db.Address.get(test_address.id, connection=temporary_db.connection)
        is test_address
    )

    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "delete", "address", str(test_address.gID)]
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        db.Address.get(test_address.id, connection=temporary_db.connection)


def test_delete_bank_account(capsys, monkeypatch, db_file, temporary_db):
    test_bank_account = db.BankAccount(connection=temporary_db.connection)
    assert (
        db.BankAccount.get(test_bank_account.id, connection=temporary_db.connection)
        is test_bank_account
    )

    monkeypatch.setattr(
        "sys.argv",
        ["tdb", db_file, "delete", "bank-account", str(test_bank_account.gID)],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        db.BankAccount.get(test_bank_account.id, connection=temporary_db.connection)


def test_delete_debit_card(capsys, monkeypatch, db_file, temporary_db):
    test_debit_card = db.DebitCard(connection=temporary_db.connection)
    assert (
        db.DebitCard.get(test_debit_card.id, connection=temporary_db.connection)
        is test_debit_card
    )
    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "delete", "debit-card", str(test_debit_card.gID)]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        db.DebitCard.get(test_debit_card.id, connection=temporary_db.connection)


def test_delete_job(capsys, monkeypatch, db_file, person, organization, temporary_db):
    test_job = db.Job(connection=temporary_db.connection)
    assert db.Job.get(test_job.id, connection=temporary_db.connection) is test_job

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            db_file,
            "delete",
            "job",
            str(test_job.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        db.Job.get(test_job.id, connection=temporary_db.connection)


def test_delete_key_value(capsys, monkeypatch, db_file, temporary_db):
    test_key_value = db.KeyValue(
        connection=temporary_db.connection, key="test_delete_key_value"
    )
    assert (
        db.KeyValue.get(test_key_value.id, connection=temporary_db.connection)
        is test_key_value
    )

    monkeypatch.setattr(
        "sys.argv",
        ["tdb", db_file, "delete", "key-value", test_key_value.key],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        db.KeyValue.get(test_key_value.id, connection=temporary_db.connection)


def test_delete_organization(capsys, monkeypatch, db_file, temporary_db):
    test_organization = db.Organization(connection=temporary_db.connection)
    assert (
        db.Organization.get(test_organization.id, connection=temporary_db.connection)
        is test_organization
    )

    monkeypatch.setattr(
        "sys.argv",
        ["tdb", db_file, "delete", "organization", str(test_organization.gID)],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        db.Organization.get(test_organization.id, connection=temporary_db.connection)


def test_delete_person(capsys, monkeypatch, db_file, temporary_db):
    test_person = db.Person(connection=temporary_db.connection)
    assert (
        db.Person.get(test_person.id, connection=temporary_db.connection) is test_person
    )

    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "delete", "person", str(test_person.gID)]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        db.Person.get(test_person.id, connection=temporary_db.connection)


def test_delete_personal_key_value_secure(
    capsys, monkeypatch, db_file, person, temporary_db
):
    test_personal_key_value_secure = db.PersonalKeyValueSecure(
        connection=temporary_db.connection,
        key="test_delete_personal_key_value_secure",
        person=person,
    )
    assert (
        db.PersonalKeyValueSecure.get(
            test_personal_key_value_secure.id, connection=temporary_db.connection
        )
        is test_personal_key_value_secure
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            db_file,
            "delete",
            "personal-key-value-secure",
            str(person.gID),
            test_personal_key_value_secure.key,
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out

    with pytest.raises(SQLObjectNotFound):
        db.PersonalKeyValueSecure.get(
            test_personal_key_value_secure.id, connection=temporary_db.connection
        )
