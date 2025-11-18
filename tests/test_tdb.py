import pytest

import test_db as db
from test_db.main import main as tdb


@pytest.fixture(scope="module")
def db_file(temporary_db):
    return str(temporary_db.filePath)


@pytest.fixture(scope="module")
def person(temporary_db):
    return db.Person(connection=temporary_db.connection)


@pytest.fixture(scope="module")
def organization(temporary_db):
    return db.Organization(connection=temporary_db.connection)


def test_add_address(capsys, monkeypatch, db_file):
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "add", "address"])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "addr_" in captured.out


def test_add_address_with_owner(capsys, monkeypatch, db_file, person):
    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "add", "address", "--occupant-gid", person.gID]
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "addr_" in captured.out


def test_add_address_with_bad_owner(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", db_file, "add", "address", "--occupant-gid", "NonExistentGID"],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "does not exist" in captured.err


def test_add_bank_account(capsys, monkeypatch, db_file):
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "add", "bank-account"])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "ba_" in captured.out


def test_add_bank_account_with_owner(capsys, monkeypatch, db_file, person):
    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "add", "bank-account", "--owner-gid", person.gID]
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "ba_" in captured.out


def test_add_bank_account_with_bad_owner(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", db_file, "add", "bank-account", "--owner-gid", "NonExistentGID"],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_add_debit_card(capsys, monkeypatch, db_file):
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "add", "debit-card"])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "dc_" in captured.out


def test_add_debit_card_with_owner(capsys, monkeypatch, db_file, person):
    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "add", "debit-card", "--owner-gid", person.gID]
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "dc_" in captured.out


def test_add_debit_card_with_bad_owner(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv",
        ["tdb", db_file, "add", "debit-card", "--owner-gid", "NonExistentGID"],
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_add_job(capsys, monkeypatch, db_file, person, organization):
    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "add", "job", organization.gID, person.gID]
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "j_" in captured.out


def test_add_key_value(capsys, monkeypatch, db_file, person, organization):
    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "add", "key-value", "test_key", "test_value"]
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert not captured.out


def test_add_organization(capsys, monkeypatch, db_file):
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "add", "organization"])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "o_" in captured.out


def test_add_person(capsys, monkeypatch, db_file):
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "add", "person"])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "p_" in captured.out


def test_list_addresses(capsys, monkeypatch, db_file):
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "list", "addresses"])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "addr_" in captured.out


def test_list_bank_accounts(capsys, monkeypatch, db_file):
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "list", "bank-accounts"])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "ba_" in captured.out


def test_list_debit_cards(capsys, monkeypatch, db_file):
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "list", "debit-cards"])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "dc_" in captured.out


def test_list_jobs(capsys, monkeypatch, db_file):
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "list", "jobs"])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "j_" in captured.out


def test_list_organizations(capsys, monkeypatch, db_file):
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "list", "organizations"])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "o_" in captured.out


def test_list_people(capsys, monkeypatch, db_file):
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "list", "people"])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "p_" in captured.out


def test_view_address(capsys, monkeypatch, db_file, temporary_db):
    address = db.Address(connection=temporary_db.connection)
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "view", "address", address.gID])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "addr_" in captured.out


def test_view_bank_account(capsys, monkeypatch, db_file, temporary_db):
    bank_account = db.BankAccount(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "view", "bank-account", bank_account.gID]
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "ba_" in captured.out


def test_view_debit_card(capsys, monkeypatch, db_file, temporary_db):
    debit_card = db.DebitCard(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "view", "debit-card", debit_card.gID]
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "dc_" in captured.out


def test_view_job(capsys, monkeypatch, db_file, temporary_db, organization, person):
    job = db.Job(
        organization=organization, person=person, connection=temporary_db.connection
    )
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "view", "job", job.gID])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "j_" in captured.out


def test_view_organization(capsys, monkeypatch, db_file, organization):
    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "view", "organization", organization.gID]
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "o_" in captured.out


def test_view_person(capsys, monkeypatch, db_file, person):
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "view", "person", person.gID])

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert "p_" in captured.out
