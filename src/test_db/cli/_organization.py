import logging

from rich.progress import track
import typer

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_organization

logger = logging.getLogger(__name__)

organization_app = typer.Typer()


@organization_app.command("add")
def organization_add():
    organization = test_db.Organization()
    if _TyperOptions().interactive:
        test_db.OrganizationView(organization).edit()
    print(organization.gID)


@organization_app.command("bulk-add")
def organization_bulk_add(count: int = 100):
    logger.debug(
        "Current organization count: %d", test_db.Organization.select().count()
    )
    for i in track(range(count), description=f"Creating {count} organizations..."):
        test_db.Organization()
    logger.debug("New organization count: %d", test_db.Organization.select().count())


@organization_app.command("delete")
def organization_delete(gid: str):
    organization = validate_organization(gid)
    organization.destroySelf()


@organization_app.command("edit")
def organization_edit(gid: str):
    organization = validate_organization(gid)
    test_db.OrganizationView(organization).edit()


@organization_app.command("list")
def organization_list():
    test_db.OrganizationView.list()


@organization_app.command("view")
def organization_view(gid: str):
    organization = validate_organization(gid)
    test_db.OrganizationView(organization).viewDetails()
