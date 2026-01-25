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
class JobCommandSet(BaseCommandSet):
    tdb_job_add_parser = cmd2.Cmd2ArgumentParser()
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
            organization = self.validate_organization(args.organization_gid)
        if args.person_gid:
            person = self.validate_person(args.person_gid)
        new_job = test_db.Job(organization=organization, person=person)
        if self._cmd.command_interaction:
            test_db.JobView(new_job).edit()
        readline.set_auto_history(True)

    gid_parser = cmd2.Cmd2ArgumentParser()
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
