import typer

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_person

person_app = typer.Typer()


@person_app.command("add")
def person_add():
    test_db.PersonView.add(interactive=_TyperOptions().interactive)


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
