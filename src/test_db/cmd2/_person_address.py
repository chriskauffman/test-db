import logging

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

logger = logging.getLogger(__name__)


@with_default_category("Database")
class PersonAddressCommandSet(BaseCommandSet):
    def validate_address(self, gid: str):
        try:
            return test_db.PersonAddress.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    optional_related_entity_parser = cmd2.Cmd2ArgumentParser()
    optional_related_entity_parser.add_argument(
        "--person_gid",
        help="related organizaiton or person's gID",
    )

    @cmd2.with_argparser(optional_related_entity_parser)
    def do_tdb_person_address_add(self, args):
        readline.set_auto_history(False)
        if args.person_gid:
            person = self.validate_person(args.person_gid)
        else:
            person = test_db.Person()
            if self._cmd.command_interaction:
                test_db.PersonView(person).edit()
        new_address = test_db.PersonAddress(person=person)
        if self._cmd.command_interaction:
            test_db.AddressView(new_address).edit()
        readline.set_auto_history(True)

    connect_parser = cmd2.Cmd2ArgumentParser()
    connect_parser.add_argument(
        "gid",
        help="object's gID",
    )
    connect_parser.add_argument(
        "person_gid",
        help="related organizaiton or person's gID",
    )

    gid_parser = cmd2.Cmd2ArgumentParser()
    gid_parser.add_argument(
        "gid",
        help="object's gID",
    )

    @cmd2.with_argparser(gid_parser)
    def do_tdb_person_address_delete(self, args):
        address = self.validate_address(args.gid)
        address.destroySelf()

    @cmd2.with_argparser(connect_parser)
    def do_tdb_person_address_disconnect(self, args):
        address = self.validate_address(args.gid)
        person = self.validate_person(args.person_gid)
        person.removeAddress(address)

    @cmd2.with_argparser(gid_parser)
    def do_tdb_person_address_edit(self, args):
        readline.set_auto_history(False)
        address = self.validate_address(args.gid)
        test_db.AddressView(address).edit()
        readline.set_auto_history(True)

    def do_tdb_person_address_list(self, args):
        test_db.AddressView.list()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_person_address_view(self, args):
        address = self.validate_address(args.gid)
        test_db.AddressView(address).viewDetails()
