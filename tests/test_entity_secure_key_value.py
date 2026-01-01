from test_db._entity import Entity
from test_db import EntitySecureKeyValue


def test_init(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)

    assert EntitySecureKeyValue(
        itemKey="testClientId", entity=test_entity, connection=temporary_db.connection
    )


def test_create_key_value(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)

    test_token = EntitySecureKeyValue(
        itemKey="testClientId",
        entity=test_entity,
        itemValue={},
        connection=temporary_db.connection,
    )

    assert isinstance(test_token.itemValue, dict)
    assert test_token.itemValue == {}


def test_update_key_value(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)

    test_token = EntitySecureKeyValue(
        itemKey="testClientId", entity=test_entity, connection=temporary_db.connection
    )

    test_token.itemValue = {"access_token": "abc123", "refresh_token": "xyz123"}

    assert isinstance(test_token.itemValue, dict)
    assert test_token.itemValue["access_token"] == "abc123"
    assert test_token.itemValue["refresh_token"] == "xyz123"

    test_token.itemValue = {"access_token": "abc888", "refresh_token": "xyz888"}

    assert isinstance(test_token.itemValue, dict)
    assert test_token.itemValue["access_token"] == "abc888"
    assert test_token.itemValue["refresh_token"] == "xyz888"


def test_cascade_delete(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)
    test_entity_id = test_entity.id
    test_key_count = EntitySecureKeyValue.select(
        connection=temporary_db.connection
    ).count()

    for item in range(5):
        EntitySecureKeyValue(
            itemKey=f"cascadeTest{item}",
            entity=test_entity,
            connection=temporary_db.connection,
        )

    assert (
        EntitySecureKeyValue.select(connection=temporary_db.connection).count()
        == test_key_count + 5
    )
    assert (
        EntitySecureKeyValue.select(
            EntitySecureKeyValue.q.entity == test_entity_id,
            connection=temporary_db.connection,
        ).count()
        == 5
    )

    test_entity.destroySelf()
    assert (
        EntitySecureKeyValue.select(connection=temporary_db.connection).count()
        == test_key_count
    )
    assert (
        EntitySecureKeyValue.select(
            EntitySecureKeyValue.q.entity == test_entity_id,
            connection=temporary_db.connection,
        ).count()
        == 0
    )
