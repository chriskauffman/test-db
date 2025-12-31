import logging

import test_db


logger = logging.getLogger(__name__)


class _TyperOptions:
    @property
    def interactive(self):
        return test_db.typer.interactive
