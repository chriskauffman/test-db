import test_db
from test_db.tdb_console import main as tdb


def test_organization_key_value_add(capsys, monkeypatch, temporary_db):
    organization = test_db.Organization(connection=temporary_db.connection)
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            "set command_interaction false",
            f"tdb_organization_key_value_add {organization.gID} test_key_value_add test_key_value_add_value",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert not captured.err

def test_organization_key_value_view(capsys, monkeypatch, temporary_db):
    organization = test_db.Organization(connection=temporary_db.connection)
    organization_key_value = test_db.OrganizationKeyValue(
        connection=temporary_db.connection,
        organization=organization,
        itemKey="test_organization_key_value_view",
        itemValue="test_organization_key_value_view_value",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_organization_key_value_view {organization.gID} {organization_key_value.itemKey}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert "test_organization_key_value_view" in captured.out
    assert "test_organization_key_value_view_value" in captured.out


def test_organization_key_value_list(capsys, monkeypatch, temporary_db):
    organization = test_db.Organization(connection=temporary_db.connection)
    organization_key_value = test_db.OrganizationKeyValue(
        connection=temporary_db.connection,
        organization=organization,
        itemKey="test_organization_key_value_list",
        itemValue="test_organization_key_value_list_value",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"tdb_organization_key_value_list {organization.gID}",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert organization_key_value.itemKey in captured.out
