import logging
import sys

from formencode.validators import Invalid  # type: ignore
from sqlobject import SQLObjectNotFound  # type: ignore
import typer

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Optional

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_organization

logger = logging.getLogger(__name__)

organization_bank_account_app = typer.Typer()


def validate_bank_account(gid: str):
    try:
        return test_db.OrganizationBankAccount.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@organization_bank_account_app.command("add")
def organization_bank_account_add(organization_gid: Optional[str] = None):
    if organization_gid:
        organization = validate_organization(organization_gid)
    else:
        organization = test_db.Organization()
        if _TyperOptions().interactive:
            test_db.OrganizationView(organization).edit()
    new_bank_account = test_db.OrganizationBankAccount(organization=organization)
    if _TyperOptions().interactive:
        test_db.BankAccountView(new_bank_account).edit()


@organization_bank_account_app.command("delete")
def organization_bank_account_delete(gid: str):
    bank_account = validate_bank_account(gid)
    bank_account.destroySelf()


@organization_bank_account_app.command("edit")
def organization_bank_account_edit(gid: str):
    bank_account = validate_bank_account(gid)
    test_db.BankAccountView(bank_account).edit()


@organization_bank_account_app.command("list")
def organization_bank_account_list(organization_gid: str):
    organization = validate_organization(organization_gid)
    test_db.BankAccountView.list(organization.bankAccounts)


@organization_bank_account_app.command("view")
def organization_bank_account_view(gid: str):
    bank_account = validate_bank_account(gid)
    test_db.BankAccountView(bank_account).viewDetails()
