import logging

from rich.progress import track
import typer

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_person

logger = logging.getLogger(__name__)

person_app = typer.Typer()


@person_app.command("add")
def person_add():
    person = test_db.Person()
    if _TyperOptions().interactive:
        test_db.PersonView(person).edit()
    print(person.gID)


@person_app.command("bulk-add")
def person_bulk_add(count: int = 100):
    logger.debug("Current person count: %d", test_db.Person.select().count())
    for i in track(range(count), description=f"Creating {count} people..."):
        test_db.Person()
    logger.debug("New person count: %d", test_db.Person.select().count())


@person_app.command("delete")
def delete_person(gid: str):
    person = validate_person(gid)
    person.destroySelf()


@person_app.command("edit")
def person_edit(gid: str):
    person = validate_person(gid)
    test_db.PersonView(person).edit()


@person_app.command("list")
def person_list():
    test_db.PersonView.list()


@person_app.command("view")
def person_view(gid: str):
    person = validate_person(gid)
    test_db.PersonView(person).viewDetails()
