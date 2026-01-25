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

person_address_app = typer.Typer()


def validate_address(gid: str):
    try:
        return test_db.PersonAddress.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@person_address_app.command("add")
def person_address_add(person_gid: Optional[str] = None):
    if person_gid:
        person = validate_person(person_gid)
    else:
        person = test_db.Person()
        if _TyperOptions().interactive:
            test_db.PersonView(person).edit()
    new_address = test_db.PersonAddress(person=person)
    if _TyperOptions().interactive:
        test_db.AddressView(new_address).edit()
    print(new_address.gID)


@person_address_app.command("delete")
def person_address_delete(gid: str):
    address = validate_address(gid)
    address.destroySelf()


@person_address_app.command("edit")
def person_address_edit(gid: str):
    address = validate_address(gid)
    test_db.AddressView(address).edit()


@person_address_app.command("list")
def person_address_list(person_gid: Optional[str] = None):
    if person_gid:
        person = validate_person(person_gid)
        test_db.AddressView.list(person.addresses)
    else:
        test_db.AddressView.list(test_db.PersonAddress.select())


@person_address_app.command("view")
def person_address_view(gid: str):
    address = validate_address(gid)
    test_db.AddressView(address).viewDetails()
