import logging

from test_db import cli


logger = logging.getLogger(__name__)


class _TyperOptions:
    @property
    def interactive(self):
        return cli.interactive
