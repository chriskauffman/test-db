import logging
import sys

from sqlobject.dberrors import DuplicateEntryError  # type: ignore
import typer

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_person

logger = logging.getLogger(__name__)

person_secure_key_value_app = typer.Typer()


@person_secure_key_value_app.command("add")
def person_secure_key_value_add(person_gid: str, key: str, value: str):
    person = validate_person(person_gid)
    try:
        key_value = person.getSecureKeyValueByKey(key, value=value)
        if _TyperOptions().interactive:
            test_db.KeyValueView(key_value).edit()
    except DuplicateEntryError as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@person_secure_key_value_app.command("delete")
def person_secure_key_value_delete(person_gid: str, key: str):
    person = validate_person(person_gid)
    key_value = person.getSecureKeyValueByKey(key)
    if key_value:
        key_value.destroySelf()


@person_secure_key_value_app.command("edit")
def key_value_edit(person_gid: str, key: str):
    person = validate_person(person_gid)
    key_value = person.getSecureKeyValueByKey(key)
    test_db.KeyValueView(key_value).edit()


@person_secure_key_value_app.command("list")
def person_secure_key_value_list(person_gid: str):
    person = validate_person(person_gid)
    test_db.KeyValueView.list(person.secureKeyValues)


@person_secure_key_value_app.command("view")
def person_secure_key_value_view(person_gid: str, key: str):
    person = validate_person(person_gid)
    # ToDo: Needs fix: key will always exist
    key_value = person.getSecureKeyValueByKey(key)
    if key_value:
        test_db.KeyValueView(key_value).viewDetails()
