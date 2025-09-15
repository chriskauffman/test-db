"""db_maintenance

Basic tools for managing a user DB
"""

import datetime
from importlib.metadata import version as get_version
import logging
import os
import pathlib
import sys

from pydantic import Field, SecretStr, ValidationError
import pydantic_settings

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Literal, Optional, Union


import test_db as db
# from ._backup_file import backup_file
# from ._logger_setup import logger_setup

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


def locateTomlFile() -> Optional[pathlib.Path]:
    for toml_file_path in (
        pathlib.Path(TOML_FILE_NAME),
        pathlib.Path(DEFAULT_CONFIG_PATH, TOML_FILE_NAME),
    ):
        if os.path.exists(toml_file_path):
            return toml_file_path
    return None


class DBMaintenanceSettings(pydantic_settings.BaseSettings):
    """Test DB DB Maintenance Script

    Provides basic create and upgrade capability for the database
    """

    model_config = pydantic_settings.SettingsConfigDict(
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
    version: bool = Field(default=False, description="show the current version")

    add_person: bool = False
    add_random_person: bool = False
    delete_person: bool = False
    edit_person: bool = False
    list_people: bool = Field(
        default=False,
        description="lists the people in the database",
    )
    select_person: Optional[str] = None
    view_person: bool = False

    add_bank_account: Optional[str] = None
    add_debit_card: Optional[str] = None
    add_job: Optional[int] = None
    provider_id: Optional[int] = None

    backup_path: pathlib.Path = Field(
        default=DEFAULT_BACKUP_PATH, description="directory for file backups"
    )
    database_encryption_key: pydantic_settings.CliSuppress[SecretStr] = Field(
        default=SecretStr(""),
        description="key to be used for encrypting sensitive database contents",
    )
    db_file_path: pathlib.Path = Field(
        default=pathlib.Path(DEFAULT_CONFIG_PATH, "test_db.sqlite"),
        description="database file",
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


class VersionSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        cli_implicit_flags=True,
        cli_parse_args=True,
    )

    version: bool = Field(default=False, description="show the current version")


def main() -> None:
    try:
        settings = DBMaintenanceSettings()  # type: ignore
    except ValidationError as e:
        # if version has been requested supply that
        if VersionSettings().version:
            print(get_version(__package__))
            return
        print("error: incorrect settings - check toml, env and command options")
        for error in e.errors():
            print(f"{error.get('msg')}: {error.get('loc')}")
        sys.exit(1)

    if settings.version:
        print(get_version(__package__))
        return

    # log_file = logger_setup(
    #     SCRIPT_NAME,
    #     settings.log_path,
    #     file_timestamp=START_TIMESTAMP,
    #     log_level_screen=settings.log_level_screen,
    #     log_level_file=settings.log_level_file,
    # )
    # print(f"Log: {log_file}")
    logger = logging.getLogger(SCRIPT_NAME)
    logger.debug("settings=%s", settings)

    if (
        settings.db_file_path != db.IN_MEMORY_DB_FILE
        and not os.path.isfile(settings.db_file_path)
        and not settings.create
    ):
        # ToDo: Any way to do this with pydantic?
        # parser.print_usage()
        print(f"DB file {settings.db_file_path} does not exist")
        sys.exit(1)

    db.databaseEncryptionKey = settings.database_encryption_key.get_secret_value()

    # backup_file(
    #     settings.db_file_path, settings.backup_path, file_timestamp=START_TIMESTAMP
    # )
    db.DatabaseController(
        settings.db_file_path,
        create=settings.create,
        defaultConnection=True,
        upgrade=settings.upgrade,
    )

    if settings.add_person:
        add_person = db.PersonView.add()
        if not add_person:
            logger.error("user add failed")
            sys.exit(1)
        logger.warning(
            "Overriding user %s with user %s",
            settings.select_person,
            add_person.email,
        )
        # As email is generated, argument must be set to new email
        settings.select_person = add_person.email

    if settings.add_random_person:
        add_person = db.Person()
        logger.warning(
            "Overriding user %s with randomly generated user %s",
            settings.select_person,
            add_person.email,
        )
        # As email is generated, argument must be set to new email
        settings.select_person = add_person.email

    if settings.select_person:
        working_person = db.Person.findByEmail(settings.select_person)
        if working_person:
            if settings.edit_person:
                db.PersonView(working_person).edit()

            if settings.add_bank_account:
                working_person.getBankAccountByName(settings.add_bank_account)

            if settings.add_debit_card:
                working_person.getDebitCardByName(settings.add_debit_card)

            if settings.add_job:
                working_person.getJobByProviderId(settings.add_job)

            if settings.view_person:
                db.PersonView(working_person).viewDetails()

    if settings.list_people:
        db.PersonView.list()


if __name__ == "__main__":
    main()
