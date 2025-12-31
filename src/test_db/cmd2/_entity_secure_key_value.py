import logging

import cmd2
from cmd2 import with_default_category

try:
    import gnureadline as readline  # type: ignore
except ImportError:
    import readline

from sqlobject.dberrors import DuplicateEntryError  # type: ignore

import test_db

from ._base_command_set import BaseCommandSet

logger = logging.getLogger(__name__)


@with_default_category("Database")
class EntitySecureKeyValueCommandSet(BaseCommandSet):
    tdb_entity_secure_key_value_add_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    tdb_entity_secure_key_value_add_parser.add_argument(
        "entity_gid",
        help="person or organization's gID",
    )
    tdb_entity_secure_key_value_add_parser.add_argument(
        "key",
        help="key",
    )
    tdb_entity_secure_key_value_add_parser.add_argument(
        "value",
        help="value",
    )

    @cmd2.with_argparser(tdb_entity_secure_key_value_add_parser)
    def do_tdb_entity_secure_key_value_add(self, args):
        readline.set_auto_history(False)
        entity = self.validate_entity(args.entity_gid)
        try:
            test_db.EntitySecureKeyValueView.add(
                entity=entity,
                itemKey=args.key,
                itemValue=args.value,
                interactive=self._cmd.command_interaction,
            )
        except DuplicateEntryError as exc:
            self._cmd.perror(f"error: {str(exc)}")
        readline.set_auto_history(False)

    tdb_entity_secure_key_value_delete_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    tdb_entity_secure_key_value_delete_parser.add_argument(
        "entity_gid",
        help="person's gID",
    )
    tdb_entity_secure_key_value_delete_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(tdb_entity_secure_key_value_delete_parser)
    def do_tdb_entity_secure_key_value_delete(self, args):
        entity = self.validate_entity(args.entity_gid)
        key_value = entity.getSecureKeyValueByKey(args.key)
        if key_value:
            key_value.destroySelf()

    def do_tdb_entity_secure_key_value_list(self, args):
        test_db.EntitySecureKeyValueView.list()

    tdb_entity_secure_key_value_view_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    tdb_entity_secure_key_value_view_parser.add_argument(
        "entity_gid",
        help="person's gID",
    )
    tdb_entity_secure_key_value_view_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(tdb_entity_secure_key_value_view_parser)
    def do_tdb_entity_secure_key_value_view(self, args):
        entity = self.validate_entity(args.entity_gid)
        key_value = entity.getSecureKeyValueByKey(args.key)
        if key_value:
            test_db.EntitySecureKeyValueView(key_value).viewDetails()
