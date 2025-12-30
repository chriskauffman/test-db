"""test_db maintenance script"""

from importlib.metadata import version as get_version
import logging
import logging.handlers
import pathlib
import sys

import cmd2

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Optional

import test_db
from test_db._cli_settings import DEFAULT_CONFIG_PATH, Settings
from test_db.cmd2 import (
    AddressCommandSet,
    BankAccountCommandSet,
    DebitCardCommandSet,
    EntityKeyValueCommandSet,
    EntitySecureKeyValueCommandSet,
    JobCommandSet,
    KeyValueCommandSet,
    OrgnizationCommandSet,
    PersonCommandSet,
)

logger = logging.getLogger(__name__)


class Console(cmd2.Cmd):
    """A simple cmd application."""

    # pylint: disable=unused-argument,too-many-public-methods,too-many-instance-attributes

    intro = "Welcome to the ODP simulator.  Type help or ? to list commands.\n"
    _cmd_history_file = pathlib.Path(DEFAULT_CONFIG_PATH, "tdb_cmd2_history")
    _prompt = "tdb"

    def __init__(self, settings: Settings, **kwargs) -> None:
        super().__init__(persistent_history_file=str(self._cmd_history_file), **kwargs)

        self._settings = settings

        self.command_interaction = True
        self.add_settable(
            cmd2.Settable(
                "command_interaction",
                bool,
                "Require user to interact and provide confirmation in certain commands",
                self,
            )
        )

        self.db_connection_uri = self._settings.db_connection_uri
        self.add_settable(
            cmd2.Settable(
                "db_connection_uri",
                str,
                "Database connection URI",
                self,
                onchange_cb=self._onchange_db_connection_uri,
            )
        )

        self._db: Optional[test_db.DatabaseController] = None

        self._reset_db()
        self._set_prompt()

    def _onchange_db_connection_uri(self, _param_name, _old, new) -> None:
        """Execute when db_connection_uri setting changed"""
        logger.debug("_param_name=%s, _old=%s, new=%s", _param_name, _old, new)
        self._reset_db()
        self._set_prompt()

    def _reset_db(self):
        logger.debug("resetting db with db_connection_uri=%s", self.db_connection_uri)
        if self._db and self._db.connection:
            self._db.close()
        try:
            self._db = test_db.DatabaseController(
                self.db_connection_uri, defaultConnection=True
            )
        except ValueError:
            self._db = None

    def _set_prompt(self):
        """Set Prompt"""
        self.prompt = f"{self._prompt}: "

    def do_version(self, args):
        print(get_version(__package__))


def main() -> None:
    settings = Settings()

    if not settings.log_path.is_dir():
        sys.stderr.write(
            f"error: incorrect log_path {settings.log_path}, must be existing directory"
        )
        sys.exit(1)

    logging_file_handler = logging.handlers.RotatingFileHandler(
        pathlib.Path(settings.log_path, "tdb_console.log"),
        encoding="utf-8",
        maxBytes=2 * 1024 * 1024,  # 2 MB
        backupCount=10,
    )
    logging_file_handler.setLevel(settings.log_level_file)
    logging_file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(module)s - %(levelname)s - %(name)s - %(message)s"
        )
    )
    logger.addHandler(logging_file_handler)

    logging_stream_handler = logging.StreamHandler(sys.stdout)
    logging_stream_handler.setLevel(settings.log_level_screen)
    logging_stream_handler.setFormatter(
        logging.Formatter("%(levelname)s - %(message)s")
    )
    logger.addHandler(logging_stream_handler)
    logger.debug("settings=%s", settings)

    test_db.databaseEncryptionKey = settings.database_encryption_key.get_secret_value()
    test_db.fernetIterations = settings.database_fernet_iterations

    console = Console(
        settings,
        command_sets=[
            AddressCommandSet(),
            BankAccountCommandSet(),
            DebitCardCommandSet(),
            EntityKeyValueCommandSet(),
            EntitySecureKeyValueCommandSet(),
            JobCommandSet(),
            KeyValueCommandSet(),
            OrgnizationCommandSet(),
            PersonCommandSet(),
        ],
    )
    sys.exit(console.cmdloop())


if __name__ == "__main__":
    main()
