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

from sqlobject import SQLObjectNotFound  # type: ignore

import typer

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Literal, Optional, Union

import test_db
from test_db._views._base_view import BaseView

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
    interactive: Annotated[
        bool, typer.Option(help="allow interactive prompts for user input")
    ] = False,
    upgrade: Annotated[
        bool, typer.Option(help="upgrade the database if it is out of date")
    ] = False,
):
    BaseView.interactive = interactive
    settings = Settings()
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
            if db_file_path != test_db.IN_MEMORY_DB_FILE and not create:
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

    test_db.databaseEncryptionKey = settings.database_encryption_key.get_secret_value()
    test_db.fernetIterations = settings.database_fernet_iterations

    test_db.DatabaseController(
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


@add_app.command("address")
def address_add(occupant_gid: Optional[str] = None):
    if occupant_gid:
        try:
            occupant = test_db.Person.byGID(occupant_gid) or test_db.Organization.byGID(
                occupant_gid
            )
        except SQLObjectNotFound as exc:
            print(f"error: {str(exc)}")
            return
        test_db.AddressView.add(occupant=occupant)
    else:
        test_db.AddressView.add()


@add_app.command("bank-account")
def bank_account_add(owner_gid: Optional[str] = None):
    if owner_gid:
        try:
            owner = test_db.Person.byGID(owner_gid)
        except SQLObjectNotFound:
            try:
                test_db.Organization.byGID(owner_gid)
            except SQLObjectNotFound:
                print("error: person or organization not found")
                return
        test_db.BankAccountView.add(owner=owner)
    else:
        test_db.BankAccountView.add()


@add_app.command("debit-card")
def debit_card_add(owner_gid: Optional[str] = None):
    if owner_gid:
        try:
            owner = test_db.Person.byGID(owner_gid)
        except SQLObjectNotFound:
            try:
                test_db.Organization.byGID(owner_gid)
            except SQLObjectNotFound:
                print("error: person or organization not found")
                return
        test_db.DebitCardView.add(owner=owner)
    else:
        test_db.DebitCardView.add()


@add_app.command("job")
def job_add(employer_gid: str, employee_gid: str):
    employer = test_db.Organization.byGID(employer_gid)
    if not employer:
        print("error: organization not found")
        return
    employee = test_db.Person.byGID(employee_gid)
    if not employee:
        print("error: person not found")
        return
    test_db.JobView.add(employer=employer, employee=employee)


@add_app.command("key-value")
def key_value_add(key: str, value: str):
    test_db.KeyValueView.add(key=key, value=value)


@add_app.command("organization")
def organization_add():
    test_db.OrganizationView.add()


@add_app.command("person")
def person_add():
    test_db.PersonView.add()


@add_app.command("personal-key-value-secure")
def personal_key_value_secure_add(person_gid: str, key: str, value: str):
    try:
        person = test_db.Person.byGID(person_gid)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.PersonalKeyValueSecureView.add(person=person, key=key, value=value)


edit_app = typer.Typer()
app.add_typer(edit_app, name="edit")


@edit_app.command("address")
def address_edit(gid: str):
    try:
        address = test_db.Address.byGID(gid)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.AddressView(address).edit()


@edit_app.command("bank-account")
def bank_account_edit(gid: str):
    try:
        bank_account = test_db.BankAccount.byGID(gid)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.BankAccountView(bank_account).edit()


@edit_app.command("debit-card")
def debit_card_edit(gid: str):
    try:
        debit_card = test_db.DebitCard.byGID(gid)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.DebitCardView(debit_card).edit()


@edit_app.command("job")
def job_edit(gid: str):
    try:
        job = test_db.Job.byGID(gid)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.JobView(job).edit()


@edit_app.command("key-value")
def key_value_edit(key: str):
    try:
        key_value = test_db.KeyValue.byKey(key)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.KeyValueView(key_value).edit()


@edit_app.command("organization")
def organization_edit(gid: str):
    try:
        organization = test_db.Organization.byGID(gid)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.OrganizationView(organization).edit()


@edit_app.command("person")
def person_edit(gid: str):
    try:
        person = test_db.Person.byGID(gid)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.PersonView(person).edit()


list_app = typer.Typer()
app.add_typer(list_app, name="list")


@list_app.command("addresses")
def address_list():
    test_db.AddressView.list()


@list_app.command("bank-accounts")
def bank_account_list():
    test_db.BankAccountView.list()


@list_app.command("debit-cards")
def debit_card_list():
    test_db.DebitCardView.list()


@list_app.command("jobs")
def job_list():
    test_db.JobView.list()


@list_app.command("key-value")
def key_value_list():
    test_db.KeyValueView.list()


@list_app.command("organizations")
def organizations_list():
    test_db.OrganizationView.list()


@list_app.command("people")
def people_list():
    test_db.PersonView.list()


@list_app.command("personal-key-value-secure")
def personal_key_value_secure_list():
    test_db.PersonalKeyValueSecureView.list()


view_app = typer.Typer()
app.add_typer(view_app, name="view")


@view_app.command("address")
def address_view(gid: str):
    try:
        address = test_db.Address.byGID(gid)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.AddressView(address).viewDetails()


@view_app.command("bank-account")
def bank_account_view(gid: str):
    try:
        bank_account = test_db.BankAccount.byGID(gid)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.BankAccountView(bank_account).viewDetails()


@view_app.command("debit-card")
def debit_card_view(gid: str):
    try:
        debit_card = test_db.DebitCard.byGID(gid)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.DebitCardView(debit_card).viewDetails()


@view_app.command("job")
def job_view(gid: str):
    try:
        job = test_db.Job.byGID(gid)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.JobView(job).viewDetails()


@view_app.command("key-value")
def key_value_view(key: str):
    try:
        key_value = test_db.KeyValue.byKey(key)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.KeyValueView(key_value).viewDetails()


@view_app.command("organization")
def organization_view(gid: str):
    try:
        organization = test_db.Organization.byGID(gid)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.OrganizationView(organization).viewDetails()


@view_app.command("person")
def person_view(gid: str):
    try:
        person = test_db.Person.byGID(gid)
    except SQLObjectNotFound as exc:
        print(f"error: {str(exc)}")
        return
    test_db.PersonView(person).viewDetails()


@view_app.command("personal-key-value-secure")
def personal_key_value_secure_view(person_gid: str, key: str):
    person = test_db.Person.byGID(person_gid)
    if person:
        key_value = person.getPersonalKeyValueSecureByKey(key)
        if key_value:
            test_db.PersonalKeyValueSecureView(key_value).viewDetails()
    else:
        print("error: email not found")


class Settings(BaseSettings):
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


def main() -> None:
    app()


if __name__ == "__main__":
    main()
