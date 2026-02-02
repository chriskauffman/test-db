import test_db
from test_db._organization import Organization
from test_db._organization_address import OrganizationAddress
from test_db._organization_bank_account import OrganizationBankAccount
from test_db._organization_key_value import OrganizationKeyValue


def test_organization(temporary_db):
    test_organization = Organization(connection=temporary_db.connection)

    assert isinstance(test_organization, Organization)


def test_autoCreateDependents_children(temporary_db):
    test_db.autoCreateDependents = False
    test_organization = Organization(connection=temporary_db.connection)
    assert len(test_organization.addresses) == 0
    assert len(test_organization.bankAccounts) == 0

    test_db.autoCreateDependents = True
    test_organization = Organization(connection=temporary_db.connection)
    assert len(test_organization.addresses) == 1
    assert isinstance(test_organization.addresses[0], OrganizationAddress)
    assert len(test_organization.bankAccounts) == 1
    assert isinstance(test_organization.bankAccounts[0], OrganizationBankAccount)


def test_getKeyValueByKey(temporary_db):
    test_organization = Organization(connection=temporary_db.connection)

    test_key_value = test_organization.getKeyValueByKey("test_getKeyValueByKey")

    assert isinstance(test_key_value, OrganizationKeyValue)
    assert test_key_value.key == "test_getKeyValueByKey"

    test_key_value = test_organization.getKeyValueByKey(
        "test_getKeyValueByKey_2", value="testAccessToken"
    )

    assert test_key_value.value == "testAccessToken"


def test_cascade_delete(temporary_db):
    test_db.autoCreateDependents = False
    test_organization = Organization(connection=temporary_db.connection)

    initial_count_of_all_organization_addresses = OrganizationAddress.select(
        connection=temporary_db.connection
    ).count()
    for item in range(5):
        OrganizationAddress(
            organization=test_organization,
            connection=temporary_db.connection,
        )

    assert (
        OrganizationAddress.select(connection=temporary_db.connection).count()
        == initial_count_of_all_organization_addresses + 5
    )
    assert (
        OrganizationAddress.select(
            OrganizationAddress.q.organization == test_organization.id,
            connection=temporary_db.connection,
        ).count()
        == 5
    )
    assert len(test_organization.addresses) == 5

    initial_count_of_all_organization_bank_accounts = OrganizationBankAccount.select(
        connection=temporary_db.connection
    ).count()
    for item in range(5):
        OrganizationBankAccount(
            organization=test_organization,
            connection=temporary_db.connection,
        )

    assert (
        OrganizationBankAccount.select(connection=temporary_db.connection).count()
        == initial_count_of_all_organization_bank_accounts + 5
    )
    assert (
        OrganizationBankAccount.select(
            OrganizationBankAccount.q.organization == test_organization.id,
            connection=temporary_db.connection,
        ).count()
        == 5
    )
    assert len(test_organization.bankAccounts) == 5

    initial_count_of_all_organization_key_values = OrganizationKeyValue.select(
        connection=temporary_db.connection
    ).count()
    for item in range(5):
        OrganizationKeyValue(
            key=f"cascadeTest{item}",
            organization=test_organization,
            connection=temporary_db.connection,
        )

    assert (
        OrganizationKeyValue.select(connection=temporary_db.connection).count()
        == initial_count_of_all_organization_key_values + 5
    )
    assert (
        OrganizationKeyValue.select(
            OrganizationKeyValue.q.organization == test_organization.id,
            connection=temporary_db.connection,
        ).count()
        == 5
    )
    assert len(test_organization.keyValues) == 5

    test_organization.destroySelf()
    assert (
        OrganizationAddress.select(connection=temporary_db.connection).count()
        == initial_count_of_all_organization_addresses
    )
    assert (
        OrganizationAddress.select(
            OrganizationAddress.q.organization == test_organization.id,
            connection=temporary_db.connection,
        ).count()
        == 0
    )
    assert (
        OrganizationBankAccount.select(connection=temporary_db.connection).count()
        == initial_count_of_all_organization_bank_accounts
    )
    assert (
        OrganizationBankAccount.select(
            OrganizationBankAccount.q.organization == test_organization.id,
            connection=temporary_db.connection,
        ).count()
        == 0
    )
    assert (
        OrganizationKeyValue.select(connection=temporary_db.connection).count()
        == initial_count_of_all_organization_key_values
    )
    assert (
        OrganizationKeyValue.select(
            OrganizationKeyValue.q.organization == test_organization.id,
            connection=temporary_db.connection,
        ).count()
        == 0
    )
    test_db.autoCreateDependents = True
