import logging
import sys

import sqlobject
import typer
from formencode.validators import Invalid
from rich.progress import track
from sqlobject import SQLObjectNotFound

import test_db

from ._typer_options import _TyperOptions
from ._validate import validate_organization

logger = logging.getLogger(__name__)

organization_address_app = typer.Typer()


def validate_address(gid: str):
    try:
        return test_db.OrganizationAddress.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {exc!s}")
        sys.exit(1)


@organization_address_app.command("add")
def organization_address_add(organization_gid: str | None = None):
    if organization_gid:
        new_address = test_db.OrganizationAddress(
            organization=validate_organization(organization_gid)
        )
    else:
        new_address = test_db.OrganizationAddress()
    if _TyperOptions().interactive:
        test_db.AddressView(new_address).edit()
    print(new_address.gID)


@organization_address_app.command("bulk-add")
def address_bulk_add(count: int = 100, organization_gid: str | None = None):
    organization = None
    if organization_gid:
        organization = validate_organization(organization_gid)
    logger.debug(
        "Current counts: organizations=%d, addresses=%d",
        test_db.Organization.select().count(),
        test_db.OrganizationAddress.select().count(),
    )
    conn = sqlobject.sqlhub.processConnection
    trans = conn.transaction()
    try:
        for i in track(
            range(count), description=f"Creating {count} organization addresses..."
        ):
            test_db.OrganizationAddress(organization=organization, connection=trans)
        trans.commit()
    except Exception:
        trans.rollback()
        raise
    logger.debug(
        "Current counts: organizations=%d, addresses=%d",
        test_db.Organization.select().count(),
        test_db.OrganizationAddress.select().count(),
    )


@organization_address_app.command("delete")
def organization_address_delete(gid: str):
    address = validate_address(gid)
    address.destroySelf()


@organization_address_app.command("edit")
def organization_address_edit(gid: str):
    address = validate_address(gid)
    test_db.AddressView(address).edit()


@organization_address_app.command("list")
def organization_address_list(organization_gid: str | None = None):
    if organization_gid:
        organization = validate_organization(organization_gid)
        test_db.AddressView.list(organization.addresses)
    else:
        test_db.AddressView.list(test_db.OrganizationAddress.select())


@organization_address_app.command("view")
def organization_address_view(gid: str):
    address = validate_address(gid)
    test_db.AddressView(address).viewDetails()
