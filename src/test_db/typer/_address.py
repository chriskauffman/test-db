import sys

from formencode.validators import Invalid  # type: ignore
from sqlobject import SQLObjectNotFound  # type: ignore
from sqlobject.dberrors import DuplicateEntryError  # type: ignore
import typer
from typing_extensions import Optional

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_entity

address_app = typer.Typer()


def validate_address(gid: str):
    try:
        return test_db.Address.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@address_app.command("add")
def address_add(entity_gid: Optional[str] = None):
    if entity_gid:
        entity = validate_entity(entity_gid)
        test_db.AddressView.add(entity=entity, interactive=_TyperOptions().interactive)
    else:
        test_db.AddressView.add(interactive=_TyperOptions().interactive)


@address_app.command("connect")
def address_connect(gid: str, entity_gid: str):
    address = validate_address(gid)
    entity = validate_entity(entity_gid)
    try:
        entity.addAddress(address)
    except DuplicateEntryError:
        pass


@address_app.command("delete")
def address_delete(gid: str):
    address = validate_address(gid)
    address.destroySelf()


@address_app.command("disconnect")
def address_disconnect(gid: str, entity_gid: str):
    address = validate_address(gid)
    entity = validate_entity(entity_gid)
    entity.removeAddress(address)


@address_app.command("edit")
def address_edit(gid: str):
    address = validate_address(gid)
    test_db.AddressView(address).edit()


@address_app.command("list")
def address_list():
    test_db.AddressView.list()


@address_app.command("view")
def address_view(gid: str):
    address = validate_address(gid)
    test_db.AddressView(address).viewDetails()
