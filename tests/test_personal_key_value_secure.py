from test_db import Person, PersonalKeyValueSecure


def test_init(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    assert PersonalKeyValueSecure(
        key="testClientId", person=test_person, connection=temporary_db.connection
    )


def test_init_set_token(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    test_token = PersonalKeyValueSecure(
        key="testClientId",
        person=test_person,
        value={},
        connection=temporary_db.connection,
    )

    assert isinstance(test_token.value, dict)
    assert test_token.value == {}


def test_set_token(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    test_token = PersonalKeyValueSecure(
        key="testClientId", person=test_person, connection=temporary_db.connection
    )

    test_token.value = {"access_token": "abc123", "refresh_token": "xyz123"}

    assert isinstance(test_token.value, dict)
    assert test_token.value["access_token"] == "abc123"
    assert test_token.value["refresh_token"] == "xyz123"

    test_token.value = {"access_token": "abc888", "refresh_token": "xyz888"}

    assert isinstance(test_token.value, dict)
    assert test_token.value["access_token"] == "abc888"
    assert test_token.value["refresh_token"] == "xyz888"
