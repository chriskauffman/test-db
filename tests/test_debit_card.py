import test_db
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


def test_autoCreateDependents_person(temporary_db):
    new_person = Person(connection=temporary_db.connection)
    person_count = Person.select(connection=temporary_db.connection).count()

    test_db.autoCreateDependents = False
    test_debit_card = PersonDebitCard(
        connection=temporary_db.connection,
    )
    assert test_debit_card.person is None
    assert Person.select(connection=temporary_db.connection).count() == person_count

    test_debit_card = PersonDebitCard(
        person=new_person,
        connection=temporary_db.connection,
    )
    assert test_debit_card.person is new_person
    assert Person.select(connection=temporary_db.connection).count() == person_count

    test_db.autoCreateDependents = True
    test_debit_card = PersonDebitCard(
        connection=temporary_db.connection,
    )
    assert isinstance(test_debit_card.person, Person)
    assert Person.select(connection=temporary_db.connection).count() == person_count + 1

    test_debit_card = PersonDebitCard(
        person=new_person,
        connection=temporary_db.connection,
    )
    assert test_debit_card.person is new_person
    assert Person.select(connection=temporary_db.connection).count() == person_count + 1
