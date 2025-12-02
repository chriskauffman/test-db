from datetime import datetime, timezone
import logging

from test_db._address import Address
from test_db._bank_account import BankAccount
from test_db._debit_card import DebitCard
from test_db._entity import Entity
from test_db._job import Job
from test_db._organization import Organization
from test_db._person import Person

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
        isinstance(instance, Entity)
        and instance._connection.tdbGlobalDatabaseOptions.autoCreateDependents
    ):
        if not instance.addresses:
            instance.addAddress(Address(connection=instance._connection))
        if not instance.bankAccounts:
            instance.addBankAccount(BankAccount(connection=instance._connection))
        if not instance.debitCards:
            instance.addDebitCard(DebitCard(connection=instance._connection))
    if (
        isinstance(instance, Job)
        and instance._connection.tdbGlobalDatabaseOptions.autoCreateDependents
    ):
        if not instance.organization:
            instance.organization = Organization(connection=instance._connection)
        if not instance.person:
            instance.person = Person(connection=instance._connection)
