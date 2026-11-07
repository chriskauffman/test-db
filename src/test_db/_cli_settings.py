import logging
import pathlib
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import (
    BaseSettings,
    CliSuppress,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

# Default paths are initialized by the CLI entry points, not on import.
DEFAULT_CONFIG_PATH = pathlib.Path(pathlib.Path.home(), ".test_db")
DEFAULT_DB_NAME = "test_db.sqlite"
DEFAULT_DB_PATH = pathlib.Path(DEFAULT_CONFIG_PATH, DEFAULT_DB_NAME)
DEFAULT_LOG_PATH = pathlib.Path(DEFAULT_CONFIG_PATH, "log")
DEFAULT_BACKUP_PATH = pathlib.Path(DEFAULT_CONFIG_PATH, "backup")
CONFIG_FILE_NAME = "test_db.toml"

logger = logging.getLogger(__name__)


def initialize_default_paths() -> None:
    """Create the default CLI directories and files."""
    DEFAULT_CONFIG_PATH.mkdir(parents=True, exist_ok=True)
    DEFAULT_DB_PATH.touch(exist_ok=True)
    DEFAULT_LOG_PATH.mkdir(exist_ok=True)
    DEFAULT_BACKUP_PATH.mkdir(exist_ok=True)
    pathlib.Path(DEFAULT_CONFIG_PATH, CONFIG_FILE_NAME).touch(exist_ok=True)


def locateFile(file_name: str) -> pathlib.Path | None:
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
        default=1_200_000,
        description="PBKDF2 iterations when initializing encryption metadata",
    )
    db_connection_uri: SecretStr | None = Field(
        default=SecretStr(f"sqlite:{DEFAULT_DB_PATH}"),
        description="sqlobject connection URI",
    )
    log_level_file: int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = (
        Field(default="INFO", description="log level for file storage of log messages")
    )
    log_level_screen: int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = (
        Field(
            default="ERROR", description="log level for screen display of log messages"
        )
    )
    log_path: pathlib.Path = Field(
        default=DEFAULT_LOG_PATH, description="directory for logging activity"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Add TOML to sources"""
        # pylint: disable=too-many-arguments
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls),
        )
