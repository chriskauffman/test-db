import uuid

import pytest

import test_db
from test_db.tdb import app as cli


@pytest.mark.parametrize(
    "command,owner_class,key_value_class,owner_field",
    [
        ("person-key-value", test_db.Person, test_db.PersonKeyValue, "person"),
        ("job-key-value", test_db.Job, test_db.JobKeyValue, "job"),
        (
            "organization-key-value",
            test_db.Organization,
            test_db.OrganizationKeyValue,
            "organization",
        ),
        (
            "person-secure-key-value",
            test_db.Person,
            test_db.PersonSecureKeyValue,
            "person",
        ),
    ],
)
def test_duplicate_key_add_fails(
    capsys,
    monkeypatch,
    temporary_db,
    command,
    owner_class,
    key_value_class,
    owner_field,
):
    connection = temporary_db.connection
    owner = owner_class(connection=connection)
    key = f"duplicate-{uuid.uuid4()}"

    monkeypatch.setattr("sys.argv", ["tdb", command, "add", str(owner.gID), key, "old"])
    with pytest.raises(SystemExit) as first:
        cli()
    assert first.value.code == 0
    assert not capsys.readouterr().err

    records = key_value_class.selectBy(connection=connection, **{owner_field: owner})
    assert records.count() == 1
    stored = records.getOne()

    monkeypatch.setattr("sys.argv", ["tdb", command, "add", str(owner.gID), key, "new"])
    with pytest.raises(SystemExit) as second:
        cli()
    captured = capsys.readouterr()

    assert second.value.code == 1
    assert captured.err
    assert not captured.out
    assert records.count() == 1
    stored.sync()
    assert stored.value == "old"
