import logging
import sys

import sqlobject
import typer
from formencode.validators import Invalid
from rich.progress import track
from sqlobject import SQLObjectNotFound

import test_db

from ._typer_options import _TyperOptions
from ._validate import validate_organization

logger = logging.getLogger(__name__)

organization_bank_account_app = typer.Typer()


def validate_bank_account(gid: str):
    try:
        return test_db.OrganizationBankAccount.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {exc!s}")
        sys.exit(1)


@organization_bank_account_app.command("add")
def organization_bank_account_add(organization_gid: str | None = None):
    if organization_gid:
        new_bank_account = test_db.OrganizationBankAccount(
            organization=validate_organization(organization_gid)
        )
    else:
        new_bank_account = test_db.OrganizationBankAccount()
    if _TyperOptions().interactive:
        test_db.BankAccountView(new_bank_account).edit()
    print(new_bank_account.gID)


@organization_bank_account_app.command("bulk-add")
def bank_account_bulk_add(count: int = 100, organization_gid: str | None = None):
    organization = None
    if organization_gid:
        organization = validate_organization(organization_gid)
    logger.debug(
        "Current counts: organizations=%d, bankAccounts=%d",
        test_db.Organization.select().count(),
        test_db.OrganizationBankAccount.select().count(),
    )
    conn = sqlobject.sqlhub.processConnection
    trans = conn.transaction()
    try:
        for i in track(
            range(count), description=f"Creating {count} organization bank accounts..."
        ):
            test_db.OrganizationBankAccount(organization=organization, connection=trans)
        trans.commit()
    except Exception:
        trans.rollback()
        raise
    logger.debug(
        "Current counts: organizations=%d, bankAccounts=%d",
        test_db.Organization.select().count(),
        test_db.OrganizationBankAccount.select().count(),
    )


@organization_bank_account_app.command("delete")
def organization_bank_account_delete(gid: str):
    bank_account = validate_bank_account(gid)
    bank_account.destroySelf()


@organization_bank_account_app.command("edit")
def organization_bank_account_edit(gid: str):
    bank_account = validate_bank_account(gid)
    test_db.BankAccountView(bank_account).edit()


@organization_bank_account_app.command("list")
def organization_bank_account_list(organization_gid: str | None = None):
    if organization_gid:
        organization = validate_organization(organization_gid)
        test_db.BankAccountView.list(organization.bankAccounts)
    else:
        test_db.BankAccountView.list(test_db.OrganizationBankAccount.select())


@organization_bank_account_app.command("view")
def organization_bank_account_view(gid: str):
    bank_account = validate_bank_account(gid)
    test_db.BankAccountView(bank_account).viewDetails()
