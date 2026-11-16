import logging

import test_db

logger = logging.getLogger(__name__)


class _GlobalDatabaseOptions:
    def __init__(self) -> None:
        self.bulkAdd = False
        self.bulkUniqueValues: dict = {}

    @property
    def autoCreateDependents(self) -> bool:
        return test_db.autoCreateDependents
