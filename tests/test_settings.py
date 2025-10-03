from test_db._settings import KeyValue, KeyJson, PersonalKeyValue, PersonalKeyJson
from test_db._person import Person


def test_key_value(temporary_db):
    test_key_value = KeyValue(
        key="test_key_value",
        connection=temporary_db.connection,
    )

    assert isinstance(test_key_value, KeyValue)


def test_key_json(temporary_db):
    test_key_json = KeyJson(
        key="test_key_json",
        connection=temporary_db.connection,
    )

    assert isinstance(test_key_json, KeyJson)


def test_personal_key_value(temporary_db):
    test_person = Person(connection=temporary_db.connection)
    test_personal_key_value = PersonalKeyValue(
        key="test_personal_key_value",
        person=test_person,
        connection=temporary_db.connection,
    )

    assert isinstance(test_personal_key_value, PersonalKeyValue)


def test_duplicate_keys(temporary_db):
    test_person_1 = Person(connection=temporary_db.connection)
    test_person_2 = Person(connection=temporary_db.connection)

    key_1 = PersonalKeyValue(
        key="duplicate_key",
        value="value_for_person_1",
        person=test_person_1,
        connection=temporary_db.connection,
    )

    key_2 = PersonalKeyValue(
        key="duplicate_key",
        value="value_for_person_2",
        person=test_person_2,
        connection=temporary_db.connection,
    )

    assert key_1.value != key_2.value


def test_personal_key_json(temporary_db):
    test_person = Person(connection=temporary_db.connection)
    test_personal_key_json = PersonalKeyJson(
        key="test_personal_key_json",
        person=test_person,
        connection=temporary_db.connection,
    )

    assert isinstance(test_personal_key_json, PersonalKeyJson)


def test_duplicate_json_keys(temporary_db):
    test_person_1 = Person(connection=temporary_db.connection)
    test_person_2 = Person(connection=temporary_db.connection)

    key_1 = PersonalKeyJson(
        key="duplicate_key",
        value={"test": "value_for_person_1"},
        person=test_person_1,
        connection=temporary_db.connection,
    )

    key_2 = PersonalKeyJson(
        key="duplicate_key",
        value={"test": "value_for_person_2"},
        person=test_person_2,
        connection=temporary_db.connection,
    )

    assert key_1.value["test"] != key_2.value["test"]
