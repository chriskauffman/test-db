from test_db._entity import Entity


def test_init(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)
    assert test_entity
