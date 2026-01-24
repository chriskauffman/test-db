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
from ._validate import validate_person

logger = logging.getLogger(__name__)

person_debit_card_app = typer.Typer()


def validate_debit_card(gid: str):
    try:
        return test_db.PersonDebitCard.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@person_debit_card_app.command("add")
def person_debit_card_add(person_gid: Optional[str] = None):
    if person_gid:
        person = validate_person(person_gid)
    else:
        person = test_db.Person()
        if _TyperOptions().interactive:
            test_db.PersonView(person).edit()
    new_debit_card = test_db.PersonDebitCard(person=person)
    if _TyperOptions().interactive:
        test_db.DebitCardView(new_debit_card).edit()
    print(new_debit_card.gID)


@person_debit_card_app.command("delete")
def debit_card_delete(gid: str):
    debit_card = validate_debit_card(gid)
    debit_card.destroySelf()


@person_debit_card_app.command("edit")
def person_debit_card_edit(gid: str):
    debit_card = validate_debit_card(gid)
    test_db.DebitCardView(debit_card).edit()


@person_debit_card_app.command("list")
def person_debit_card_list(person_gid: str):
    person = validate_person(person_gid)
    test_db.DebitCardView.list(person.debitCards)


@person_debit_card_app.command("view")
def person_debit_card_view(gid: str):
    debit_card = validate_debit_card(gid)
    test_db.DebitCardView(debit_card).viewDetails()
