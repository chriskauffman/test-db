from test_db._oauth2_token import PersonalOAuth2Token
from test_db._person import Person


def test_init(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    assert PersonalOAuth2Token(
        clientID="testClientId", person=test_person, connection=temporary_db.connection
    )


def test_init_set_token(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    test_token = PersonalOAuth2Token(
        clientID="testClientId",
        person=test_person,
        token={},
        connection=temporary_db.connection,
    )

    assert isinstance(test_token.token, dict)
    assert test_token.token == {}


def test_set_token(temporary_db):
    test_person = Person(connection=temporary_db.connection)

    test_token = PersonalOAuth2Token(
        clientID="testClientId", person=test_person, connection=temporary_db.connection
    )

    test_token.token = {"access_token": "abc123", "refresh_token": "xyz123"}

    assert isinstance(test_token.token, dict)
    assert test_token.token["access_token"] == "abc123"
    assert test_token.token["refresh_token"] == "xyz123"

    test_token.token = {"access_token": "abc888", "refresh_token": "xyz888"}

    assert isinstance(test_token.token, dict)
    assert test_token.token["access_token"] == "abc888"
    assert test_token.token["refresh_token"] == "xyz888"
