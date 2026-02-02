from test_db._person import Person
from test_db._person_debit_card import PersonDebitCard


def debit_card_validation(test_debit_card):
    assert isinstance(test_debit_card.cardNumber, str)
    assert isinstance(int(test_debit_card.cardNumber), int)
    assert isinstance(test_debit_card.cvv, str)
    assert isinstance(int(test_debit_card.cvv), int)


def test_debit_card(temporary_db):
    test_debit_card = PersonDebitCard(
        person=Person(connection=temporary_db.connection),
        connection=temporary_db.connection,
    )

    assert isinstance(test_debit_card, PersonDebitCard)
    debit_card_validation(test_debit_card)
