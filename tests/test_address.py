import test_db
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


def test_autoCreateDependents_organization(temporary_db):
    new_organization = Organization(connection=temporary_db.connection)
    organization_count = Organization.select(connection=temporary_db.connection).count()

    test_db.autoCreateDependents = False
    test_address = OrganizationAddress(
        connection=temporary_db.connection,
    )
    assert test_address.organization is None
    assert (
        Organization.select(connection=temporary_db.connection).count()
        == organization_count
    )

    test_address = OrganizationAddress(
        organization=new_organization,
        connection=temporary_db.connection,
    )
    assert test_address.organization is new_organization
    assert (
        Organization.select(connection=temporary_db.connection).count()
        == organization_count
    )

    test_db.autoCreateDependents = True
    test_address = OrganizationAddress(
        connection=temporary_db.connection,
    )
    assert isinstance(test_address.organization, Organization)
    assert (
        Organization.select(connection=temporary_db.connection).count()
        == organization_count + 1
    )

    test_address = OrganizationAddress(
        organization=new_organization,
        connection=temporary_db.connection,
    )
    assert test_address.organization is new_organization
    assert (
        Organization.select(connection=temporary_db.connection).count()
        == organization_count + 1
    )


def test_person_address(temporary_db):
    test_address = PersonAddress(
        person=Person(connection=temporary_db.connection),
        connection=temporary_db.connection,
    )

    assert isinstance(test_address, PersonAddress)
    assert address_validation(test_address)


def test_autoCreateDependents_person(temporary_db):
    new_person = Person(connection=temporary_db.connection)
    person_count = Person.select(connection=temporary_db.connection).count()

    test_db.autoCreateDependents = False
    test_address = PersonAddress(
        connection=temporary_db.connection,
    )
    assert test_address.person is None
    assert Person.select(connection=temporary_db.connection).count() == person_count

    test_address = PersonAddress(
        person=new_person,
        connection=temporary_db.connection,
    )
    assert test_address.person is new_person
    assert Person.select(connection=temporary_db.connection).count() == person_count

    test_db.autoCreateDependents = True
    test_address = PersonAddress(
        connection=temporary_db.connection,
    )
    assert isinstance(test_address.person, Person)
    assert Person.select(connection=temporary_db.connection).count() == person_count + 1

    test_address = PersonAddress(
        person=new_person,
        connection=temporary_db.connection,
    )
    assert test_address.person is new_person
    assert Person.select(connection=temporary_db.connection).count() == person_count + 1
