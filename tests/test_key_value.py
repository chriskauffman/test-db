import uuid
from test_db._key_value import KeyValue


def test_key_value(temporary_db):
    test_key = str(uuid.uuid4())
    test_key_value = KeyValue(
        itemKey=test_key,
        itemValue="test_value",
        connection=temporary_db.connection,
    )

    assert isinstance(test_key_value, KeyValue)
    assert test_key_value.itemKey == test_key
    assert test_key_value.itemValue == "test_value"
