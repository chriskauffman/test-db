import logging

import cmd2
from sqlobject.dberrors import DuplicateEntryError

import test_db

from ._base_command_set import BaseCommandSet

logger = logging.getLogger(__name__)


class OrganizationKeyValueCommandSet(BaseCommandSet):
    DEFAULT_CATEGORY = "Database"

    tdb_organization_key_value_add_parser = cmd2.Cmd2ArgumentParser()
    tdb_organization_key_value_add_parser.add_argument(
        "organization_gid",
        help="person or organization's gID",
    )
    tdb_organization_key_value_add_parser.add_argument(
        "key",
        help="key",
    )
    tdb_organization_key_value_add_parser.add_argument(
        "value",
        help="value",
    )

    @cmd2.with_argparser(tdb_organization_key_value_add_parser)
    def do_tdb_organization_key_value_add(self, args):
        organization = self.validate_organization(args.organization_gid)
        try:
            key_value = test_db.OrganizationKeyValue(
                organization=organization,
                key=args.key,
                value=args.value,
            )
            if self._cmd.command_interaction:
                test_db.KeyValueView(key_value).edit()
        except DuplicateEntryError as exc:
            self._cmd.perror(f"error: {exc!s}")

    tdb_organization_key_value_delete_parser = cmd2.Cmd2ArgumentParser()
    tdb_organization_key_value_delete_parser.add_argument(
        "organization_gid",
        help="person's gID",
    )
    tdb_organization_key_value_delete_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(tdb_organization_key_value_delete_parser)
    def do_tdb_organization_key_value_delete(self, args):
        organization = self.validate_organization(args.organization_gid)
        key_value = organization.getKeyValueByKey(args.key)
        if key_value:
            key_value.destroySelf()

    tdb_organization_key_value_list_parser = cmd2.Cmd2ArgumentParser()
    tdb_organization_key_value_list_parser.add_argument(
        "organization_gid",
        help="person or organization's gID",
    )

    @cmd2.with_argparser(tdb_organization_key_value_list_parser)
    def do_tdb_organization_key_value_list(self, args):
        organization = self.validate_organization(args.organization_gid)
        test_db.KeyValueView.list(organization.keyValues)

    tdb_organization_key_value_view_parser = cmd2.Cmd2ArgumentParser()
    tdb_organization_key_value_view_parser.add_argument(
        "organization_gid",
        help="person's gID",
    )
    tdb_organization_key_value_view_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(tdb_organization_key_value_view_parser)
    def do_tdb_organization_key_value_view(self, args):
        organization = self.validate_organization(args.organization_gid)
        key_value = organization.getKeyValueByKey(args.key)
        if key_value:
            test_db.KeyValueView(key_value).viewDetails()
