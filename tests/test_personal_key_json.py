from test_db import Person, PersonalKeyJson


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
