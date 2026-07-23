import logging

import cmd2

import test_db

from ._base_command_set import BaseCommandSet

logger = logging.getLogger(__name__)


class OrgnizationCommandSet(BaseCommandSet):
    DEFAULT_CATEGORY = "Database"

    def do_tdb_organization_add(self, args):
        new_organization = test_db.Organization()
        if self._cmd.command_interaction:
            test_db.OrganizationView(new_organization).edit()
        self._cmd.poutput(new_organization.gID)

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
        organization = self.validate_organization(args.gid)
        test_db.OrganizationView(organization).edit()

    def do_tdb_organization_list(self, args):
        test_db.OrganizationView.list()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_organization_view(self, args):
        organization = self.validate_organization(args.gid)
        test_db.OrganizationView(organization).viewDetails()
