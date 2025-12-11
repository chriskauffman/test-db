import sys

from formencode.validators import Invalid  # type: ignore
from sqlobject import SQLObjectNotFound  # type: ignore
from sqlobject.dberrors import DuplicateEntryError  # type: ignore
import typer

import test_db
from ._typer_options import _TyperOptions

personal_key_value_secure_app = typer.Typer()


def validate_person(gid: str):
    try:
        return test_db.Person.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@personal_key_value_secure_app.command("add")
def personal_key_value_secure_add(person_gid: str, key: str, value: str):
    person = validate_person(person_gid)
    try:
        test_db.PersonalKeyValueSecureView.add(
            person=person, key=key, value=value, interactive=_TyperOptions().interactive
        )
    except DuplicateEntryError as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@personal_key_value_secure_app.command("delete")
def personal_key_value_secure_delete(person_gid: str, key: str):
    person = validate_person(person_gid)
    key_value = person.getPersonalKeyValueSecureByKey(key)
    if key_value:
        key_value.destroySelf()


@personal_key_value_secure_app.command("personal-key-value-secure")
def personal_key_value_secure_list():
    test_db.PersonalKeyValueSecureView.list()


@personal_key_value_secure_app.command("view")
def personal_key_value_secure_view(person_gid: str, key: str):
    person = validate_person(person_gid)
    key_value = person.getPersonalKeyValueSecureByKey(key)
    if key_value:
        test_db.PersonalKeyValueSecureView(key_value).viewDetails()
