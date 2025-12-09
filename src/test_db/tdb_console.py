"""test_db maintenance script"""

import datetime
from importlib.metadata import version as get_version
import logging
import os
import pathlib
import shutil
import sys

from typing_extensions import Type, Tuple

import cmd2

from pydantic import Field, SecretStr
from pydantic_settings import (
    BaseSettings,
    CliSuppress,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Literal, Optional, Union

import test_db
from test_db._cmd2 import (
    AddressCommandSet,
    BankAccountCommandSet,
    DebitCardCommandSet,
    JobCommandSet,
    KeyValueCommandSet,
    OrgnizationCommandSet,
    PersonCommandSet,
)

# OK to make dirs as default directory is "owned" by project
DEFAULT_CONFIG_PATH = pathlib.Path(pathlib.Path.home(), ".test_db")
if not os.path.exists(DEFAULT_CONFIG_PATH):
    os.makedirs(DEFAULT_CONFIG_PATH)

DEFAULT_DB_NAME = "test_db.sqlite"
DEFAULT_DB_PATH = pathlib.Path(DEFAULT_CONFIG_PATH, DEFAULT_DB_NAME)
DEFAULT_DB_PATH.touch()

DEFAULT_LOG_PATH = pathlib.Path(DEFAULT_CONFIG_PATH, "log")
if not os.path.exists(DEFAULT_LOG_PATH):
    os.makedirs(DEFAULT_LOG_PATH)

DEFAULT_BACKUP_PATH = pathlib.Path(DEFAULT_CONFIG_PATH, "backup")
if not os.path.exists(DEFAULT_BACKUP_PATH):
    os.makedirs(DEFAULT_BACKUP_PATH)

CONFIG_FILE_NAME = "test_db.toml"
pathlib.Path(DEFAULT_CONFIG_PATH, CONFIG_FILE_NAME).touch()

logger = logging.getLogger(__name__)


def locateFile(file_name: str) -> Optional[pathlib.Path]:
    for file_path in (
        pathlib.Path(file_name),
        pathlib.Path(DEFAULT_CONFIG_PATH, file_name),
    ):
        if file_path.is_file():
            return file_path
    return None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        toml_file=locateFile(CONFIG_FILE_NAME),
    )

    backup_path: pathlib.Path = Field(
        default=DEFAULT_BACKUP_PATH, description="directory for file backups"
    )
    database_encryption_key: CliSuppress[SecretStr] = Field(
        default=SecretStr(""),
        description="key to be used for encrypting sensitive database contents",
    )
    database_fernet_iterations: int = Field(
        default=1_200_000, description="number of iterations for fernet key generation"
    )
    db_file_path: Optional[pathlib.Path] = Field(
        default=None, description="database file"
    )
    log_level_file: Union[
        int, Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    ] = Field(default="INFO", description="log level for file storage of log messages")
    log_level_screen: Union[
        int, Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    ] = Field(
        default="WARNING", description="log level for screen display of log messages"
    )
    log_path: pathlib.Path = Field(
        default=DEFAULT_LOG_PATH, description="directory for logging activity"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """Add TOML to sources"""
        # pylint: disable=too-many-arguments
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls),
        )


class Console(cmd2.Cmd):
    """A simple cmd application."""

    # pylint: disable=unused-argument,too-many-public-methods,too-many-instance-attributes

    intro = "Welcome to the ODP simulator.  Type help or ? to list commands.\n"
    logger = logging.getLogger(__name__)
    _cmd_history_file = pathlib.Path(DEFAULT_CONFIG_PATH, "odp_cmd2_history")
    _prompt = "tdb"

    def __init__(self, settings: Settings, log_file: pathlib.Path, **kwargs) -> None:
        self.logger.debug("Function: Console.__init__")
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

        self.db_file_path = self._settings.db_file_path
        self.add_settable(
            cmd2.Settable(
                "db_file_path",
                self._val_type_db_file_path,
                "Database file name",
                self,
                onchange_cb=self._onchange_db_file_path,
            )
        )

        self._reset_db()
        self._set_prompt()

        # self._address_commands = AddressCommandSet()
        # self.register_command_set(self._address_commands)
        # self._database_commands = PersonCommandSet()
        # self.register_command_set(self._database_commands)

    def _onchange_db_file_path(self, param_name, old, new):
        """Execute when db_file_path setting changed"""
        self.logger.debug("Function: Console._onchange_db_file_path")
        if self._db.connection:
            self._db.close()
        self._reset_db()
        self._set_prompt()

    def _val_type_db_file_path(self, new: str):
        """Validate db_file_path"""
        if new != test_db.IN_MEMORY_DB_FILE:
            if not pathlib.Path(new).parent.exists():
                raise ValueError(f"db_file_path {new} invalid")
        return pathlib.Path(new)

    def _reset_db(self):
        # backup_file(self.db_file_path, self._settings.backup_path)

        try:
            self._db = test_db.DatabaseController(
                str(self.db_file_path), defaultConnection=True
            )
        except ValueError:
            self._db = None

    def _set_prompt(self):
        """Set Prompt"""
        self.prompt = f"{self._prompt}: "

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
    db_file_path = settings.db_file_path or DEFAULT_DB_PATH
    if db_file_path:
        if db_file_path.is_file():
            if settings.backup_path.is_dir():
                backup_file_path = pathlib.Path(
                    settings.backup_path,
                    db_file_path.with_suffix(
                        f".{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                        f"{db_file_path.suffix}"
                    ).name,
                )
                shutil.copy2(
                    db_file_path,
                    backup_file_path,
                )
            else:
                sys.stderr.write(
                    f"error: incorrect backup_path {settings.backup_path}, "
                    "must be existing directory"
                )
                sys.exit(1)
    else:
        sys.stderr.write(
            "error: DB file path not set: check db_file_path in toml, "
            "env and command options"
        )
        sys.exit(1)

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
            JobCommandSet(),
            KeyValueCommandSet(),
            OrgnizationCommandSet(),
            PersonCommandSet(),
        ],
    )
    sys.exit(console.cmdloop())


if __name__ == "__main__":
    main()
