import logging
import sys

import sqlobject
import typer
from formencode.validators import Invalid
from rich.progress import track
from sqlobject import SQLObjectNotFound

import test_db

from ._typer_options import _TyperOptions
from ._validate import validate_person

logger = logging.getLogger(__name__)

person_bank_account_app = typer.Typer()


def validate_bank_account(gid: str):
    try:
        return test_db.PersonBankAccount.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {exc!s}")
        sys.exit(1)


@person_bank_account_app.command("add")
def person_bank_account_add(person_gid: str | None = None):
    if person_gid:
        new_bank_account = test_db.PersonBankAccount(person=validate_person(person_gid))
    else:
        new_bank_account = test_db.PersonBankAccount()
    if _TyperOptions().interactive:
        test_db.BankAccountView(new_bank_account).edit()
    print(new_bank_account.gID)


@person_bank_account_app.command("bulk-add")
def bank_account_bulk_add(count: int = 100, person_gid: str | None = None):
    person = None
    if person_gid:
        person = validate_person(person_gid)
    logger.debug(
        "Current counts: persons=%d, bankAccounts=%d",
        test_db.Person.select().count(),
        test_db.PersonBankAccount.select().count(),
    )
    conn = sqlobject.sqlhub.processConnection
    trans = conn.transaction()
    try:
        for i in track(
            range(count), description=f"Creating {count} personal bank accounts..."
        ):
            test_db.PersonBankAccount(person=person, connection=trans)
        trans.commit()
    except Exception:
        trans.rollback()
        raise
    logger.debug(
        "Current counts: persons=%d, bankAccounts=%d",
        test_db.Person.select().count(),
        test_db.PersonBankAccount.select().count(),
    )


@person_bank_account_app.command("delete")
def person_bank_account_delete(gid: str):
    bank_account = validate_bank_account(gid)
    bank_account.destroySelf()


@person_bank_account_app.command("edit")
def person_bank_account_edit(gid: str):
    bank_account = validate_bank_account(gid)
    test_db.BankAccountView(bank_account).edit()


@person_bank_account_app.command("list")
def person_bank_account_list(person_gid: str | None = None):
    if person_gid:
        person = validate_person(person_gid)
        test_db.BankAccountView.list(person.bankAccounts)
    else:
        test_db.BankAccountView.list(test_db.PersonBankAccount.select())


@person_bank_account_app.command("view")
def person_bank_account_view(gid: str):
    bank_account = validate_bank_account(gid)
    test_db.BankAccountView(bank_account).viewDetails()
