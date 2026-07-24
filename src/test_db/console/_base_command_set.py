import logging

from cmd2 import CommandSet
from formencode.validators import Invalid
from sqlobject import SQLObjectNotFound

import test_db

logger = logging.getLogger(__name__)


class BaseCommandSet(CommandSet):
    DEFAULT_CATEGORY = "Database"

    def validate_job(self, gid: str):
        try:
            return test_db.Job.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {exc!s}")

    def validate_organization(self, gid: str):
        try:
            return test_db.Organization.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {exc!s}")

    def validate_person(self, gid: str):
        try:
            return test_db.Person.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {exc!s}")
