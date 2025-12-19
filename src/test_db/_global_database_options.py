import test_db

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
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
