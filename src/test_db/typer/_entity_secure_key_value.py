import sys

from sqlobject.dberrors import DuplicateEntryError  # type: ignore
import typer

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_entity

entity_secure_key_value_app = typer.Typer()


@entity_secure_key_value_app.command("add")
def entity_secure_key_value_add(entity_gid: str, key: str, value: str):
    entity = validate_entity(entity_gid)
    try:
        test_db.EntitySecureKeyValueView.add(
            entity=entity,
            itemKey=key,
            itemValue=value,
            interactive=_TyperOptions().interactive,
        )
    except DuplicateEntryError as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@entity_secure_key_value_app.command("delete")
def entity_secure_key_value_delete(entity_gid: str, key: str):
    entity = validate_entity(entity_gid)
    key_value = entity.getSecureKeyValueByKey(key)
    if key_value:
        key_value.destroySelf()


@entity_secure_key_value_app.command("list")
def entity_secure_key_value_list():
    test_db.EntitySecureKeyValueView.list()


@entity_secure_key_value_app.command("view")
def entity_secure_key_value_view(entity_gid: str, key: str):
    entity = validate_entity(entity_gid)
    key_value = entity.getSecureKeyValueByKey(key)
    if key_value:
        test_db.EntitySecureKeyValueView(key_value).viewDetails()
