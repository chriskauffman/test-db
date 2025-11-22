from test_db._key_value import KeyValue


def test_key_value(temporary_db):
    test_key_value = KeyValue(
        key="test_key_value",
        value="test_value",
        connection=temporary_db.connection,
    )

    assert isinstance(test_key_value, KeyValue)
    assert test_key_value.key == "test_key_value"
    assert test_key_value.value == "test_value"
