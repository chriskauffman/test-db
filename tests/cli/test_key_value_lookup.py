import uuid

import pytest

import test_db
from test_db.tdb import app as cli
from test_db.tdb_console import main as console


@pytest.mark.parametrize("interface", ["cli", "console"])
@pytest.mark.parametrize("operation", ["view", "delete"])
@pytest.mark.parametrize("other_owner_has_key", [False, True])
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
def test_missing_key_is_lookup_only(
    capsys,
    monkeypatch,
    temporary_db,
    interface,
    operation,
    other_owner_has_key,
    command,
    owner_class,
    key_value_class,
    owner_field,
):
    connection = temporary_db.connection
    owner = owner_class(connection=connection)
    key = f"missing-{uuid.uuid4()}"
    other_record = None
    if other_owner_has_key:
        other_owner = owner_class(connection=connection)
        other_record = key_value_class(
            connection=connection,
            **{owner_field: other_owner},
            key=key,
            value="other owner's value",
        )

    records = key_value_class.selectBy(connection=connection, **{owner_field: owner})
    initial_count = records.count()
    inserts = []
    original_create = key_value_class._create

    def track_create(instance, *args, **kwargs):
        inserts.append(kwargs)
        return original_create(instance, *args, **kwargs)

    monkeypatch.setattr(key_value_class, "_create", track_create)
    if interface == "cli":
        argv = ["tdb", command, operation, str(owner.gID), key]
        entrypoint = cli
    else:
        console_command = f"tdb_{command.replace('-', '_')}_{operation}"
        argv = ["tdb", f"{console_command} {owner.gID} {key}", "quit"]
        entrypoint = console
    monkeypatch.setattr("sys.argv", argv)

    with pytest.raises(SystemExit) as exc:
        entrypoint()
    captured = capsys.readouterr()

    assert not inserts
    assert records.count() == initial_count
    assert exc.value.code == (1 if interface == "cli" else 0)
    assert key in captured.err
    assert "does not exist" in captured.err
    assert not captured.out
    if other_record is not None:
        other_record.sync()
        assert other_record.value == "other owner's value"
