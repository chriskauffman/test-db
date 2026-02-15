import test_db
from test_db._organization import Organization
from test_db._organization_bank_account import OrganizationBankAccount
from test_db._person import Person
from test_db._person_bank_account import PersonBankAccount


def bank_account_validation(test_bank_account):
    assert isinstance(test_bank_account.routingNumber, str)
    assert isinstance(int(test_bank_account.accountNumber), int)
    assert isinstance(test_bank_account.accountNumber, str)
    assert isinstance(int(test_bank_account.accountNumber), int)


def test_organization_bank_account(temporary_db):
    test_bank_account = OrganizationBankAccount(
        organization=Organization(connection=temporary_db.connection),
        connection=temporary_db.connection,
    )

    assert isinstance(test_bank_account, OrganizationBankAccount)
    bank_account_validation(test_bank_account)


def test_autoCreateDependents_organization(temporary_db):
    new_organization = Organization(connection=temporary_db.connection)
    organization_count = Organization.select(connection=temporary_db.connection).count()

    test_db.autoCreateDependents = False
    test_bank_account = OrganizationBankAccount(
        connection=temporary_db.connection,
    )
    assert test_bank_account.organization is None
    assert (
        Organization.select(connection=temporary_db.connection).count()
        == organization_count
    )

    test_bank_account = OrganizationBankAccount(
        organization=new_organization,
        connection=temporary_db.connection,
    )
    assert test_bank_account.organization is new_organization
    assert (
        Organization.select(connection=temporary_db.connection).count()
        == organization_count
    )

    test_db.autoCreateDependents = True
    test_bank_account = OrganizationBankAccount(
        connection=temporary_db.connection,
    )
    assert isinstance(test_bank_account.organization, Organization)
    assert (
        Organization.select(connection=temporary_db.connection).count()
        == organization_count + 1
    )

    test_bank_account = OrganizationBankAccount(
        organization=new_organization,
        connection=temporary_db.connection,
    )
    assert test_bank_account.organization is new_organization
    assert (
        Organization.select(connection=temporary_db.connection).count()
        == organization_count + 1
    )


def test_person_bank_account(temporary_db):
    test_bank_account = PersonBankAccount(
        person=Person(connection=temporary_db.connection),
        connection=temporary_db.connection,
    )

    assert isinstance(test_bank_account, PersonBankAccount)
    bank_account_validation(test_bank_account)


def test_autoCreateDependents_person(temporary_db):
    new_person = Person(connection=temporary_db.connection)
    person_count = Person.select(connection=temporary_db.connection).count()

    test_db.autoCreateDependents = False
    test_bank_account = PersonBankAccount(
        connection=temporary_db.connection,
    )
    assert test_bank_account.person is None
    assert Person.select(connection=temporary_db.connection).count() == person_count

    test_bank_account = PersonBankAccount(
        person=new_person,
        connection=temporary_db.connection,
    )
    assert test_bank_account.person is new_person
    assert Person.select(connection=temporary_db.connection).count() == person_count

    test_db.autoCreateDependents = True
    test_bank_account = PersonBankAccount(
        connection=temporary_db.connection,
    )
    assert isinstance(test_bank_account.person, Person)
    assert Person.select(connection=temporary_db.connection).count() == person_count + 1

    test_bank_account = PersonBankAccount(
        person=new_person,
        connection=temporary_db.connection,
    )
    assert test_bank_account.person is new_person
    assert Person.select(connection=temporary_db.connection).count() == person_count + 1
