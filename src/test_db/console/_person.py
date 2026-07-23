import logging

import cmd2

import test_db

from ._base_command_set import BaseCommandSet

logger = logging.getLogger(__name__)


class PersonCommandSet(BaseCommandSet):
    DEFAULT_CATEGORY = "Database"

    def do_tdb_person_add(self, args):
        new_person = test_db.Person()
        if self._cmd.command_interaction:
            test_db.PersonView(new_person).edit()
        self._cmd.poutput(new_person.gID)

    gid_parser = cmd2.Cmd2ArgumentParser()
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
        person = self.validate_person(args.gid)
        test_db.PersonView(person).edit()

    def do_tdb_person_list(self, args):
        test_db.PersonView.list()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_person_view(self, args):
        person = self.validate_person(args.gid)
        test_db.PersonView(person).viewDetails()
