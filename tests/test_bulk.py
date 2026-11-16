import pytest

import test_db
from test_db._organization import Organization
from test_db._organization_address import OrganizationAddress
from test_db._organization_bank_account import OrganizationBankAccount
from test_db._person import Person
from test_db._person_address import PersonAddress
from test_db._person_bank_account import PersonBankAccount
from test_db._person_debit_card import PersonDebitCard
from test_db.cli import bulk_transaction


@pytest.mark.parametrize(
    ("model", "blocked_methods"),
    [
        (Person, ("selectBy", "byEmail", "bySocialSecurityNumber")),
        (Organization, ("byName", "byEmployerIdentificationNumber")),
        (PersonAddress, ("selectBy",)),
        (OrganizationAddress, ("selectBy",)),
        (PersonBankAccount, ("selectBy",)),
        (OrganizationBankAccount, ("selectBy",)),
        (PersonDebitCard, ("selectBy",)),
    ],
)
def test_bulk_handlers_skip_per_row_lookup(
    temporary_db, monkeypatch, model, blocked_methods
):
    previous_auto_create_dependents = test_db.autoCreateDependents
    test_db.autoCreateDependents = False

    def fail(*args, **kwargs):
        pytest.fail(f"bulk generation queried {model.__name__}")

    for method in blocked_methods:
        monkeypatch.setattr(model, method, fail)

    try:
        with bulk_transaction(temporary_db.connection) as transaction:
            model(connection=transaction)
    finally:
        test_db.autoCreateDependents = previous_auto_create_dependents
