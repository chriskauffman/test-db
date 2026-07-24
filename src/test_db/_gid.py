import logging

from typeid import TypeID
from typeid.errors import (
    InvalidTypeIDStringException,
    PrefixValidationException,
    SuffixValidationException,
)

logger = logging.getLogger(__name__)


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
    if isinstance(gID, TypeID):
        globalTypeID = gID
    else:
        return False
    if gIDPrefix:
        return globalTypeID.prefix == gIDPrefix
    return True
