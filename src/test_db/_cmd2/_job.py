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


@with_default_category("Database")
class JobCommandSet(BaseCommandSet):
    def validate_job(self, gid: str):
        try:
            return test_db.Job.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

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

    gid_parser = cmd2.Cmd2ArgumentParser(add_help=False)
    gid_parser.add_argument(
        "gid",
        help="object's gID",
    )

    @cmd2.with_argparser(gid_parser)
    def do_tdb_job_delete(self, args):
        job = self.validate_job(args.gid)
        job.destroySelf()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_job_edit(self, args):
        readline.set_auto_history(False)
        job = self.validate_job(args.gid)
        test_db.JobView(job).edit()
        readline.set_auto_history(True)

    def do_tdb_job_list(self, args):
        test_db.JobView.list()

    @cmd2.with_argparser(gid_parser)
    def do_tdb_job_view(self, args):
        job = self.validate_job(args.gid)
        test_db.JobView(job).viewDetails()
