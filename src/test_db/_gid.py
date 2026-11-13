import logging
from typing import Any

from typeid import TypeID
from typeid.errors import (
    InvalidTypeIDStringException,
    PrefixValidationException,
    SuffixValidationException,
)

logger = logging.getLogger(__name__)


class GIDMixin:
    """Shared gID setter for SQLObject models."""

    def _set_gID(self: Any, value):
        if value:
            if validGID(value, self._gIDPrefix):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(TypeID(self._gIDPrefix))


def validGID(gID: str | TypeID, gIDPrefix: str | None = None) -> bool:
    """Determines if a string is a valid global ID

    Args:
        gID (str | TypeID):
        gIDPrefix (str | None): when provided, the gID must match this prefix

    Returns:
        bool: True when valid
    """
    if isinstance(gID, str):
        try:
            globalTypeID = TypeID.from_string(gID)
        except InvalidTypeIDStringException:
            return False
        except PrefixValidationException:
            return False
        except SuffixValidationException:
            return False
    elif isinstance(gID, TypeID):
        globalTypeID = gID
    else:
        return False
    if gIDPrefix:
        return globalTypeID.prefix == gIDPrefix
    return True
