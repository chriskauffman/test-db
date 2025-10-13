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

from typing_extensions import Annotated, Type, Tuple

from pydantic import Field, SecretStr
from pydantic_settings import (
    BaseSettings,
    CliSuppress,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

import typer

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
app = typer.Typer()


def locateTomlFile() -> Optional[pathlib.Path]:
    for toml_file_path in (
        pathlib.Path(TOML_FILE_NAME),
        pathlib.Path(DEFAULT_CONFIG_PATH, TOML_FILE_NAME),
    ):
        if os.path.exists(toml_file_path):
            return toml_file_path
    return None


@app.callback()
def app_callback(
    db_file_path: pathlib.Path,
    create: Annotated[
        bool,
        typer.Option(
            help="databases are not created by default, creates the database file when True"
        ),
    ] = False,
    upgrade: Annotated[
        bool, typer.Option(help="upgrade the database if it is out of date")
    ] = False,
):
    print(db_file_path)
    settings = DBMaintenanceSettings()
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
                print(
                    f"error: incorrect backup_path {settings.backup_path}, "
                    "must be existing directory"
                )
                sys.exit(1)
        else:
            if db_file_path != db.IN_MEMORY_DB_FILE and not create:
                print(
                    f"error: DB file {db_file_path} does not exist: "
                    "check db_file_path in toml, env and command options or use --create"
                )
                sys.exit(1)
    else:
        print(
            "error: DB file path not set: check db_file_path in toml, "
            "env and command options"
        )
        sys.exit(1)

    if not settings.log_path.is_dir():
        print(
            f"error: incorrect log_path {settings.log_path}, must be existing directory"
        )
        sys.exit(1)

    root_logger = logging.getLogger("")
    root_logger.setLevel(logging.DEBUG)

    logging_file_handler = logging.FileHandler(
        pathlib.Path(settings.log_path, "test_db.log"),
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

    db.databaseEncryptionKey = settings.database_encryption_key.get_secret_value()
    db.fernetIterations = settings.database_fernet_iterations

    db.DatabaseController(
        db_file_path,
        create=create,
        defaultConnection=True,
        upgrade=upgrade,
    )


@app.command()
def version():
    print(get_version(__package__))


add_app = typer.Typer()
app.add_typer(add_app, name="add")


@add_app.command("bank-account")
def bank_account_add(
    description: Optional[str] = None, person_email: Optional[str] = None
):
    if person_email:
        person = db.Person.findByEmail(person_email)
        if person:
            person.getBankAccountByName(description or "default")
        else:
            print("error: email not found")
    else:
        db.BankAccount(description=description)


@add_app.command("debit-card")
def debit_card_add(
    description: Optional[str] = None, person_email: Optional[str] = None
):
    if person_email:
        person = db.Person.findByEmail(person_email)
        if person:
            person.getDebitCardByName(description or "default")
        else:
            print("error: email not found")
    else:
        db.DebitCard(description=description)


@add_app.command("person")
def person_add(random: bool = False):
    if random:
        print(f"{db.Person().email} added")
    else:
        new_person = db.PersonView.add()
        if new_person:
            print(f"{new_person.email} added")


edit_app = typer.Typer()
app.add_typer(edit_app, name="edit")


@edit_app.command("person")
def person_edit(email: str):
    person = db.Person.findByEmail(email)
    if person:
        db.PersonView(person).edit()
    else:
        print("error: email not found")


list_app = typer.Typer()
app.add_typer(list_app, name="list")


@list_app.command("people")
def people_list():
    db.PersonView.list()


view_app = typer.Typer()
app.add_typer(view_app, name="view")


@view_app.command("person")
def person_view(email: str, db_file_path: Optional[pathlib.Path] = None):
    person = db.Person.findByEmail(email)
    if person:
        db.PersonView(person).viewDetails()
    else:
        print("error: email not found")


class DBMaintenanceSettings(BaseSettings):
    """Test DB DB Maintenance Script

    Provides basic create and upgrade capability for the database
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        toml_file=locateTomlFile(),
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

        # if self.attach_to_person:
        # working_person.getBankAccountByName(self.add_bank_account)

        # working_person.getDebitCardByName(self.add_debit_card)

        # working_person.getJobByProviderId(self.add_job)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
