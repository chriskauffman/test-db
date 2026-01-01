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
class DebitCardCommandSet(BaseCommandSet):
    def validate_debit_card(self, gid: str):
        try:
            return test_db.DebitCard.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    optional_related_entity_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    optional_related_entity_parser.add_argument(
        "--entity_gid",
        help="related organizaiton or person's gID",
    )

    @cmd2.with_argparser(optional_related_entity_parser)
    def do_tdb_debit_card_add(self, args):
        readline.set_auto_history(False)
        if args.entity_gid:
            entity = self.validate_entity(args.entity_gid)
            test_db.DebitCardView.add(
                entity=entity, interactive=self._cmd.command_interaction
            )
        else:
            test_db.DebitCardView.add(interactive=self._cmd.command_interaction)
        readline.set_auto_history(True)

    connect_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    connect_parser.add_argument(
        "gid",
        help="object's gID",
    )
    connect_parser.add_argument(
        "entity_gid",
        help="related organizaiton or person's gID",
    )

    @cmd2.with_argparser(connect_parser)
    def do_tdb_debit_card_connect(self, args):
        debit_card = self.validate_debit_card(args.gid)
        entity = self.validate_entity(args.entity_gid)
        try:
            entity.addDebitCard(debit_card)
        except DuplicateEntryError:
            pass

    gid_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    gid_parser.add_argument(
        "gid",
        help="object's gID",
    )

    @cmd2.with_argparser(gid_parser)
    def do_tdb_debit_card_delete(self, args):
        debit_card = self.validate_debit_card(args.gid)
        debit_card.destroySelf()

    @cmd2.with_argparser(connect_parser)
    def do_tdb_debit_card_disconnect(self, args):
        debit_card = self.validate_debit_card(args.gid)
        entity = self.validate_entity(args.entity_gid)
        entity.removeDebitCard(debit_card)

    @cmd2.with_argparser(gid_parser)
    def do_tdb_debit_card_edit(self, args):
        readline.set_auto_history(False)
        debit_card = self.validate_debit_card(args.gid)
        test_db.DebitCardView(debit_card).edit()
        readline.set_auto_history(True)

    def do_tdb_debit_card_list(self, args):
        test_db.DebitCardView.list()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_debit_card_view(self, args):
        debit_card = self.validate_debit_card(args.gid)
        test_db.DebitCardView(debit_card).viewDetails()
