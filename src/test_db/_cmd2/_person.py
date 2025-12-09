import cmd2
from cmd2 import with_default_category

try:
    import gnureadline as readline  # type: ignore
except ImportError:
    import readline

from sqlobject import SQLObjectNotFound  # type: ignore

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

    def do_tdb_person_add(self, args):
        readline.set_auto_history(False)
        test_db.PersonView.add(interactive=self._cmd.command_interaction)
        readline.set_auto_history(True)

    gid_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    gid_parser.add_argument(
        "gid",
        help="object's gID",
    )

    @cmd2.with_argparser(gid_parser)
    def do_tdb_person_delete(self, args):
        person = self.validate_person(args.gid)
        person.destroySelf()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_person_edit(self, args):
        readline.set_auto_history(False)
        person = self.validate_person(args.gid)
        test_db.PersonView(person).edit()
        readline.set_auto_history(True)

    def do_tdb_person_list(self, args):
        test_db.PersonView.list()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_person_view(self, args):
        person = self.validate_person(args.gid)
        test_db.PersonView(person).viewDetails()
