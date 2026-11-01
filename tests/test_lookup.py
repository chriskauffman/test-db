import pytest
from cryptography.fernet import InvalidToken
from formencode.validators import Invalid
from sqlobject import SQLObjectNotFound

from test_db._lookup import NotFoundError, lookup


def _raise(exc):
    def fn():
        raise exc

    return fn


@pytest.mark.parametrize(
    "exc", [Invalid("bad", None, None), SQLObjectNotFound("missing"), InvalidToken()]
)
def test_lookup_converts_to_not_found(exc):
    with pytest.raises(NotFoundError):
        lookup(_raise(exc))


def test_lookup_does_not_hide_bugs():
    with pytest.raises(KeyError):
        lookup(_raise(KeyError("bug")))


def test_lookup_returns_value():
    assert lookup(lambda x: x, 1) == 1
