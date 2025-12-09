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


@with_default_category("Database")
class PersonCommandSet(BaseCommandSet):
    def validate_person(self, gid: str):
        try:
            return test_db.Person.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    def do_tdb_add_person(self, args):
        readline.set_auto_history(False)
        test_db.PersonView.add(interactive=self._cmd.command_interaction)
        readline.set_auto_history(True)

    tdb_add_personal_key_value_secure_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    tdb_add_personal_key_value_secure_parser.add_argument(
        "person_gid",
        help="person's gID",
    )
    tdb_add_personal_key_value_secure_parser.add_argument(
        "key",
        help="key",
    )
    tdb_add_personal_key_value_secure_parser.add_argument(
        "value",
        help="value",
    )

    @cmd2.with_argparser(tdb_add_personal_key_value_secure_parser)
    def do_tdb_add_personal_key_value_secure(self, args):
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

    gid_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    gid_parser.add_argument(
        "gid",
        help="object's gID",
    )

    @cmd2.with_argparser(gid_parser)
    def do_tdb_delete_person(self, args):
        person = self.validate_person(args.gid)
        person.destroySelf()

    tdb_delete_personal_key_value_secure_parser = cmd2.Cmd2ArgumentParser(
        add_help=False
    )
    tdb_delete_personal_key_value_secure_parser.add_argument(
        "person_gid",
        help="person's gID",
    )
    tdb_delete_personal_key_value_secure_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(tdb_delete_personal_key_value_secure_parser)
    def do_tdb_delete_personal_key_value_secure(self, args):
        person = self.validate_person(args.person_gid)
        key_value = person.getPersonalKeyValueSecureByKey(args.key)
        if key_value:
            key_value.destroySelf()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_edit_person(self, args):
        readline.set_auto_history(False)
        person = self.validate_person(args.gid)
        test_db.PersonView(person).edit()
        readline.set_auto_history(True)

    def do_tdb_list_people(self, args):
        test_db.PersonView.list()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_view_person(self, args):
        person = self.validate_person(args.gid)
        test_db.PersonView(person).viewDetails()

    tdb_view_personal_key_value_secure_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    tdb_view_personal_key_value_secure_parser.add_argument(
        "person_gid",
        help="person's gID",
    )
    tdb_view_personal_key_value_secure_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(tdb_view_personal_key_value_secure_parser)
    def do_tdb_view_personal_key_value_secure(self, args):
        person = self.validate_person(args.person_gid)
        key_value = person.getPersonalKeyValueSecureByKey(args.key)
        if key_value:
            test_db.PersonalKeyValueSecureView(key_value).viewDetails()
