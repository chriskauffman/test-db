import datetime

from test_db._key_value_secure import KeyValueSecure


def test_init(temporary_db):
    assert KeyValueSecure(key="testkey", connection=temporary_db.connection)


def test_set_various_values(temporary_db):
    test_token = KeyValueSecure(
        key="test_set_various_values",
        value={},
        connection=temporary_db.connection,
    )

    assert isinstance(test_token.value, dict)
    assert test_token.value == {}

    test_token.value = "abc123"
    assert test_token.value == "abc123"

    test_token.value = 1234
    assert test_token.value == 1234

    test_token.value = 1234.11
    assert test_token.value == 1234.11

    test_token.value = datetime.datetime(2020, 1, 1, 12, 0, 0)
    assert test_token.value == datetime.datetime(2020, 1, 1, 12, 0, 0)


def test_set_and_retrieve_value(temporary_db):
    test_token = KeyValueSecure(
        key="test_set_and_retrieve_value",
        value={"abc": 123},
        connection=temporary_db.connection,
    )

    assert isinstance(test_token.value, dict)
    assert test_token.value == {"abc": 123}

    test_token = KeyValueSecure.byKey(
        "test_set_and_retrieve_value", connection=temporary_db.connection
    )

    assert isinstance(test_token.value, dict)
    assert test_token.value == {"abc": 123}


def test_set_value_as_token(temporary_db):
    test_token = KeyValueSecure(
        key="test_set_value_as_token", connection=temporary_db.connection
    )

    test_token.value = {"access_token": "abc123", "refresh_token": "xyz123"}

    assert isinstance(test_token.value, dict)
    assert test_token.value["access_token"] == "abc123"
    assert test_token.value["refresh_token"] == "xyz123"

    test_token.value = {"access_token": "abc888", "refresh_token": "xyz888"}

    assert isinstance(test_token.value, dict)
    assert test_token.value["access_token"] == "abc888"
    assert test_token.value["refresh_token"] == "xyz888"
