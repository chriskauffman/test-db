import test_db as db
from test_db.main import main as tdb


def test_list_addresses(capsys, monkeypatch, db_file, temporary_db, tmp_path_factory):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_list_addresses.sqlite")
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--create", empty_db_file, "list", "addresses"]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    db.Address(connection=temporary_db.connection)
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "list", "addresses"])
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("addr_")
    assert captured.out.count("addr_") >= 1


def test_list_bank_accounts(
    capsys, monkeypatch, db_file, temporary_db, tmp_path_factory
):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_list_addresses.sqlite")
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--create", empty_db_file, "list", "bank-accounts"]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    db.BankAccount(connection=temporary_db.connection)
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "list", "bank-accounts"])
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("ba_")
    assert captured.out.count("ba_") >= 1


def test_list_debit_cards(capsys, monkeypatch, db_file, temporary_db, tmp_path_factory):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_list_addresses.sqlite")
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--create", empty_db_file, "list", "debit-cards"]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    db.DebitCard(connection=temporary_db.connection)
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "list", "debit-cards"])
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("dc_")
    assert captured.out.count("dc_") >= 1


def test_list_jobs(
    capsys, monkeypatch, db_file, temporary_db, tmp_path_factory, organization, person
):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_list_addresses.sqlite")
    monkeypatch.setattr("sys.argv", ["tdb", "--create", empty_db_file, "list", "jobs"])

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    db.Job(connection=temporary_db.connection, organization=organization, person=person)
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "list", "jobs"])
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("j_")
    assert captured.out.count("j_") >= 1


def test_list_organizations(
    capsys, monkeypatch, db_file, temporary_db, tmp_path_factory
):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_list_addresses.sqlite")
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--create", empty_db_file, "list", "organizations"]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    db.Organization(connection=temporary_db.connection)
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "list", "organizations"])
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("o_")
    assert captured.out.count("o_") >= 1


def test_list_people(capsys, monkeypatch, db_file, temporary_db, tmp_path_factory):
    empty_db_file = str(tmp_path_factory.mktemp("data") / "test_list_addresses.sqlite")
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--create", empty_db_file, "list", "people"]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    db.Person(connection=temporary_db.connection)
    monkeypatch.setattr("sys.argv", ["tdb", db_file, "list", "people"])
    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("p_")
    assert captured.out.count("p_") >= 1
