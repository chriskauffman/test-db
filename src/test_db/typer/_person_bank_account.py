import logging
import sys

from formencode.validators import Invalid  # type: ignore
from rich.progress import track
from sqlobject import SQLObjectNotFound  # type: ignore
import typer

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Optional

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_person

logger = logging.getLogger(__name__)

person_bank_account_app = typer.Typer()


def validate_bank_account(gid: str):
    try:
        return test_db.PersonBankAccount.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@person_bank_account_app.command("add")
def person_bank_account_add(person_gid: Optional[str] = None):
    if person_gid:
        new_bank_account = test_db.PersonBankAccount(person=validate_person(person_gid))
    else:
        new_bank_account = test_db.PersonBankAccount()
    if _TyperOptions().interactive:
        test_db.BankAccountView(new_bank_account).edit()
    print(new_bank_account.gID)


@person_bank_account_app.command("bulk-add")
def bank_account_bulk_add(count: int = 100, person_gid: Optional[str] = None):
    person = None
    if person_gid:
        person = validate_person(person_gid)
    logger.debug(
        "Current counts: persons=%d, bankAccounts=%d",
        test_db.Person.select().count(),
        test_db.PersonBankAccount.select().count(),
    )
    for i in track(
        range(count), description=f"Creating {count} personal bank accounts..."
    ):
        test_db.PersonBankAccount(person=person)
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
def person_bank_account_list(person_gid: Optional[str] = None):
    if person_gid:
        person = validate_person(person_gid)
        test_db.BankAccountView.list(person.bankAccounts)
    else:
        test_db.BankAccountView.list(test_db.PersonBankAccount.select())


@person_bank_account_app.command("view")
def person_bank_account_view(gid: str):
    bank_account = validate_bank_account(gid)
    test_db.BankAccountView(bank_account).viewDetails()
