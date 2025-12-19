import logging

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Optional, Union

from typeid import TypeID
from typeid.errors import (
    InvalidTypeIDStringException,
    PrefixValidationException,
    SuffixValidationException,
)

logger = logging.getLogger(__name__)


def validGID(gID: Union[str, TypeID], gIDPrefix: Optional[str] = None) -> bool:
    """Determines if a string is a valid global ID

    Args:
        gID (Union[str, TypeID]):
        gIDPrefix (Optional[str]): when provided, the gID must match this prefix

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
    if gIDPrefix and globalTypeID.prefix != gIDPrefix:
        return False
    return True
