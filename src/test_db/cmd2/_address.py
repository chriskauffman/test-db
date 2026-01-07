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
class AddressCommandSet(BaseCommandSet):
    def validate_address(self, gid: str):
        try:
            return test_db.Address.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    optional_related_entity_parser = cmd2.Cmd2ArgumentParser()
    optional_related_entity_parser.add_argument(
        "--entity_gid",
        help="related organizaiton or person's gID",
    )

    @cmd2.with_argparser(optional_related_entity_parser)
    def do_tdb_address_add(self, args):
        readline.set_auto_history(False)
        if args.entity_gid:
            entity = self.validate_entity(args.gid)
            test_db.AddressView.add(
                entity=entity, interactive=self._cmd.command_interaction
            )
        else:
            test_db.AddressView.add(interactive=self._cmd.command_interaction)
        readline.set_auto_history(True)

    connect_parser = cmd2.Cmd2ArgumentParser()
    connect_parser.add_argument(
        "gid",
        help="object's gID",
    )
    connect_parser.add_argument(
        "entity_gid",
        help="related organizaiton or person's gID",
    )

    @cmd2.with_argparser(connect_parser)
    def do_tdb_address_connect(self, args):
        address = self.validate_address(args.gid)
        entity = self.validate_entity(args.entity_gid)
        try:
            entity.addAddress(address)
        except DuplicateEntryError:
            pass

    gid_parser = cmd2.Cmd2ArgumentParser()
    gid_parser.add_argument(
        "gid",
        help="object's gID",
    )

    @cmd2.with_argparser(gid_parser)
    def do_tdb_address_delete(self, args):
        address = self.validate_address(args.gid)
        address.destroySelf()

    @cmd2.with_argparser(connect_parser)
    def do_tdb_address_disconnect(self, args):
        address = self.validate_address(args.gid)
        entity = self.validate_entity(args.entity_gid)
        entity.removeAddress(address)

    @cmd2.with_argparser(gid_parser)
    def do_tdb_address_edit(self, args):
        readline.set_auto_history(False)
        address = self.validate_address(args.gid)
        test_db.AddressView(address).edit()
        readline.set_auto_history(True)

    def do_tdb_address_list(self, args):
        test_db.AddressView.list()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_address_view(self, args):
        address = self.validate_address(args.gid)
        test_db.AddressView(address).viewDetails()
