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
class PersonDebitCardCommandSet(BaseCommandSet):
    def validate_debit_card(self, gid: str):
        try:
            return test_db.PersonDebitCard.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    optional_related_entity_parser = cmd2.Cmd2ArgumentParser()
    optional_related_entity_parser.add_argument(
        "--person_gid",
        help="related organizaiton or person's gID",
    )

    @cmd2.with_argparser(optional_related_entity_parser)
    def do_tdb_person_debit_card_add(self, args):
        readline.set_auto_history(False)
        if args.person_gid:
            new_debit_card = test_db.PersonDebitCard(
                person=self.validate_person(args.person_gid)
            )
        else:
            new_debit_card = test_db.PersonDebitCard()
        if self._cmd.command_interaction:
            test_db.DebitCardView(new_debit_card).edit()
        self._cmd.poutput(new_debit_card.gID)
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
    def do_tdb_person_debit_card_delete(self, args):
        debit_card = self.validate_debit_card(args.gid)
        debit_card.destroySelf()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_person_debit_card_edit(self, args):
        readline.set_auto_history(False)
        debit_card = self.validate_debit_card(args.gid)
        test_db.DebitCardView(debit_card).edit()
        readline.set_auto_history(True)

    @cmd2.with_argparser(optional_related_entity_parser)
    def do_tdb_person_debit_card_list(self, args):
        if args.person_gid:
            person = self.validate_person(args.person_gid)
            test_db.DebitCardView.list(person.debitCards)
        else:
            test_db.DebitCardView.list(test_db.PersonDebitCard.select())

    @cmd2.with_argparser(gid_parser)
    def do_tdb_person_debit_card_view(self, args):
        debit_card = self.validate_debit_card(args.gid)
        test_db.DebitCardView(debit_card).viewDetails()
