import logging

from sqlobject import StringCol  # type: ignore

from test_db._base_sqlobject import BaseSQLObject


logger = logging.getLogger(__name__)


class KeyValue(BaseSQLObject):
    """Basic key value storage

    Designed for simple data storage needs such as database or app configuration

    Attributes:
        key (StringCol):
        value (StringCol):
    """

    key: StringCol = StringCol(alternateID=True, unique=True)
    value: StringCol = StringCol(default=None)
