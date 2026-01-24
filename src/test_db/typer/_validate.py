import logging
import sys

from formencode.validators import Invalid  # type: ignore
from sqlobject import SQLObjectNotFound  # type: ignore

import test_db

logger = logging.getLogger(__name__)


def validate_job(gid: str):
    try:
        return test_db.Job.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


def validate_organization(gid: str):
    try:
        return test_db.Organization.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


def validate_person(gid: str):
    try:
        return test_db.Person.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)
