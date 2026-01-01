import logging
import typer

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_organization

logger = logging.getLogger(__name__)

organization_app = typer.Typer()


@organization_app.command("add")
def organization_add():
    test_db.OrganizationView.add(interactive=_TyperOptions().interactive)


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
