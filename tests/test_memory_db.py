import test_db


def test_memory_db():
    test_db.autoCreateDependents = True
    test_db.databaseEncryptionKey = "a test encryption key"
    db = test_db.DatabaseController("sqlite:/:memory:")

    assert db.validSchema
    assert test_db.IN_MEMORY_DB_FILE == "sqlite:/:memory:"
