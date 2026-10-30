import logging
import sys

from formencode.validators import Invalid
from sqlobject import SQLObjectNotFound

import test_db

logger = logging.getLogger(__name__)


def validate_key_value(key_values, key: str):
    try:
        return key_values.filter(key_values.sourceClass.q.key == key).getOne()
    except SQLObjectNotFound:
        sys.stderr.write(f"error: key {key!r} does not exist\n")
        sys.exit(1)


def validate_job(gid: str):
    try:
        return test_db.Job.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {exc!s}")
        sys.exit(1)


def validate_organization(gid: str):
    try:
        return test_db.Organization.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {exc!s}")
        sys.exit(1)


def validate_person(gid: str):
    try:
        return test_db.Person.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {exc!s}")
        sys.exit(1)
