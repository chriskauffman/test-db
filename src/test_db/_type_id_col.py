import logging
from typeid import TypeID
from typeid.errors import (
    InvalidTypeIDStringException,
    PrefixValidationException,
    SuffixValidationException,
)

from typing_extensions import Optional

# from sqlobject import sqlbuilder
from sqlobject.col import Col, SOCol, SOValidator  # type: ignore
from formencode import validators  # type: ignore

logger = logging.getLogger(__name__)


class TypeIDValidator(SOValidator):
    # def getGIDPrefix(self, state):
    #     try:
    #         return self.gIDPrefix
    #     except AttributeError:
    #         return self.soCol.getGIDPrefix(state)

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

    def from_python(self, value, state):
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
    # def __init__(self, **kw):
    #     self.gIDPrefix = kw.pop("gIDPrefix", "tdb")
    #     super(SOTypeIDCol, self).__init__(**kw)

    def createValidators(self):
        return [TypeIDValidator(name=self.name)] + super(
            SOTypeIDCol, self
        ).createValidators()

    # Python TypeID documentation specifies max length of 90 characters
    def _sqlType(self):
        return "VARCHAR(90)"

    # def getGIDPrefix(self, state):
    #     if self.gIDPrefix:
    #         return self.gIDPrefix
    #     try:
    #         gIDPrefix = state.soObject.sqlmeta.gIDPrefix
    #     except AttributeError:
    #         gIDPrefix = None
    #     if gIDPrefix:
    #         return gIDPrefix
    #     try:
    #         connection = state.connection or state.soObject._connection
    #     except AttributeError:
    #         gIDPrefix = None
    #     else:
    #         gIDPrefix = getattr(connection, "gIDPrefix", None)
    #     if not gIDPrefix:
    #         raise ValueError("Invalid TypeID config, check gIDPrefix value")
    #     return gIDPrefix


class TypeIDCol(Col):
    baseClass = SOTypeIDCol
