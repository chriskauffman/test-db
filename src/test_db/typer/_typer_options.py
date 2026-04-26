import logging

from test_db import typer as tdb_typer


logger = logging.getLogger(__name__)


class _TyperOptions:
    @property
    def interactive(self):
        return tdb_typer.interactive
