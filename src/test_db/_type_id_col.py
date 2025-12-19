import logging

from typeid import TypeID
from typeid.errors import (
    InvalidTypeIDStringException,
    PrefixValidationException,
    SuffixValidationException,
)

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Optional

from sqlobject.col import Col, SOCol, SOValidator  # type: ignore
from formencode import validators  # type: ignore

logger = logging.getLogger(__name__)


class TypeIDValidator(SOValidator):
    def to_python(self, value, state) -> Optional[TypeID]:
        if value is None:
            return None
        if isinstance(value, str):
            return TypeID.from_string(value)
        if isinstance(value, TypeID):
            return value
        raise validators.Invalid(
            "expected string in the TypeIDCol '%s', "
            "got %s %r instead" % (self.name, type(value), value),
            value,
            state,
        )

    def from_python(self, value, state) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, str):
            try:
                TypeID.from_string(value)
                return value
            except InvalidTypeIDStringException:
                pass
            except PrefixValidationException:
                pass
            except SuffixValidationException:
                pass
            raise validators.Invalid(
                "expected str(TypeID) in the TypeIDCol '%s', "
                "got %s %r instead" % (self.name, type(value), value),
                value,
                state,
            )
        if isinstance(value, TypeID):
            return str(value)
        raise validators.Invalid(
            "expected TypeID in the TypeIDCol '%s', "
            "got %s %r instead" % (self.name, type(value), value),
            value,
            state,
        )


class SOTypeIDCol(SOCol):
    def createValidators(self):
        return [TypeIDValidator(name=self.name)] + super(
            SOTypeIDCol, self
        ).createValidators()

    # Python TypeID documentation specifies max length of 90 characters
    def _sqlType(self):
        return "VARCHAR(90)"


class TypeIDCol(Col):
    baseClass = SOTypeIDCol
