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
from sqlobject.dberrors import DuplicateEntryError  # type: ignore

from formencode.validators import Invalid  # type: ignore
import typer

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Literal, Optional, Union

import test_db

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
state = {"interactive": True}


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


def validate_address(gid: str):
    try:
        return test_db.Address.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


def validate_bank_account(gid: str):
    try:
        return test_db.BankAccount.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


def validate_debit_card(gid: str):
    try:
        return test_db.DebitCard.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


def validate_entity(gid: str):
    try:
        return test_db.Person.byGID(gid)
    except Invalid as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)
    except SQLObjectNotFound:
        try:
            return test_db.Organization.byGID(gid)
        except SQLObjectNotFound:
            sys.stderr.write("error: person or organization not found")
            sys.exit(1)


def validate_job(gid: str):
    try:
        return test_db.Job.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


def validate_key(key: str):
    try:
        return test_db.KeyValue.byKey(key)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


def validate_orgnization(gid: str):
    try:
        return test_db.Organization.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


def validate_person(gid: str):
    try:
        return test_db.Person.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@add_app.command("address")
def add_address(entity_gid: Optional[str] = None):
    if entity_gid:
        entity = validate_entity(entity_gid)
        test_db.AddressView.add(entity=entity, interactive=state["interactive"])
    else:
        test_db.AddressView.add(interactive=state["interactive"])


@add_app.command("bank-account")
def add_bank_account(entity_gid: Optional[str] = None):
    if entity_gid:
        entity = validate_entity(entity_gid)
        test_db.BankAccountView.add(entity=entity, interactive=state["interactive"])
    else:
        test_db.BankAccountView.add(interactive=state["interactive"])


@add_app.command("debit-card")
def debit_card_add(entity_gid: Optional[str] = None):
    if entity_gid:
        entity = validate_entity(entity_gid)
        test_db.DebitCardView.add(entity=entity, interactive=state["interactive"])
    else:
        test_db.DebitCardView.add(interactive=state["interactive"])


@add_app.command("job")
def add_job(organization_gid: Optional[str] = None, person_gid: Optional[str] = None):
    organization = None
    person = None
    if organization_gid:
        organization = validate_orgnization(organization_gid)
    if person_gid:
        person = validate_person(person_gid)
    test_db.JobView.add(
        organization=organization, person=person, interactive=state["interactive"]
    )


@add_app.command("key-value")
def add_key_value(key: str, value: str):
    try:
        test_db.KeyValueView.add(key=key, value=value, interactive=state["interactive"])
    except DuplicateEntryError as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@add_app.command("organization")
def add_organization():
    test_db.OrganizationView.add(interactive=state["interactive"])


@add_app.command("person")
def add_person():
    test_db.PersonView.add(interactive=state["interactive"])


@add_app.command("personal-key-value-secure")
def add_personal_key_value_secure(person_gid: str, key: str, value: str):
    person = validate_person(person_gid)
    try:
        test_db.PersonalKeyValueSecureView.add(
            person=person, key=key, value=value, interactive=state["interactive"]
        )
    except DuplicateEntryError as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


connect_app = typer.Typer()
app.add_typer(connect_app, name="connect")


@connect_app.command("address")
def connect_address(gid: str, entity_gid: str):
    address = validate_address(gid)
    entity = validate_entity(entity_gid)
    try:
        entity.addAddress(address)
    except DuplicateEntryError:
        pass


@connect_app.command("bank-account")
def connect_bank_account(gid: str, entity_gid: str):
    bank_account = validate_bank_account(gid)
    entity = validate_entity(entity_gid)
    try:
        entity.addBankAccount(bank_account)
    except DuplicateEntryError:
        pass


@connect_app.command("debit-card")
def connect_debit_card(gid: str, entity_gid: str):
    debit_card = validate_debit_card(gid)
    entity = validate_entity(entity_gid)
    try:
        entity.addDebitCard(debit_card)
    except DuplicateEntryError:
        pass


delete_app = typer.Typer()
app.add_typer(delete_app, name="delete")


@delete_app.command("address")
def delete_address(gid: str):
    address = validate_address(gid)
    address.destroySelf()


@delete_app.command("bank-account")
def delete_bank_account(gid: str):
    bank_account = validate_bank_account(gid)
    bank_account.destroySelf()


@delete_app.command("debit-card")
def delete_debit_card(gid: str):
    debit_card = validate_debit_card(gid)
    debit_card.destroySelf()


@delete_app.command("job")
def delete_job(gid: str):
    job = validate_job(gid)
    job.destroySelf()


@delete_app.command("key-value")
def delete_key_value(key: str):
    if key in test_db.RESTRICTED_KEYS:
        sys.stderr.write(f"error: key '{key}' is restricted and cannot be deleted")
        sys.exit(1)
    key_value = validate_key(key)
    key_value.destroySelf()


@delete_app.command("organization")
def delete_organization(gid: str):
    organization = validate_orgnization(gid)
    organization.destroySelf()


@delete_app.command("person")
def delete_person(gid: str):
    person = validate_person(gid)
    person.destroySelf()


@delete_app.command("personal-key-value-secure")
def delete_personal_key_value_secure(person_gid: str, key: str):
    person = validate_person(person_gid)
    key_value = person.getPersonalKeyValueSecureByKey(key)
    if key_value:
        key_value.destroySelf()


disconnect_app = typer.Typer()
app.add_typer(disconnect_app, name="disconnect")


@disconnect_app.command("address")
def disconnect_address(gid: str, entity_gid: str):
    address = validate_address(gid)
    entity = validate_entity(entity_gid)
    entity.removeAddress(address)


@disconnect_app.command("bank-account")
def disconnect_bank_account(gid: str, entity_gid: str):
    bank_account = validate_bank_account(gid)
    entity = validate_entity(entity_gid)
    entity.removeBankAccount(bank_account)


@disconnect_app.command("debit-card")
def disconnect_debit_card(gid: str, entity_gid: str):
    debit_card = validate_debit_card(gid)
    entity = validate_entity(entity_gid)
    entity.removeDebitCard(debit_card)


edit_app = typer.Typer()
app.add_typer(edit_app, name="edit")


@edit_app.command("address")
def edit_address(gid: str):
    address = validate_address(gid)
    test_db.AddressView(address).edit()


@edit_app.command("bank-account")
def edit_bank_account(gid: str):
    bank_account = validate_bank_account(gid)
    test_db.BankAccountView(bank_account).edit()


@edit_app.command("debit-card")
def edit_debit_card(gid: str):
    debit_card = validate_debit_card(gid)
    test_db.DebitCardView(debit_card).edit()


@edit_app.command("job")
def edit_job(gid: str):
    job = validate_job(gid)
    test_db.JobView(job).edit()


@edit_app.command("key-value")
def edit_key_value(key: str):
    if key in test_db.RESTRICTED_KEYS:
        sys.stderr.write(f"error: key '{key}' is restricted and cannot be edited")
        sys.exit(1)
    key_value = validate_key(key)
    test_db.KeyValueView(key_value).edit()


@edit_app.command("organization")
def edit_organization(gid: str):
    organization = validate_orgnization(gid)
    test_db.OrganizationView(organization).edit()


@edit_app.command("person")
def edit_person(gid: str):
    person = validate_person(gid)
    test_db.PersonView(person).edit()


list_app = typer.Typer()
app.add_typer(list_app, name="list")


@list_app.command("addresses")
def list_address():
    test_db.AddressView.list()


@list_app.command("bank-accounts")
def list_bank_account():
    test_db.BankAccountView.list()


@list_app.command("debit-cards")
def list_debit_card():
    test_db.DebitCardView.list()


@list_app.command("jobs")
def list_job():
    test_db.JobView.list()


@list_app.command("key-value")
def list_key_value():
    test_db.KeyValueView.list()


@list_app.command("organizations")
def list_organizations():
    test_db.OrganizationView.list()


@list_app.command("people")
def list_people():
    test_db.PersonView.list()


@list_app.command("personal-key-value-secure")
def list_personal_key_value_secure():
    test_db.PersonalKeyValueSecureView.list()


view_app = typer.Typer()
app.add_typer(view_app, name="view")


@view_app.command("address")
def view_address(gid: str):
    address = validate_address(gid)
    test_db.AddressView(address).viewDetails()


@view_app.command("bank-account")
def view_bank_account(gid: str):
    bank_account = validate_bank_account(gid)
    test_db.BankAccountView(bank_account).viewDetails()


@view_app.command("debit-card")
def view_debit_card(gid: str):
    debit_card = validate_debit_card(gid)
    test_db.DebitCardView(debit_card).viewDetails()


@view_app.command("job")
def view_job(gid: str):
    job = validate_job(gid)
    test_db.JobView(job).viewDetails()


@view_app.command("key-value")
def view_key_value(key: str):
    key_value = validate_key(key)
    test_db.KeyValueView(key_value).viewDetails()


@view_app.command("organization")
def view_organization(gid: str):
    organization = validate_orgnization(gid)
    test_db.OrganizationView(organization).viewDetails()


@view_app.command("person")
def view_person(gid: str):
    person = validate_person(gid)
    test_db.PersonView(person).viewDetails()


@view_app.command("personal-key-value-secure")
def view_personal_key_value_secure(person_gid: str, key: str):
    person = validate_person(person_gid)
    key_value = person.getPersonalKeyValueSecureByKey(key)
    if key_value:
        test_db.PersonalKeyValueSecureView(key_value).viewDetails()


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
