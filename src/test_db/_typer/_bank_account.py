import sys

from formencode.validators import Invalid  # type: ignore
from sqlobject import SQLObjectNotFound  # type: ignore
from sqlobject.dberrors import DuplicateEntryError  # type: ignore
import typer
from typing_extensions import Optional

import test_db
from ._typer_options import _TyperOptions

bank_account_app = typer.Typer()


def validate_bank_account(gid: str):
    try:
        return test_db.BankAccount.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


def validate_entity(gid: str):
    try:
        return test_db.Person.byGID(gid)
    except Invalid as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)
    except SQLObjectNotFound:
        try:
            return test_db.Organization.byGID(gid)
        except SQLObjectNotFound:
            sys.stderr.write("error: person or organization not found")
            sys.exit(1)


@bank_account_app.command("add")
def bank_account_add(entity_gid: Optional[str] = None):
    if entity_gid:
        entity = validate_entity(entity_gid)
        test_db.BankAccountView.add(
            entity=entity, interactive=_TyperOptions().interactive
        )
    else:
        test_db.BankAccountView.add(interactive=_TyperOptions().interactive)


@bank_account_app.command("connect")
def bank_account_connect(gid: str, entity_gid: str):
    bank_account = validate_bank_account(gid)
    entity = validate_entity(entity_gid)
    try:
        entity.addBankAccount(bank_account)
    except DuplicateEntryError:
        pass


@bank_account_app.command("delete")
def bank_account_delete(gid: str):
    bank_account = validate_bank_account(gid)
    bank_account.destroySelf()


@bank_account_app.command("disconnect")
def bank_account_disconnect(gid: str, entity_gid: str):
    bank_account = validate_bank_account(gid)
    entity = validate_entity(entity_gid)
    entity.removeBankAccount(bank_account)


@bank_account_app.command("edit")
def bank_account_edit(gid: str):
    bank_account = validate_bank_account(gid)
    test_db.BankAccountView(bank_account).edit()


@bank_account_app.command("list")
def bank_account_list():
    test_db.BankAccountView.list()


@bank_account_app.command("view")
def bank_account_view(gid: str):
    bank_account = validate_bank_account(gid)
    test_db.BankAccountView(bank_account).viewDetails()
