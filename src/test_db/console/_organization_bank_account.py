import logging

import cmd2
from formencode.validators import Invalid
from sqlobject import SQLObjectNotFound

import test_db

from ._base_command_set import BaseCommandSet

logger = logging.getLogger(__name__)


class OrganizationBankAccountCommandSet(BaseCommandSet):
    DEFAULT_CATEGORY = "Database"

    def validate_bank_account(self, gid: str):
        try:
            return test_db.OrganizationBankAccount.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {exc!s}")

    optional_related_entity_parser = cmd2.Cmd2ArgumentParser()
    optional_related_entity_parser.add_argument(
        "--organization_gid",
        help="related organizaiton or person's gID",
    )

    @cmd2.with_argparser(optional_related_entity_parser)
    def do_tdb_organization_bank_account_add(self, args):
        if args.organization_gid:
            new_bank_account = test_db.OrganizationBankAccount(
                organization=self.validate_organization(args.organization_gid)
            )
        else:
            new_bank_account = test_db.OrganizationBankAccount()
        if self._cmd.command_interaction:
            test_db.BankAccountView(new_bank_account).edit()
        self._cmd.poutput(new_bank_account.gID)

    connect_parser = cmd2.Cmd2ArgumentParser()
    connect_parser.add_argument(
        "gid",
        help="object's gID",
    )
    connect_parser.add_argument(
        "organization_gid",
        help="related organizaiton or person's gID",
    )

    gid_parser = cmd2.Cmd2ArgumentParser()
    gid_parser.add_argument(
        "gid",
        help="object's gID",
    )

    @cmd2.with_argparser(gid_parser)
    def do_tdb_organization_bank_account_delete(self, args):
        bank_account = self.validate_bank_account(args.gid)
        bank_account.destroySelf()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_organization_bank_account_edit(self, args):
        bank_account = self.validate_bank_account(args.gid)
        test_db.BankAccountView(bank_account).edit()

    @cmd2.with_argparser(optional_related_entity_parser)
    def do_tdb_organization_bank_account_list(self, args):
        if args.organization_gid:
            organization = self.validate_organization(args.organization_gid)
            test_db.BankAccountView.list(organization.bankAccounts)
        else:
            test_db.BankAccountView.list(test_db.OrganizationBankAccount.select())

    @cmd2.with_argparser(gid_parser)
    def do_tdb_organization_bank_account_view(self, args):
        bank_account = self.validate_bank_account(args.gid)
        test_db.BankAccountView(bank_account).viewDetails()
