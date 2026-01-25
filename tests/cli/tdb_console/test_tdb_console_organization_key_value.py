import test_db
from test_db.tdb_console import main as tdb


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
            f"set db_connection_uri {temporary_db.connectionURI}",
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
    monkeypatch.setattr(
        "sys.argv",
        [
            "tdb",
            f"set db_connection_uri {temporary_db.connectionURI}",
            "tdb_organization_key_value_list",
            "quit",
        ],
    )

    try:
        tdb()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    assert captured.out
