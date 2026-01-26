from datetime import datetime, timezone
import logging

from test_db._job import Job
from test_db._organization import Organization
from test_db._organization_address import OrganizationAddress
from test_db._organization_bank_account import OrganizationBankAccount
from test_db._person import Person
from test_db._person_address import PersonAddress
from test_db._person_bank_account import PersonBankAccount
from test_db._person_debit_card import PersonDebitCard


logger = logging.getLogger(__name__)


def handleRowCreateSignal(instance, kwargs, post_funcs):
    """Sets createdAt field"""
    kwargs["updatedAt"] = datetime.now(timezone.utc)
    kwargs["createdAt"] = kwargs.get("createdAt") or kwargs["updatedAt"]


def handleRowUpdateSignal(instance, kwargs):
    """Keeps updatedAt field current"""
    kwargs["updatedAt"] = datetime.now(timezone.utc)


def handleRowCreatedSignal(instance, kwargs, post_funcs):
    if (
        isinstance(instance, Organization)
        and instance._connection.tdbGlobalDatabaseOptions.autoCreateDependents
    ):
        if not instance.addresses:
            OrganizationAddress(organization=instance, connection=instance._connection)
        if not instance.bankAccounts:
            OrganizationBankAccount(
                organization=instance, connection=instance._connection
            )
    if (
        isinstance(instance, Person)
        and instance._connection.tdbGlobalDatabaseOptions.autoCreateDependents
    ):
        if not instance.addresses:
            PersonAddress(person=instance, connection=instance._connection)
        if not instance.bankAccounts:
            PersonBankAccount(person=instance, connection=instance._connection)
        if not instance.debitCards:
            PersonDebitCard(person=instance, connection=instance._connection)
    if (
        isinstance(instance, Job)
        and instance._connection.tdbGlobalDatabaseOptions.autoCreateDependents
    ):
        if not instance.organization:
            instance.organization = Organization(connection=instance._connection)
        if not instance.person:
            instance.person = Person(connection=instance._connection)
