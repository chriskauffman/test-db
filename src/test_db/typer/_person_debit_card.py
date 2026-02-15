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
        new_debit_card = test_db.PersonDebitCard(person=validate_person(person_gid))
    else:
        new_debit_card = test_db.PersonDebitCard()
    if _TyperOptions().interactive:
        test_db.DebitCardView(new_debit_card).edit()
    print(new_debit_card.gID)


@person_debit_card_app.command("bulk-add")
def debit_card_bulk_add(count: int = 100, person_gid: Optional[str] = None):
    person = None
    if person_gid:
        person = validate_person(person_gid)
    logger.debug(
        "Current counts: persons=%d, debitCards=%d",
        test_db.Person.select().count(),
        test_db.PersonDebitCard.select().count(),
    )
    for i in track(
        range(count), description=f"Creating {count} personal debit cards..."
    ):
        test_db.PersonDebitCard(person=person)
    logger.debug(
        "Current counts: persons=%d, debitCards=%d",
        test_db.Person.select().count(),
        test_db.PersonDebitCard.select().count(),
    )


@person_debit_card_app.command("delete")
def debit_card_delete(gid: str):
    debit_card = validate_debit_card(gid)
    debit_card.destroySelf()


@person_debit_card_app.command("edit")
def person_debit_card_edit(gid: str):
    debit_card = validate_debit_card(gid)
    test_db.DebitCardView(debit_card).edit()


@person_debit_card_app.command("list")
def person_debit_card_list(person_gid: Optional[str] = None):
    if person_gid:
        person = validate_person(person_gid)
        test_db.DebitCardView.list(person.debitCards)
    else:
        test_db.DebitCardView.list(test_db.PersonDebitCard.select())


@person_debit_card_app.command("view")
def person_debit_card_view(gid: str):
    debit_card = validate_debit_card(gid)
    test_db.DebitCardView(debit_card).viewDetails()
