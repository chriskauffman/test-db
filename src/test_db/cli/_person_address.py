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

person_address_app = typer.Typer()


def validate_address(gid: str):
    try:
        return test_db.PersonAddress.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {exc!s}")
        sys.exit(1)


@person_address_app.command("add")
def person_address_add(person_gid: str | None = None):
    if person_gid:
        new_address = test_db.PersonAddress(person=validate_person(person_gid))
    else:
        new_address = test_db.PersonAddress()
    if _TyperOptions().interactive:
        test_db.AddressView(new_address).edit()
    print(new_address.gID)


@person_address_app.command("bulk-add")
def address_bulk_add(count: int = 100, person_gid: str | None = None):
    person = None
    if person_gid:
        person = validate_person(person_gid)
    logger.debug(
        "Current counts: persons=%d, addresses=%d",
        test_db.Person.select().count(),
        test_db.PersonAddress.select().count(),
    )
    conn = sqlobject.sqlhub.processConnection
    trans = conn.transaction()
    try:
        for i in track(
            range(count), description=f"Creating {count} personal addresses..."
        ):
            test_db.PersonAddress(person=person, connection=trans)
        trans.commit()
    except Exception:
        trans.rollback()
        raise
    logger.debug(
        "Current counts: persons=%d, addresses=%d",
        test_db.Person.select().count(),
        test_db.PersonAddress.select().count(),
    )


@person_address_app.command("delete")
def person_address_delete(gid: str):
    address = validate_address(gid)
    address.destroySelf()


@person_address_app.command("edit")
def person_address_edit(gid: str):
    address = validate_address(gid)
    test_db.AddressView(address).edit()


@person_address_app.command("list")
def person_address_list(person_gid: str | None = None):
    if person_gid:
        person = validate_person(person_gid)
        test_db.AddressView.list(person.addresses)
    else:
        test_db.AddressView.list(test_db.PersonAddress.select())


@person_address_app.command("view")
def person_address_view(gid: str):
    address = validate_address(gid)
    test_db.AddressView(address).viewDetails()
