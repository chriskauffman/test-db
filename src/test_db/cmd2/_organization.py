import logging

import cmd2
from cmd2 import with_default_category

try:
    import gnureadline as readline  # type: ignore
except ImportError:
    import readline

import test_db

from ._base_command_set import BaseCommandSet

logger = logging.getLogger(__name__)


@with_default_category("Database")
class OrgnizationCommandSet(BaseCommandSet):
    def do_tdb_organization_add(self, args):
        readline.set_auto_history(False)
        new_organization = test_db.Organization()
        if self._cmd.command_interaction:
            test_db.OrganizationView(new_organization).edit()
        self._cmd.poutput(new_organization.gID)
        readline.set_auto_history(True)

    gid_parser = cmd2.Cmd2ArgumentParser()
    gid_parser.add_argument(
        "gid",
        help="object's gID",
    )

    @cmd2.with_argparser(gid_parser)
    def do_tdb_organization_delete(self, args):
        organization = self.validate_organization(args.gid)
        organization.destroySelf()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_organization_edit(self, args):
        readline.set_auto_history(False)
        organization = self.validate_organization(args.gid)
        test_db.OrganizationView(organization).edit()
        readline.set_auto_history(True)

    def do_tdb_organization_list(self, args):
        test_db.OrganizationView.list()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_organization_view(self, args):
        organization = self.validate_organization(args.gid)
        test_db.OrganizationView(organization).viewDetails()
