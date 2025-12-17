from test_db._entity import Entity
from test_db import EntityKeyValue


def test_init(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)

    assert EntityKeyValue(
        key="testClientId", entity=test_entity, connection=temporary_db.connection
    )


def test_init_set_token(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)

    test_token = EntityKeyValue(
        key="testClientId",
        entity=test_entity,
        value="",
        connection=temporary_db.connection,
    )

    assert isinstance(test_token.value, str)
    assert test_token.value == ""


def test_set_token(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)

    test_token = EntityKeyValue(
        key="testClientId", entity=test_entity, connection=temporary_db.connection
    )

    test_token.value = "xyz123"

    assert isinstance(test_token.value, str)
    assert test_token.value == "xyz123"

    test_token.value = "xyz888"

    assert isinstance(test_token.value, str)
    assert test_token.value == "xyz888"


def test_cascade_delete(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)
    test_person_id = test_entity.id
    test_key_count = EntityKeyValue.select(connection=temporary_db.connection).count()

    for item in range(5):
        EntityKeyValue(
            key=f"cascadeTest{item}",
            entity=test_entity,
            connection=temporary_db.connection,
        )

    assert (
        EntityKeyValue.select(connection=temporary_db.connection).count()
        == test_key_count + 5
    )
    assert (
        EntityKeyValue.select(
            EntityKeyValue.q.entity == test_person_id,
            connection=temporary_db.connection,
        ).count()
        == 5
    )

    test_entity.destroySelf()
    assert (
        EntityKeyValue.select(connection=temporary_db.connection).count()
        == test_key_count
    )
    assert (
        EntityKeyValue.select(
            EntityKeyValue.q.entity == test_person_id,
            connection=temporary_db.connection,
        ).count()
        == 0
    )
