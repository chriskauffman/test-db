"""test_db maintenance script"""

from importlib.metadata import version as get_version
import logging
import pathlib
import sys

import typer

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Annotated, Optional

import test_db
from test_db._backup_file import backupFile
from test_db._cli_settings import DEFAULT_DB_PATH, Settings
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


@app.command()
def version():
    print(get_version(__package__))


@app.callback()
def tdb_app_callback(
    db_connection_uri: Annotated[
        Optional[str], typer.Option(help="sqlobject connection string")
    ] = None,
    db_file_path: Annotated[
        Optional[pathlib.Path], typer.Option(help="path to sqlite database file")
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
    """main callback for test_db typer applications"""
    if db_connection_uri and db_file_path:
        sys.stderr.write(
            "error: both db_connection_uri and db_file_path are specified, only one is allowed"
        )
        sys.exit(1)
    test_db.typer.interactive = interactive
    settings = Settings()
    if db_file_path:
        db_file_path = db_file_path or settings.db_file_path or DEFAULT_DB_PATH
        try:
            backupFile(db_file_path, settings.backup_path)
        except ValueError:
            sys.stderr.write(
                f"error: incorrect backup_path {settings.backup_path}, "
                "must be existing directory"
            )
            sys.exit(1)
        if (
            not db_file_path.is_file()
            and db_file_path != test_db.IN_MEMORY_DB_FILE
            and not create
        ):
            sys.stderr.write(
                f"error: DB file {db_file_path} does not exist: "
                "check db_file_path in toml, env and command options or use --create"
            )
            sys.exit(1)
        db_connection_uri = f"sqlite:{str(db_file_path)}"

    if not db_connection_uri:
        sys.stderr.write(
            "error: no database specified, use db_connection_uri or db_file_path"
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
        db_connection_uri,
        create=create,
        defaultConnection=True,
        upgrade=upgrade,
    )


def main():
    app()


if __name__ == "__main__":
    main()
