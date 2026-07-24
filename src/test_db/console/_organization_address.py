import logging

import cmd2
from formencode.validators import Invalid
from sqlobject import SQLObjectNotFound

import test_db

from ._base_command_set import BaseCommandSet

logger = logging.getLogger(__name__)


class OrganizationAddressCommandSet(BaseCommandSet):
    DEFAULT_CATEGORY = "Database"

    def validate_address(self, gid: str):
        try:
            return test_db.OrganizationAddress.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {exc!s}")

    optional_related_entity_parser = cmd2.Cmd2ArgumentParser()
    optional_related_entity_parser.add_argument(
        "--organization_gid",
        help="related organizaiton or person's gID",
    )

    @cmd2.with_argparser(optional_related_entity_parser)
    def do_tdb_organization_address_add(self, args):
        if args.organization_gid:
            new_address = test_db.OrganizationAddress(
                organization=self.validate_organization(args.organization_gid)
            )
        else:
            new_address = test_db.OrganizationAddress()
        if self._cmd.command_interaction:
            test_db.AddressView(new_address).edit()
        self._cmd.poutput(new_address.gID)

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
    def do_tdb_organization_address_delete(self, args):
        address = self.validate_address(args.gid)
        address.destroySelf()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_organization_address_edit(self, args):
        address = self.validate_address(args.gid)
        test_db.AddressView(address).edit()

    @cmd2.with_argparser(optional_related_entity_parser)
    def do_tdb_organization_address_list(self, args):
        if args.organization_gid:
            organization = self.validate_organization(args.organization_gid)
            test_db.AddressView.list(organization.addresses)
        else:
            test_db.AddressView.list(test_db.OrganizationAddress.select())

    @cmd2.with_argparser(gid_parser)
    def do_tdb_organization_address_view(self, args):
        address = self.validate_address(args.gid)
        test_db.AddressView(address).viewDetails()
