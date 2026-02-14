import logging
import os
import pathlib


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
from typing_extensions import Literal, Optional, Type, Tuple, Union


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
    db_connection_uri: Optional[str] = Field(
        default=f"sqlite:{DEFAULT_DB_PATH}", description="sqlobject connection URI"
    )
    log_level_file: Union[
        int, Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    ] = Field(default="INFO", description="log level for file storage of log messages")
    log_level_screen: Union[
        int, Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    ] = Field(
        default="ERROR", description="log level for screen display of log messages"
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
