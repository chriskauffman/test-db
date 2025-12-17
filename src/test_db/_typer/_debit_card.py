import sys

from formencode.validators import Invalid  # type: ignore
from sqlobject import SQLObjectNotFound  # type: ignore
from sqlobject.dberrors import DuplicateEntryError  # type: ignore
import typer
from typing_extensions import Optional

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_entity

debit_card_app = typer.Typer()


def validate_debit_card(gid: str):
    try:
        return test_db.DebitCard.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@debit_card_app.command("add")
def debit_card_add(entity_gid: Optional[str] = None):
    if entity_gid:
        entity = validate_entity(entity_gid)
        test_db.DebitCardView.add(
            entity=entity, interactive=_TyperOptions().interactive
        )
    else:
        test_db.DebitCardView.add(interactive=_TyperOptions().interactive)


@debit_card_app.command("connect")
def debit_card_connect(gid: str, entity_gid: str):
    debit_card = validate_debit_card(gid)
    entity = validate_entity(entity_gid)
    try:
        entity.addDebitCard(debit_card)
    except DuplicateEntryError:
        pass


@debit_card_app.command("delete")
def debit_card_delete(gid: str):
    debit_card = validate_debit_card(gid)
    debit_card.destroySelf()


@debit_card_app.command("disconnect")
def debit_card_disconnect(gid: str, entity_gid: str):
    debit_card = validate_debit_card(gid)
    entity = validate_entity(entity_gid)
    entity.removeDebitCard(debit_card)


@debit_card_app.command("edit")
def debit_card_edit(gid: str):
    debit_card = validate_debit_card(gid)
    test_db.DebitCardView(debit_card).edit()


@debit_card_app.command("list")
def debit_card_list():
    test_db.DebitCardView.list()


@debit_card_app.command("view")
def debit_card_view(gid: str):
    debit_card = validate_debit_card(gid)
    test_db.DebitCardView(debit_card).viewDetails()
