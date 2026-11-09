import logging

import test_db

logger = logging.getLogger(__name__)


class _GlobalDatabaseOptions:
    @property
    def autoCreateDependents(self) -> bool:
        return test_db.autoCreateDependents
