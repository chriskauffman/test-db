from test_db._organization import Organization


def test_organization(temporary_db):
    test_organization = Organization(
        name="test_organization",
        connection=temporary_db.connection,
    )

    assert isinstance(test_organization, Organization)
