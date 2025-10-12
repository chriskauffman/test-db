"""db_maintenance

Basic tools for managing a user DB
"""

import datetime
from importlib.metadata import version as get_version
import logging
import os
import pathlib
import shutil
import sys

from pydantic import Field, SecretStr
from pydantic_settings import (
    BaseSettings,
    CliApp,
    CliPositionalArg,
    CliSubCommand,
    CliSuppress,
    SettingsConfigDict,
)

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Literal, Optional, Union


import test_db as db

# OK to make dirs as default directory is "owned" by project
DEFAULT_CONFIG_PATH = pathlib.Path(pathlib.Path.home(), ".test_db")
if not os.path.exists(DEFAULT_CONFIG_PATH):
    os.makedirs(DEFAULT_CONFIG_PATH)

DEFAULT_LOG_PATH = pathlib.Path(DEFAULT_CONFIG_PATH, "log")
if not os.path.exists(DEFAULT_LOG_PATH):
    os.makedirs(DEFAULT_LOG_PATH)

DEFAULT_BACKUP_PATH = pathlib.Path(DEFAULT_CONFIG_PATH, "backup")
if not os.path.exists(DEFAULT_BACKUP_PATH):
    os.makedirs(DEFAULT_BACKUP_PATH)

TOML_FILE_NAME = "test_db.toml"
pathlib.Path(DEFAULT_CONFIG_PATH, TOML_FILE_NAME).touch()

SCRIPT_NAME = "tdb"
START_TIMESTAMP = datetime.datetime.now()

logger = logging.getLogger(__name__)


def locateTomlFile() -> Optional[pathlib.Path]:
    for toml_file_path in (
        pathlib.Path(TOML_FILE_NAME),
        pathlib.Path(DEFAULT_CONFIG_PATH, TOML_FILE_NAME),
    ):
        if os.path.exists(toml_file_path):
            return toml_file_path
    return None


class DBMaintenanceSettings(BaseSettings):
    """Test DB DB Maintenance Script

    Provides basic create and upgrade capability for the database
    """

    model_config = SettingsConfigDict(
        cli_implicit_flags=True,
        cli_parse_args=True,
        env_file=".env",
        extra="ignore",
        toml_file=locateTomlFile(),
    )

    create: bool = Field(
        default=False,
        description="databases are not created by default, creates the database file when True",
    )
    upgrade: bool = Field(
        default=False,
        description="upgrade the database if it is out of date",
    )

    backup_path: pathlib.Path = Field(
        default=DEFAULT_BACKUP_PATH, description="directory for file backups"
    )
    database_encryption_key: CliSuppress[SecretStr] = Field(
        default=SecretStr(""),
        description="key to be used for encrypting sensitive database contents",
    )
    database_fernet_iterations: int = Field(
        1_200_000, description="number of iterations for fernet key generation"
    )
    db_file_path: Optional[pathlib.Path] = Field(None, description="database file")
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


def main() -> None:
    class BankAccount(BaseSettings):
        name: str

    class BankAccountAdd(BankAccount):
        attach_to_person: bool = False

        def cli_cmd(self) -> None:
            if self.attach_to_person:
                # working_person.getBankAccountByName(self.add_bank_account)
                pass
            else:
                pass

    class DebitCard(BaseSettings):
        name: str

    class DebitCardAdd(DebitCard):
        pass

        def cli_cmd(self) -> None:
            # working_person.getDebitCardByName(self.add_debit_card)
            pass

    class Job(BaseSettings):
        pass

    class JobAdd(Job):
        pass

        def cli_cmd(self) -> None:
            # working_person.getJobByProviderId(self.add_job)
            pass

    class Person(BaseSettings):
        email: CliPositionalArg[str]

        def cli_cmd(self) -> None:
            CliApp.run_subcommand(self)

    class PersonDelete(Person):
        def cli_cmd(self) -> None:
            pass

    class PersonEdit(Person):
        def cli_cmd(self) -> None:
            person = db.Person.findByEmail(self.email)
            if person:
                db.PersonView(person).edit()
            else:
                print("error: email not found")

    class PersonView(Person):
        def cli_cmd(self) -> None:
            person = db.Person.findByEmail(self.email)
            if person:
                db.PersonView(person).viewDetails()
            else:
                print("error: email not found")

    class People(BaseSettings):
        pass

    class PeopleAdd(People):
        random: bool = False

        def cli_cmd(self) -> None:
            if self.random:
                print(f"{db.Person().email} added")
            else:
                new_person = db.PersonView.add()
                if new_person:
                    print(f"{new_person.email} added")

    class PeopleList(People):
        def cli_cmd(self) -> None:
            print("listing persons")
            db.PersonView.list()

    class Add(BaseSettings):
        bank_account: CliSubCommand[BankAccountAdd]
        debit_card: CliSubCommand[DebitCardAdd]
        job: CliSubCommand[JobAdd]
        people: CliSubCommand[PeopleAdd]

        def cli_cmd(self) -> None:
            CliApp.run_subcommand(self)

    class Edit(BaseSettings):
        person: CliSubCommand[PersonEdit]

        def cli_cmd(self) -> None:
            CliApp.run_subcommand(self)

    class List(BaseSettings):
        person: CliSubCommand[PeopleList]

        def cli_cmd(self) -> None:
            CliApp.run_subcommand(self)

    class Version(BaseSettings):
        def cli_cmd(self) -> None:
            print(get_version(__package__))

    class View(BaseSettings):
        person: CliSubCommand[PersonView]

        def cli_cmd(self) -> None:
            CliApp.run_subcommand(self)

    class Command(DBMaintenanceSettings):
        add: CliSubCommand[Add]
        edit: CliSubCommand[Edit]
        list: CliSubCommand[List]
        view: CliSubCommand[View]
        version: CliSubCommand[Version]

        def cli_cmd(self) -> None:
            if self.db_file_path:
                if self.db_file_path.is_file():
                    if self.backup_path.is_dir():
                        backup_file_path = pathlib.Path(
                            self.backup_path,
                            self.db_file_path.with_suffix(
                                f".{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                                f"{self.db_file_path.suffix}"
                            ).name,
                        )
                        shutil.copy2(
                            self.db_file_path,
                            backup_file_path,
                        )
                    else:
                        print(
                            f"error: incorrect backup_path {self.backup_path}, "
                            "must be existing directory"
                        )
                        sys.exit(1)
                else:
                    if self.db_file_path != db.IN_MEMORY_DB_FILE and not self.create:
                        print(
                            f"error: DB file {self.db_file_path} does not exist: "
                            "check db_file_path in toml, env and command options or use --create"
                        )
                        sys.exit(1)
            else:
                print(
                    "error: DB file path not set: check db_file_path in toml, "
                    "env and command options"
                )
                sys.exit(1)

            if not self.log_path.is_dir():
                print(
                    f"error: incorrect log_path {self.log_path}, must be existing directory"
                )
                sys.exit(1)

            root_logger = logging.getLogger("")
            root_logger.setLevel(logging.DEBUG)

            logging_file_handler = logging.FileHandler(
                pathlib.Path(self.log_path, "test_db.log"),
                mode="w",
                encoding="utf-8",
            )
            logging_file_handler.setLevel(self.log_level_file)
            logging_file_handler.setFormatter(
                logging.Formatter("%(name)s - %(levelname)s - %(message)s")
            )
            root_logger.addHandler(logging_file_handler)

            logging_stream_handler = logging.StreamHandler(sys.stdout)
            logging_stream_handler.setLevel(self.log_level_screen)
            logging_stream_handler.setFormatter(
                logging.Formatter("%(levelname)s - %(message)s")
            )
            root_logger.addHandler(logging_stream_handler)
            logger.debug("self=%s", self)

            db.databaseEncryptionKey = self.database_encryption_key.get_secret_value()
            db.fernetIterations = self.database_fernet_iterations

            db.DatabaseController(
                self.db_file_path,
                create=self.create,
                defaultConnection=True,
                upgrade=self.upgrade,
            )

            if self.add or self.edit or self.list or self.view or self.version:
                CliApp.run_subcommand(self)

    CliApp.run(Command)


if __name__ == "__main__":
    main()
