import cmd2
from cmd2 import with_default_category

try:
    import gnureadline as readline  # type: ignore
except ImportError:
    import readline

from sqlobject.dberrors import DuplicateEntryError  # type: ignore

import test_db

from ._base_command_set import BaseCommandSet


@with_default_category("Database")
class PersonalKeyValueSecureCommandSet(BaseCommandSet):
    tdb_personal_key_value_secure_add_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    tdb_personal_key_value_secure_add_parser.add_argument(
        "person_gid",
        help="person's gID",
    )
    tdb_personal_key_value_secure_add_parser.add_argument(
        "key",
        help="key",
    )
    tdb_personal_key_value_secure_add_parser.add_argument(
        "value",
        help="value",
    )

    @cmd2.with_argparser(tdb_personal_key_value_secure_add_parser)
    def do_tdb_personal_key_value_secure_add(self, args):
        readline.set_auto_history(False)
        person = self.validate_person(args.person_gid)
        try:
            test_db.PersonalKeyValueSecureView.add(
                person=person,
                key=args.key,
                value=args.value,
                interactive=self._cmd.command_interaction,
            )
        except DuplicateEntryError as exc:
            self._cmd.perror(f"error: {str(exc)}")
        readline.set_auto_history(False)

    tdb_personal_key_value_secure_delete_parser = cmd2.Cmd2ArgumentParser(
        add_help=False
    )
    tdb_personal_key_value_secure_delete_parser.add_argument(
        "person_gid",
        help="person's gID",
    )
    tdb_personal_key_value_secure_delete_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(tdb_personal_key_value_secure_delete_parser)
    def do_tdb_personal_key_value_secure_delete(self, args):
        person = self.validate_person(args.person_gid)
        key_value = person.getPersonalKeyValueSecureByKey(args.key)
        if key_value:
            key_value.destroySelf()

    tdb_personal_key_value_secure_view_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    tdb_personal_key_value_secure_view_parser.add_argument(
        "person_gid",
        help="person's gID",
    )
    tdb_personal_key_value_secure_view_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(tdb_personal_key_value_secure_view_parser)
    def do_tdb_personal_key_value_secure_view(self, args):
        person = self.validate_person(args.person_gid)
        key_value = person.getPersonalKeyValueSecureByKey(args.key)
        if key_value:
            test_db.PersonalKeyValueSecureView(key_value).viewDetails()
