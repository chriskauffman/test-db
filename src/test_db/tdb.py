"""test_db maintenance script"""

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

import test_db
from test_db.typer import (
    address_app,
    bank_account_app,
    debit_card_app,
    entity_key_value_app,
    entity_secure_key_value_app,
    job_app,
    key_value_app,
    organization_app,
    person_app,
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

app = typer.Typer()
app.add_typer(address_app, name="address")
app.add_typer(bank_account_app, name="bank-account")
app.add_typer(debit_card_app, name="debit-card")
app.add_typer(entity_key_value_app, name="entity-key-value")
app.add_typer(entity_secure_key_value_app, name="entity-secure-key-value")
app.add_typer(job_app, name="job")
app.add_typer(key_value_app, name="key-value")
app.add_typer(organization_app, name="organization")
app.add_typer(person_app, name="person")
state = {"interactive": False}


def locateFile(file_name: str) -> Optional[pathlib.Path]:
    for file_path in (
        pathlib.Path(file_name),
        pathlib.Path(DEFAULT_CONFIG_PATH, file_name),
    ):
        if file_path.is_file():
            return file_path
    return None


@app.command()
def version():
    print(get_version(__package__))


add_app = typer.Typer()
app.add_typer(add_app, name="add")


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


@app.callback()
def main(
    db_file_path: Annotated[
        Optional[pathlib.Path], typer.Option(help="path to database file")
    ] = None,
    create: Annotated[
        bool,
        typer.Option(
            help="databases are not created by default, creates the database file when True"
        ),
    ] = False,
    interactive: Annotated[
        bool, typer.Option(help="allow interactive prompts for user input")
    ] = False,
    upgrade: Annotated[
        bool, typer.Option(help="upgrade the database if it is out of date")
    ] = False,
) -> None:
    state["interactive"] = interactive
    test_db.typer.interactive = interactive
    settings = Settings()
    db_file_path = db_file_path or settings.db_file_path or DEFAULT_DB_PATH
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
            if db_file_path != test_db.IN_MEMORY_DB_FILE and not create:
                sys.stderr.write(
                    f"error: DB file {db_file_path} does not exist: "
                    "check db_file_path in toml, env and command options or use --create"
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

    test_db.databaseEncryptionKey = settings.database_encryption_key.get_secret_value()
    test_db.fernetIterations = settings.database_fernet_iterations

    test_db.DatabaseController(
        db_file_path,
        create=create,
        defaultConnection=True,
        upgrade=upgrade,
    )


if __name__ == "__main__":
    app()
