import logging

from sqlobject import JSONCol, StringCol  # type: ignore

from test_db._base_sqlobject import BaseSQLObject


logger = logging.getLogger(__name__)


class KeyJson(BaseSQLObject):
    """KeyJson SQLObject

    Attributes:
        key (StringCol):
        value (JSONCol):
    """

    key: StringCol = StringCol(alternateID=True, unique=True)
    value: JSONCol = JSONCol(default=None)
