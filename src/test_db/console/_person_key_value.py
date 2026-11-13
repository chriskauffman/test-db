import logging

import cmd2
from sqlobject.dberrors import DuplicateEntryError

import test_db

from ._base_command_set import BaseCommandSet

logger = logging.getLogger(__name__)


class PersonKeyValueCommandSet(BaseCommandSet):
    DEFAULT_CATEGORY = "Database"

    person_key_value_add_parser = cmd2.Cmd2ArgumentParser()
    person_key_value_add_parser.add_argument(
        "person_gid",
        help="person or organization's gID",
    )
    person_key_value_add_parser.add_argument(
        "key",
        help="key",
    )
    person_key_value_add_parser.add_argument(
        "value",
        help="value",
    )

    @cmd2.with_argparser(person_key_value_add_parser)
    def do_person_key_value_add(self, args):
        person = self.validate_person(args.person_gid)
        try:
            key_value = test_db.PersonKeyValue(
                person=person,
                key=args.key,
                value=args.value,
            )
            if self._cmd.command_interaction:
                test_db.KeyValueView(key_value).edit()
        except DuplicateEntryError as exc:
            self._cmd.perror(f"error: {exc!s}")

    person_key_value_delete_parser = cmd2.Cmd2ArgumentParser()
    person_key_value_delete_parser.add_argument(
        "person_gid",
        help="person's gID",
    )
    person_key_value_delete_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(person_key_value_delete_parser)
    def do_person_key_value_delete(self, args):
        person = self.validate_person(args.person_gid)
        key_value = self.validate_key_value(person.keyValuesSelect, args.key)
        key_value.destroySelf()

    person_key_value_list_parser = cmd2.Cmd2ArgumentParser()
    person_key_value_list_parser.add_argument(
        "person_gid",
        help="person's gID",
    )

    @cmd2.with_argparser(person_key_value_list_parser)
    def do_person_key_value_list(self, args):
        person = self.validate_person(args.person_gid)
        test_db.KeyValueView.list(person.keyValues)

    person_key_value_view_parser = cmd2.Cmd2ArgumentParser()
    person_key_value_view_parser.add_argument(
        "person_gid",
        help="person's gID",
    )
    person_key_value_view_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(person_key_value_view_parser)
    def do_person_key_value_view(self, args):
        person = self.validate_person(args.person_gid)
        key_value = self.validate_key_value(person.keyValuesSelect, args.key)
        test_db.KeyValueView(key_value).viewDetails()
