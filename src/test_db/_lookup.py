from cryptography.fernet import InvalidToken
from formencode.validators import Invalid
from sqlobject import SQLObjectNotFound


class NotFoundError(Exception):
    """Raised by lookup() when a row cannot be found or read."""


def lookup(fn, *args):
    """Call a row getter, raising NotFoundError for any not-found/invalid/undecryptable result."""
    try:
        return fn(*args)
    except (Invalid, SQLObjectNotFound) as exc:
        raise NotFoundError(str(exc)) from exc
    except InvalidToken as exc:
        raise NotFoundError(
            "Unable to decrypt - check database encryption key"
        ) from exc


def get_key_value(key_values, key: str):
    try:
        return key_values.filter(key_values.sourceClass.q.key == key).getOne()
    except SQLObjectNotFound as exc:
        raise NotFoundError(f"key {key!r} does not exist") from exc
