from test_db._debit_card import PersonalDebitCard
from test_db._person import Person


def test_personal_debit_card(temporary_db):
    test_person = Person(connection=temporary_db.connection)
    test_personal_debit_card = PersonalDebitCard(
        name="test_personal_debit_card",
        person=test_person,
        connection=temporary_db.connection,
    )

    assert isinstance(test_personal_debit_card, PersonalDebitCard)
    assert isinstance(test_personal_debit_card.cardNumber, str)
    assert isinstance(int(test_personal_debit_card.cardNumber), int)
    assert isinstance(test_personal_debit_card.cvv, str)
    assert isinstance(int(test_personal_debit_card.cvv), int)
