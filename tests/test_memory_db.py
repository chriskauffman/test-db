import test_db


def test_memory_db(db_encryption_key):
    test_db.autoCreateDependents = True
    test_db.databaseEncryptionKey = db_encryption_key
    db = test_db.DatabaseController("sqlite:/:memory:")

    assert db.validSchema
    assert test_db.IN_MEMORY_DB_FILE == "sqlite:/:memory:"
