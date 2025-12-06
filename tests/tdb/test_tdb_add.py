import test_db as db
from test_db.tdb import app as tdb


def test_add_address(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--db-file-path", db_file, "add", "address"]
    )

    try:
        tdb()
    except SystemExit:
        pass  # Ignore sys.exit() calls

    captured = capsys.readouterr()
    assert captured.out.startswith("addr_")


def test_add_address_with_owner(capsys, monkeypatch, db_file, person):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "address",
            "--entity-gid",
            str(person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("addr_")


def test_add_address_with_bad_owner(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "address",
            "--entity-gid",
            "test_01kah9p4b0ejfb7apkkr2abr7c",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_add_bank_account(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--db-file-path", db_file, "add", "bank-account"]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("ba_")


def test_add_bank_account_with_owner(capsys, monkeypatch, db_file, person):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "bank-account",
            "--entity-gid",
            str(person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("ba_")


def test_add_bank_account_with_bad_owner(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "bank-account",
            "--entity-gid",
            "test_01kah9p4b0ejfb7apkkr2abr7c",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_add_debit_card(capsys, monkeypatch, db_file, temporary_db):
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--db-file-path", db_file, "add", "debit-card"]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("dc_")


def test_add_debit_card_with_owner(capsys, monkeypatch, db_file, person):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "debit-card",
            "--entity-gid",
            str(person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("dc_")


def test_add_debit_card_with_bad_owner(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "debit-card",
            "--entity-gid",
            "test_01kah9p4b0ejfb7apkkr2abr7c",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_add_job(capsys, monkeypatch, db_file, person, organization):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "job",
            "--organization-gid",
            str(organization.gID),
            "--person-gid",
            str(person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("j_")


def test_add_job_bad_org(capsys, monkeypatch, db_file, person):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "job",
            "--organization-gid",
            "test_01kah9p4b0ejfb7apkkr2abr7c",
            "--person-gid",
            str(person.gID),
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "does not exist" in captured.err


def test_add_job_bad_person(capsys, monkeypatch, db_file, organization):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "job",
            "--organization-gid",
            str(organization.gID),
            "--person-gid",
            "test_01kah9p4b0ejfb7apkkr2abr7c",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "does not exist" in captured.err


def test_add_key_value(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "key-value",
            "test_add_key_value",
            "test_value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out


def test_add_key_value_duplicate(capsys, monkeypatch, db_file, temporary_db):
    db.KeyValue(
        key="test_add_key_value_duplicate",
        value="test_value",
        connection=temporary_db.connection,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "key-value",
            "test_add_key_value_duplicate",
            "test_value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "UNIQUE constraint failed" in captured.err


def test_add_organization(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv", ["tdb", "--db-file-path", db_file, "add", "organization"]
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("o_")


def test_add_person(capsys, monkeypatch, db_file):
    monkeypatch.setattr("sys.argv", ["tdb", "--db-file-path", db_file, "add", "person"])

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("p_")


def test_add_personal_key_value_secure(capsys, monkeypatch, db_file, person):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "personal-key-value-secure",
            str(person.gID),
            "secret",
            "value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.out


def test_add_personal_key_value_secure_bad_person(capsys, monkeypatch, db_file):
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "personal-key-value-secure",
            "test_01kah9p4b0ejfb7apkkr2abr7c",
            "secret",
            "value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "does not exist" in captured.err


def test_add_personal_key_value_secure_duplicate(capsys, monkeypatch, db_file, person):
    person.getPersonalKeyValueSecureByKey("secret2", value="test value")
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "--db-file-path",
            db_file,
            "add",
            "personal-key-value-secure",
            str(person.gID),
            "secret2",
            "value",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "UNIQUE constraint failed" in captured.err
