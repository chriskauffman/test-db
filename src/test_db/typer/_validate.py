import sys

from formencode.validators import Invalid  # type: ignore
from sqlobject import SQLObjectNotFound  # type: ignore

import test_db


def validate_entity(gid: str):
    try:
        return test_db.Person.byGID(gid)
    except Invalid as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)
    except SQLObjectNotFound:
        try:
            return test_db.Organization.byGID(gid)
        except SQLObjectNotFound:
            sys.stderr.write("error: person or organization not found")
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
