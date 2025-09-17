from test_db._address import PersonalAddress
from test_db._person import Person


def test_personal_address(temporary_db):
    test_person = Person(connection=temporary_db.connection)
    test_personal_address = PersonalAddress(
        name="test_personal_address",
        person=test_person,
        connection=temporary_db.connection,
    )

    assert isinstance(test_personal_address, PersonalAddress)
