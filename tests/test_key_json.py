from test_db._key_json import KeyJson


def test_key_json(temporary_db):
    test_key_json = KeyJson(
        key="test_key_json",
        connection=temporary_db.connection,
    )

    assert isinstance(test_key_json, KeyJson)
