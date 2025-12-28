from test_db._entity import Entity

import test_db
from test_db._entity_key_value import EntityKeyValue
from test_db._entity_secure_key_value import EntitySecureKeyValue


def test_init(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)
    assert test_entity


def test_getKeyValueByKey(temporary_db):
    test_person = Entity(connection=temporary_db.connection)
    test_db.databaseEncryptionKey = "a really good key"

    test_oauth2_token = test_person.getKeyValueByKey("testClientId1")

    assert isinstance(test_oauth2_token, EntityKeyValue)
    assert test_oauth2_token.itemKey == "testClientId1"

    test_oauth2_token = test_person.getKeyValueByKey(
        "testClientId2", itemValue="testAccessToken"
    )

    assert test_oauth2_token.itemValue == "testAccessToken"


def test_getSecureKeyValueByKey(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)
    test_db.databaseEncryptionKey = "a really good key"

    test_secure_kv = test_entity.getSecureKeyValueByKey("testKey1")

    assert isinstance(test_secure_kv, EntitySecureKeyValue)
    assert test_secure_kv.itemKey == "testKey1"

    test_secure_kv = test_entity.getSecureKeyValueByKey(
        "testKey2", itemValue={"secret_data": "testSecretData"}
    )

    assert test_secure_kv.itemValue == {"secret_data": "testSecretData"}
