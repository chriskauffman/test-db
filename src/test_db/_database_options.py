import test_db


class _GlobalDatabaseOptions:
    @property
    def databaseEncryptionKey(self):
        return test_db.databaseEncryptionKey

    @property
    def fernetIterations(self):
        return test_db.fernetIterations
