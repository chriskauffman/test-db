import logging
import sys

from formencode.validators import Invalid  # type: ignore
from sqlobject import SQLObjectNotFound  # type: ignore
from sqlobject.dberrors import DuplicateEntryError  # type: ignore
import typer

import test_db
from ._typer_options import _TyperOptions

logger = logging.getLogger(__name__)

key_value_app = typer.Typer()


def validate_key(key: str):
    try:
        return test_db.KeyValue.byItemKey(key)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@key_value_app.command("add")
def key_value_add(key: str, value: str):
    try:
        key_value = test_db.KeyValue(itemKey=key, itemValue=value)
        if _TyperOptions().interactive:
            test_db.KeyValueView(key_value).edit()
    except DuplicateEntryError as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@key_value_app.command("delete")
def key_value_delete(key: str):
    if key in test_db.RESTRICTED_KEYS:
        sys.stderr.write(f"error: key '{key}' is restricted and cannot be deleted")
        sys.exit(1)
    key_value = validate_key(key)
    key_value.destroySelf()


@key_value_app.command("edit")
def key_value_edit(key: str):
    if key in test_db.RESTRICTED_KEYS:
        sys.stderr.write(f"error: key '{key}' is restricted and cannot be edited")
        sys.exit(1)
    key_value = validate_key(key)
    test_db.KeyValueView(key_value).edit()


@key_value_app.command("list")
def key_value_list():
    test_db.KeyValueView.list(test_db.KeyValue.select())


@key_value_app.command("view")
def key_value_view(key: str):
    key_value = validate_key(key)
    test_db.KeyValueView(key_value).viewDetails()
