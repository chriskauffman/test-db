import logging

from cmd2 import CommandSet, with_default_category

from sqlobject import SQLObjectNotFound  # type: ignore

from formencode.validators import Invalid  # type: ignore

import test_db

logger = logging.getLogger(__name__)


@with_default_category("Database")
class BaseCommandSet(CommandSet):
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

    def validate_organization(self, gid: str):
        try:
            return test_db.Organization.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")

    def validate_person(self, gid: str):
        try:
            return test_db.Person.byGID(gid)
        except (Invalid, SQLObjectNotFound) as exc:
            self._cmd.perror(f"error: {str(exc)}")
