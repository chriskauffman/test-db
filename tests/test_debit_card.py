from test_db._debit_card import DebitCard


def test_debit_card(temporary_db):
    test_debit_card = DebitCard(connection=temporary_db.connection)

    assert isinstance(test_debit_card, DebitCard)
    assert isinstance(test_debit_card.cardNumber, str)
    assert isinstance(int(test_debit_card.cardNumber), int)
    assert isinstance(test_debit_card.cvv, str)
    assert isinstance(int(test_debit_card.cvv), int)
