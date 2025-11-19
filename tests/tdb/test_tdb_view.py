import test_db as db
from test_db.main import main as tdb


def test_view_address(capsys, monkeypatch, db_file, temporary_db):
    address = db.Address(connection=temporary_db.connection)
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "view", "address", address.gID])

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("\nAddress ID: addr_")


def test_view_bank_account(capsys, monkeypatch, db_file, temporary_db):
    bank_account = db.BankAccount(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "view", "bank-account", bank_account.gID]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("ba_")


def test_view_debit_card(capsys, monkeypatch, db_file, temporary_db):
    debit_card = db.DebitCard(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "view", "debit-card", debit_card.gID]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("dc_")


def test_view_job(capsys, monkeypatch, db_file, temporary_db, organization, person):
    job = db.Job(
        organization=organization, person=person, connection=temporary_db.connection
    )
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "view", "job", job.gID])

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("\nJob ID:\tj_")


def test_view_organization(capsys, monkeypatch, db_file, organization):
    monkeypatch.setattr(
        "sys.argv", ["tdb", db_file, "view", "organization", organization.gID]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("\nOrganization ID:\to_")


def test_view_person(capsys, monkeypatch, db_file, person):
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "view", "person", person.gID])

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("\nPerson ID:\tp_")
