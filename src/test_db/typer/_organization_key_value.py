import logging
import sys

from sqlobject.dberrors import DuplicateEntryError  # type: ignore
import typer

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_organization

logger = logging.getLogger(__name__)

organization_key_value_app = typer.Typer()


@organization_key_value_app.command("add")
def organization_key_value_add(organization_gid: str, key: str, value: str):
    organization = validate_organization(organization_gid)
    try:
        key_value = organization.getKeyValueByKey(key, itemValue=value)
        if _TyperOptions().interactive:
            test_db.KeyValueView(key_value).edit()
    except DuplicateEntryError as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@organization_key_value_app.command("delete")
def organization_key_value_delete(organization_gid: str, key: str):
    organization = validate_organization(organization_gid)
    key_value = organization.getKeyValueByKey(key)
    if key_value:
        key_value.destroySelf()


@organization_key_value_app.command("edit")
def key_value_edit(organization_gid: str, key: str):
    organization = validate_organization(organization_gid)
    key_value = organization.getKeyValueByKey(key)
    test_db.KeyValueView(key_value).edit()


@organization_key_value_app.command("list")
def organization_key_value_list(organization_gid: str):
    organization = validate_organization(organization_gid)
    test_db.KeyValueView.list(organization.keyValues)


@organization_key_value_app.command("view")
def organization_key_value_view(organization_gid: str, key: str):
    organization = validate_organization(organization_gid)
    # ToDo: Needs fix: key will always exist
    key_value = organization.getKeyValueByKey(key)
    if key_value:
        test_db.KeyValueView(key_value).viewDetails()
