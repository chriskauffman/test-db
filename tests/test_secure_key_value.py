from test_db._person import Person
from test_db._person_secure_key_value import PersonSecureKeyValue


def secure_key_value_validation(test_key_value, test_key, test_value):
    assert test_key_value.itemKey == test_key
    assert test_key_value.itemValue == test_value

    test_key_value.itemValue = "updated_value"
    assert isinstance(test_key_value.itemValue, str)
    assert test_key_value.itemValue == "updated_value"

    test_key_value.itemValue = {"new_secret_data": "newTestSecretData"}
    assert isinstance(test_key_value.itemValue, dict)
    assert test_key_value.itemValue["new_secret_data"] == "newTestSecretData"


def test_person_secure_key_value(temporary_db):
    test_person = Person(connection=temporary_db.connection)
    test_key_value = PersonSecureKeyValue(
        person=test_person,
        itemKey="test_person_key_value",
        itemValue="test_value",
        connection=temporary_db.connection,
    )

    assert isinstance(test_key_value, PersonSecureKeyValue)
    secure_key_value_validation(test_key_value, "test_person_key_value", "test_value")
