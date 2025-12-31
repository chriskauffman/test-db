import logging

import cmd2
from cmd2 import with_default_category

try:
    import gnureadline as readline  # type: ignore
except ImportError:
    import readline

from sqlobject import SQLObjectNotFound  # type: ignore
from sqlobject.dberrors import DuplicateEntryError  # type: ignore

from formencode.validators import Invalid  # type: ignore

import test_db

from ._base_command_set import BaseCommandSet

logger = logging.getLogger(__name__)


@with_default_category("Database")
class KeyValueCommandSet(BaseCommandSet):
    def validate_key(self, key: str):
        try:
            return test_db.KeyValue.byItemKey(key)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    tdb_add_key_value_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    tdb_add_key_value_parser.add_argument(
        "key",
        help="key",
    )
    tdb_add_key_value_parser.add_argument(
        "value",
        help="value",
    )

    @cmd2.with_argparser(tdb_add_key_value_parser)
    def do_tdb_add_key_value(self, args):
        readline.set_auto_history(False)
        try:
            test_db.KeyValueView.add(
                itemKey=args.key,
                itemValue=args.value,
                interactive=self._cmd.command_interaction,
            )
        except DuplicateEntryError as exc:
            self._cmd.perror(f"error: {str(exc)}")
        readline.set_auto_history(True)

    key_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    key_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(key_parser)
    def do_tdb_delete_key_value(self, args):
        if args.key in test_db.RESTRICTED_KEYS:
            self._cmd.perror(
                f"error: key '{args.key}' is restricted and cannot be deleted"
            )
            return
        key_value = self.validate_key(args.key)
        key_value.destroySelf()

    @cmd2.with_argparser(key_parser)
    def do_tdb_key_value_edit(self, args):
        readline.set_auto_history(False)
        if args.key in test_db.RESTRICTED_KEYS:
            self._cmd.perror(
                f"error: key '{args.key}' is restricted and cannot be edited"
            )
            return
        key_value = self.validate_key(args.key)
        test_db.KeyValueView(key_value).edit()
        readline.set_auto_history(True)

    def do_tdb_key_value_list(self, args):
        test_db.KeyValueView.list()

    @cmd2.with_argparser(key_parser)
    def do_tdb_key_value_view(self, args):
        key_value = self.validate_key(args.key)
        test_db.KeyValueView(key_value).viewDetails()
