import cmd2
from cmd2 import CommandSet, with_default_category

try:
    import gnureadline as readline  # type: ignore
except ImportError:
    import readline

from sqlobject import SQLObjectNotFound  # type: ignore
from sqlobject.dberrors import DuplicateEntryError  # type: ignore

from formencode.validators import Invalid  # type: ignore

import test_db


@with_default_category("Database")
class TestDBCommandSet(CommandSet):
    # Parent Cmd should be self._cmd

    def validate_address(self, gid: str):
        try:
            return test_db.Address.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    def validate_bank_account(self, gid: str):
        try:
            return test_db.BankAccount.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    def validate_debit_card(self, gid: str):
        try:
            return test_db.DebitCard.byGID(self, gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    def validate_entity(self, gid: str):
        try:
            return test_db.Person.byGID(gid)
        except Invalid as exc:
            self._cmd.perror(f"error: {str(exc)}")

        except SQLObjectNotFound:
            try:
                return test_db.Organization.byGID(gid)
            except SQLObjectNotFound:
                self._cmd.perror("error: person or organization not found")

    def validate_job(self, gid: str):
        try:
            return test_db.Job.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    def validate_key(self, key: str):
        try:
            return test_db.KeyValue.byKey(key)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    def validate_orgnization(self, gid: str):
        try:
            return test_db.Organization.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    def validate_person(self, gid: str):
        try:
            return test_db.Person.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    optional_related_entity_parser = cmd2.Cmd2ArgumentParser(add_help=False)
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

    @cmd2.with_argparser(optional_related_entity_parser)
    def do_tdb_add_bank_acount(self, args):
        readline.set_auto_history(False)
        if args.entity_gid:
            entity = self.validate_entity(args.entity_gid)
            test_db.BankAccountView.add(
                entity=entity, interactive=self._cmd.command_interaction
            )
        else:
            test_db.BankAccountView.add(interactive=self._cmd.command_interaction)
        readline.set_auto_history(True)

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

    tdb_job_add_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    tdb_job_add_parser.add_argument(
        "--organization_gid",
        help="related organization's gID",
    )
    tdb_job_add_parser.add_argument(
        "--person_gid",
        help="related person's gID",
    )

    @cmd2.with_argparser(tdb_job_add_parser)
    def do_tdb_job_add(self, args):
        readline.set_auto_history(False)
        organization = None
        person = None
        if args.organization_gid:
            organization = self.validate_orgnization(args.organization_gid)
        if args.person_gid:
            person = self.validate_person(args.person_gid)
        test_db.JobView.add(
            organization=organization,
            person=person,
            interactive=self._cmd.command_interaction,
        )
        readline.set_auto_history(True)

    tdb_add_key_value_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    tdb_add_key_value_parser.add_argument(
        "key",
        help="key",
    )
    tdb_add_key_value_parser.add_argument(
        "value",
        help="value",
    )

    @cmd2.with_argparser(tdb_add_key_value_parser)
    def do_tdb_key_value_add(self, args):
        readline.set_auto_history(False)
        try:
            test_db.KeyValueView.add(
                key=args.key,
                value=args.value,
                interactive=self._cmd.command_interaction,
            )
        except DuplicateEntryError as exc:
            self._cmd.perror(f"error: {str(exc)}")
        readline.set_auto_history(True)

    def do_tdb_organization_add(self, args):
        readline.set_auto_history(False)
        test_db.OrganizationView.add(interactive=self._cmd.command_interaction)
        readline.set_auto_history(True)

    def do_tdb_person_add(self, args):
        readline.set_auto_history(False)
        test_db.PersonView.add(interactive=self._cmd.command_interaction)
        readline.set_auto_history(True)

    tdb_personal_key_value_secure_add_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    tdb_personal_key_value_secure_add_parser.add_argument(
        "person_gid",
        help="person's gID",
    )
    tdb_personal_key_value_secure_add_parser.add_argument(
        "key",
        help="key",
    )
    tdb_personal_key_value_secure_add_parser.add_argument(
        "value",
        help="value",
    )

    @cmd2.with_argparser(tdb_personal_key_value_secure_add_parser)
    def do_tdb_person_addal_key_value_secure(self, args):
        readline.set_auto_history(False)
        person = self.validate_person(args.person_gid)
        try:
            test_db.PersonalKeyValueSecureView.add(
                person=person,
                key=args.key,
                value=args.value,
                interactive=self._cmd.command_interaction,
            )
        except DuplicateEntryError as exc:
            self._cmd.perror(f"error: {str(exc)}")
        readline.set_auto_history(False)

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
    def do_tdb_address_connect(self, args):
        address = self.validate_address(args.gid)
        entity = self.validate_entity(args.entity_gid)
        try:
            entity.addAddress(address)
        except DuplicateEntryError:
            pass

    @cmd2.with_argparser(connect_parser)
    def do_tdb_bank_account_connect(self, args):
        bank_account = self.validate_bank_account(args.gid)
        entity = self.validate_entity(args.entity_gid)
        try:
            entity.addBankAccount(bank_account)
        except DuplicateEntryError:
            pass

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
    def do_tdb_address_delete(self, args):
        address = self.validate_address(args.gid)
        address.destroySelf()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_bank_account_delete(self, args):
        bank_account = self.validate_bank_account(args.gid)
        bank_account.destroySelf()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_debit_card_delete(self, args):
        debit_card = self.validate_debit_card(args.gid)
        debit_card.destroySelf()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_job_delete(self, args):
        job = self.validate_job(args.gid)
        job.destroySelf()

    key_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    key_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(key_parser)
    def do_tdb_key_value_delete(self, args):
        if args.key in test_db.RESTRICTED_KEYS:
            self._cmd.perror(
                f"error: key '{args.key}' is restricted and cannot be deleted"
            )

        key_value = self.validate_key(args.key)
        key_value.destroySelf()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_organization_delete(self, args):
        organization = self.validate_orgnization(args.gid)
        organization.destroySelf()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_person_delete(self, args):
        person = self.validate_person(args.gid)
        person.destroySelf()

    tdb_delete_personal_key_value_secure_parser = cmd2.Cmd2ArgumentParser(
        add_help=False
    )
    tdb_delete_personal_key_value_secure_parser.add_argument(
        "person_gid",
        help="person's gID",
    )
    tdb_delete_personal_key_value_secure_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(tdb_delete_personal_key_value_secure_parser)
    def do_tdb_personal_key_value_secure_delete(self, args):
        person = self.validate_person(args.person_gid)
        key_value = person.getPersonalKeyValueSecureByKey(args.key)
        if key_value:
            key_value.destroySelf()

    @cmd2.with_argparser(connect_parser)
    def do_tdb_address_disconnect(self, args):
        address = self.validate_address(args.gid)
        entity = self.validate_entity(args.entity_gid)
        entity.removeAddress(address)

    @cmd2.with_argparser(connect_parser)
    def do_tdb_bank_account_disconnect(self, args):
        bank_account = self.validate_bank_account(args.gid)
        entity = self.validate_entity(args.entity_gid)
        entity.removeBankAccount(bank_account)

    @cmd2.with_argparser(connect_parser)
    def do_tdb_debit_card_disconnect(self, args):
        debit_card = self.validate_debit_card(args.gid)
        entity = self.validate_entity(args.entity_gid)
        entity.removeDebitCard(debit_card)

    @cmd2.with_argparser(gid_parser)
    def do_tdb_address_edit(self, args):
        readline.set_auto_history(False)
        address = self.validate_address(args.gid)
        test_db.AddressView(address).edit()
        readline.set_auto_history(True)

    @cmd2.with_argparser(gid_parser)
    def do_tdb_bank_account_edit(self, args):
        readline.set_auto_history(False)
        bank_account = self.validate_bank_account(args.gid)
        test_db.BankAccountView(bank_account).edit()
        readline.set_auto_history(True)

    @cmd2.with_argparser(gid_parser)
    def do_tdb_debit_card_edit(self, args):
        readline.set_auto_history(False)
        debit_card = self.validate_debit_card(args.gid)
        test_db.DebitCardView(debit_card).edit()
        readline.set_auto_history(True)

    @cmd2.with_argparser(gid_parser)
    def do_tdb_job_edit(self, args):
        readline.set_auto_history(False)
        job = self.validate_job(args.gid)
        test_db.JobView(job).edit()
        readline.set_auto_history(True)

    @cmd2.with_argparser(key_parser)
    def do_tdb_key_value_edit(self, args):
        readline.set_auto_history(False)
        if args.key in test_db.RESTRICTED_KEYS:
            self._cmd.perror(
                f"error: key '{args.key}' is restricted and cannot be edited"
            )

        key_value = self.validate_key(args.key)
        test_db.KeyValueView(key_value).edit()
        readline.set_auto_history(True)

    @cmd2.with_argparser(gid_parser)
    def do_tdb_organization_edit(self, args):
        readline.set_auto_history(False)
        organization = self.validate_orgnization(args.gid)
        test_db.OrganizationView(organization).edit()
        readline.set_auto_history(True)

    @cmd2.with_argparser(gid_parser)
    def do_tdb_person_edit(self, args):
        readline.set_auto_history(False)
        person = self.validate_person(args.gid)
        test_db.PersonView(person).edit()
        readline.set_auto_history(True)

    def do_tdb_address_list(self, args):
        test_db.AddressView.list()

    def do_tdb_bank_account_list(self, args):
        test_db.BankAccountView.list()

    def do_tdb_debit_card_list(self, args):
        test_db.DebitCardView.list()

    def do_tdb_job_list(self, args):
        test_db.JobView.list()

    def do_tdb_key_value_list(self, args):
        test_db.KeyValueView.list()

    def do_tdb_organization_list(self, args):
        test_db.OrganizationView.list()

    def do_tdb_person_list(self, args):
        test_db.PersonView.list()

    def do_tdb_personal_key_value_secure_list(self, args):
        test_db.PersonalKeyValueSecureView.list()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_address_view(self, args):
        address = self.validate_address(args.gid)
        test_db.AddressView(address).viewDetails()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_bank_account_view(self, args):
        bank_account = self.validate_bank_account(args.gid)
        test_db.BankAccountView(bank_account).viewDetails()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_debit_card_view(self, args):
        debit_card = self.validate_debit_card(args.gid)
        test_db.DebitCardView(debit_card).viewDetails()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_job_view(self, args):
        job = self.validate_job(args.gid)
        test_db.JobView(job).viewDetails()

    @cmd2.with_argparser(key_parser)
    def do_tdb_key_value_view(self, args):
        key_value = self.validate_key(args.key)
        test_db.KeyValueView(key_value).viewDetails()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_organization_view(self, args):
        organization = self.validate_orgnization(args.gid)
        test_db.OrganizationView(organization).viewDetails()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_person_view(self, args):
        person = self.validate_person(args.gid)
        test_db.PersonView(person).viewDetails()

    tdb_personal_key_value_secure_view_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    tdb_personal_key_value_secure_view_parser.add_argument(
        "person_gid",
        help="person's gID",
    )
    tdb_personal_key_value_secure_view_parser.add_argument(
        "key",
        help="key",
    )

    @cmd2.with_argparser(tdb_personal_key_value_secure_view_parser)
    def do_tdb_personal_key_value_secure_view(self, args):
        person = self.validate_person(args.person_gid)
        key_value = person.getPersonalKeyValueSecureByKey(args.key)
        if key_value:
            test_db.PersonalKeyValueSecureView(key_value).viewDetails()
