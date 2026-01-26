from test_db._organization import Organization
from test_db._organization_address import OrganizationAddress
from test_db._person import Person
from test_db._person_address import PersonAddress


def address_validation(test_address):
    return isinstance(test_address.street, str)


def test_organization_address(temporary_db):
    test_address = OrganizationAddress(
        organization=Organization(connection=temporary_db.connection),
        connection=temporary_db.connection,
    )

    assert isinstance(test_address, OrganizationAddress)
    assert address_validation(test_address)


def test_person_address(temporary_db):
    test_address = PersonAddress(
        person=Person(connection=temporary_db.connection),
        connection=temporary_db.connection,
    )

    assert isinstance(test_address, PersonAddress)
    assert address_validation(test_address)
