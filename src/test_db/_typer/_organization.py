import sys

from formencode.validators import Invalid  # type: ignore
from sqlobject import SQLObjectNotFound  # type: ignore
import typer

import test_db
from ._typer_options import _TyperOptions

organization_app = typer.Typer()


def validate_orgnization(gid: str):
    try:
        return test_db.Organization.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@organization_app.command("add")
def organization_add():
    test_db.OrganizationView.add(interactive=_TyperOptions().interactive)


@organization_app.command("delete")
def organization_delete(gid: str):
    organization = validate_orgnization(gid)
    organization.destroySelf()


@organization_app.command("edit")
def organization_edit(gid: str):
    organization = validate_orgnization(gid)
    test_db.OrganizationView(organization).edit()


@organization_app.command("list")
def organization_list():
    test_db.OrganizationView.list()


@organization_app.command("view")
def organization_view(gid: str):
    organization = validate_orgnization(gid)
    test_db.OrganizationView(organization).viewDetails()
