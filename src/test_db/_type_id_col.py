import logging

from formencode import validators
from sqlobject.col import Col, SOCol, SOValidator
from typeid import TypeID
from typeid.errors import (
    InvalidTypeIDStringException,
    PrefixValidationException,
    SuffixValidationException,
)

logger = logging.getLogger(__name__)


class TypeIDValidator(SOValidator):
    def to_python(self, value, state) -> TypeID | None:
        if value is None:
            return None
        if isinstance(value, str):
            return TypeID.from_string(value)
        if isinstance(value, TypeID):
            return value
        raise validators.Invalid(
            f"expected string in the TypeIDCol '{self.name}', "
            f"got {type(value)} {value} instead",
            value,
            state,
        )

    def from_python(self, value, state) -> str | None:
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
                f"expected str(TypeID) in the TypeIDCol '{self.name}', "
                f"got {type(value)} {value} instead",
                value,
                state,
            )
        if isinstance(value, TypeID):
            return str(value)
        raise validators.Invalid(
            f"expected TypeID in the TypeIDCol '{self.name}', "
            f"got {type(value)} {value} instead",
            value,
            state,
        )


class SOTypeIDCol(SOCol):
    def createValidators(self):
        return [TypeIDValidator(name=self.name)] + super().createValidators()

    # Python TypeID documentation specifies max length of 90 characters
    def _sqlType(self):
        return "VARCHAR(90)"


class TypeIDCol(Col):
    baseClass = SOTypeIDCol
