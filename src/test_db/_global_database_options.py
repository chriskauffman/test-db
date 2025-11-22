import test_db

from typing_extensions import Optional


class _GlobalDatabaseOptions:
    @property
    def autoCreateDependents(self) -> bool:
        return test_db.autoCreateDependents

    @property
    def databaseEncryptionKey(self) -> Optional[str]:
        return test_db.databaseEncryptionKey

    @property
    def fernetIterations(self) -> int:
        return test_db.fernetIterations
