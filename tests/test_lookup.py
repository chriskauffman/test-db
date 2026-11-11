import pytest
from sqlobject import SQLObjectNotFound

from test_db._lookup import get_key_value


def test_get_key_value_reports_missing_key():
    class MissingKeyValues:
        sourceClass = type("Source", (), {"q": type("Query", (), {"key": "key"})})

        def filter(self, condition):
            return self

        def getOne(self):
            raise SQLObjectNotFound

    with pytest.raises(SQLObjectNotFound, match="key 'missing' does not exist"):
        get_key_value(MissingKeyValues(), "missing")
