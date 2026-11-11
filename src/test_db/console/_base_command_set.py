import logging

from cmd2 import CommandSet
from formencode.validators import Invalid
from sqlobject import SQLObjectNotFound

import test_db
from test_db._lookup import get_key_value

logger = logging.getLogger(__name__)


class BaseCommandSet(CommandSet):
    DEFAULT_CATEGORY = "Database"

    def validate(self, fn, *args):
        try:
            return fn(*args)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {exc!s}")
            raise

    def validate_key_value(self, key_values, key: str):
        return self.validate(get_key_value, key_values, key)

    def validate_job(self, gid: str):
        return self.validate(test_db.Job.byGID, gid)

    def validate_organization(self, gid: str):
        return self.validate(test_db.Organization.byGID, gid)

    def validate_person(self, gid: str):
        return self.validate(test_db.Person.byGID, gid)
