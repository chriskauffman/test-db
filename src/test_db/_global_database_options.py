import logging

import test_db

logger = logging.getLogger(__name__)


class _GlobalDatabaseOptions:
    @property
    def autoCreateDependents(self) -> bool:
        return test_db.autoCreateDependents

    @property
    def databaseEncryptionKey(self) -> str | None:
        return test_db.databaseEncryptionKey

    @property
    def fernetIterations(self) -> int:
        return test_db.fernetIterations
