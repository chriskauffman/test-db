import sys

import test_db
from test_db._lookup import NotFoundError, get_key_value, lookup


def validate(fn, *args):
    try:
        return lookup(fn, *args)
    except NotFoundError as exc:
        sys.stderr.write(f"error: {exc!s}\n")
        sys.exit(1)


def validate_key_value(key_values, key: str):
    return validate(get_key_value, key_values, key)


def validate_job(gid: str):
    return validate(test_db.Job.byGID, gid)


def validate_organization(gid: str):
    return validate(test_db.Organization.byGID, gid)


def validate_person(gid: str):
    return validate(test_db.Person.byGID, gid)
