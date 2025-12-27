"""test_db maintenance script"""

from importlib.metadata import version as get_version
import logging
import os
import pathlib
import sys

import cmd2

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Optional

import test_db
from test_db._backup_file import backupFile
from test_db._cli_settings import DEFAULT_CONFIG_PATH, DEFAULT_DB_PATH, Settings
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
    logger = logging.getLogger(__name__)
    _cmd_history_file = pathlib.Path(DEFAULT_CONFIG_PATH, "odp_cmd2_history")
    _prompt = "tdb"

    def __init__(self, settings: Settings, log_file: pathlib.Path, **kwargs) -> None:
        super().__init__(persistent_history_file=str(self._cmd_history_file), **kwargs)

        self._settings = settings
        self._log_file = log_file

        self.command_interaction = True
        self.add_settable(
            cmd2.Settable(
                "command_interaction",
                bool,
                "Require user to interact and provide confirmation in certain commands",
                self,
            )
        )

        self.db_file_path = self._settings.db_file_path or DEFAULT_DB_PATH
        self.add_settable(
            cmd2.Settable(
                "db_file_path",
                self._val_type_db_file_path,
                "Database file name",
                self,
                onchange_cb=self._onchange_db_file_path,
            )
        )

        self.db_connection_uri = (
            self._settings.db_connection_uri or f"sqlite:{self.db_file_path}"
        )
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

        # self._address_commands = AddressCommandSet()
        # self.register_command_set(self._address_commands)
        # self._database_commands = PersonCommandSet()
        # self.register_command_set(self._database_commands)

    def _onchange_db_connection_uri(self, _param_name, _old, new) -> None:
        """Execute when db_connection_uri setting changed"""
        self.logger.debug("_param_name=%s, _old=%s, new=%s", _param_name, _old, new)
        self._reset_db()
        self._set_prompt()

    def _onchange_db_file_path(self, _param_name, _old, new) -> None:
        """Execute when db_file_path setting changed"""
        self.logger.debug("_param_name=%s, _old=%s, new=%s", _param_name, _old, new)
        self.db_connection_uri = f"sqlite:{new}"
        self._reset_db()
        self._set_prompt()

    def _val_type_db_file_path(self, new: str):
        """Validate db_file_path"""
        if new != test_db.IN_MEMORY_DB_FILE:
            if not pathlib.Path(new).parent.exists():
                raise ValueError(f"db_file_path {new} invalid")
        return pathlib.Path(new)

    def _reset_db(self, create: bool = False):
        # backup_file(self.db_file_path, self._settings.backup_path)
        self.logger.debug(
            "resetting db with db_connection_uri=%s", self.db_connection_uri
        )
        if self._db is not None and self._db.connection:
            self._db.close()
        if os.path.isfile(self.db_connection_uri):
            backupFile(self.db_file_path, self._settings.backup_path)
        try:
            self._db = test_db.DatabaseController(
                self.db_connection_uri, create=create, defaultConnection=True
            )
        except ValueError:
            self._db = None

    def _set_prompt(self):
        """Set Prompt"""
        self.prompt = f"{self._prompt}: "

    def do_create(self, args):
        self._reset_db(create=True)

    def do_version(self, args):
        print(get_version(__package__))

    def do_view_log(self, args):
        try:
            with open(self._log_file, "r", encoding="UTF-8") as f:
                log_text = f.read()
        except OSError:
            self.perror(f"Error reading {self._log_file}")
            return
        self.ppaged(log_text)


def main() -> None:
    settings = Settings()

    if not settings.log_path.is_dir():
        sys.stderr.write(
            f"error: incorrect log_path {settings.log_path}, must be existing directory"
        )
        sys.exit(1)

    root_logger = logging.getLogger("")
    root_logger.setLevel(logging.DEBUG)

    log_file = pathlib.Path(settings.log_path, "test_db.log")
    logging_file_handler = logging.FileHandler(
        log_file,
        mode="w",
        encoding="utf-8",
    )
    logging_file_handler.setLevel(settings.log_level_file)
    logging_file_handler.setFormatter(
        logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    )
    root_logger.addHandler(logging_file_handler)

    logging_stream_handler = logging.StreamHandler(sys.stdout)
    logging_stream_handler.setLevel(settings.log_level_screen)
    logging_stream_handler.setFormatter(
        logging.Formatter("%(levelname)s - %(message)s")
    )
    root_logger.addHandler(logging_stream_handler)
    logger.debug("settings=%s", settings)

    test_db.databaseEncryptionKey = settings.database_encryption_key.get_secret_value()
    test_db.fernetIterations = settings.database_fernet_iterations

    console = Console(
        settings,
        log_file,
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
