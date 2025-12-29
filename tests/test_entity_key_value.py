from test_db._entity import Entity
from test_db import EntityKeyValue


def test_init(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)

    assert EntityKeyValue(
        itemKey="testClientId", entity=test_entity, connection=temporary_db.connection
    )


def test_create_key_value(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)

    test_token = EntityKeyValue(
        itemKey="test_create_key",
        entity=test_entity,
        itemValue="test_value",
        connection=temporary_db.connection,
    )

    assert isinstance(test_token.itemValue, str)
    assert test_token.itemValue == "test_value"


def test_update_key_value(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)

    test_token = EntityKeyValue(
        itemKey="test_update_key",
        entity=test_entity,
        connection=temporary_db.connection,
    )

    test_token.itemValue = "xyz123"

    assert isinstance(test_token.itemValue, str)
    assert test_token.itemValue == "xyz123"

    test_token.itemValue = "xyz888"

    assert isinstance(test_token.itemValue, str)
    assert test_token.itemValue == "xyz888"


def test_cascade_delete(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)
    test_entity_id = test_entity.id
    test_key_count = EntityKeyValue.select(connection=temporary_db.connection).count()

    for item in range(5):
        EntityKeyValue(
            itemKey=f"cascadeTest{item}",
            entity=test_entity,
            connection=temporary_db.connection,
        )

    assert (
        EntityKeyValue.select(connection=temporary_db.connection).count()
        == test_key_count + 5
    )
    assert (
        EntityKeyValue.select(
            EntityKeyValue.q.entity == test_entity_id,
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
            EntityKeyValue.q.entity == test_entity_id,
            connection=temporary_db.connection,
        ).count()
        == 0
    )
