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
from test_db._cli_settings import Settings
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
    interactive: Annotated[
        bool, typer.Option(help="allow interactive prompts for user input")
    ] = False,
    upgrade: Annotated[
        bool, typer.Option(help="upgrade the database if it is out of date")
    ] = False,
) -> None:
    """main callback for test_db typer applications"""
    test_db.typer.interactive = interactive
    settings = Settings()

    db_connection_uri = db_connection_uri or settings.db_connection_uri

    if not db_connection_uri:
        sys.stderr.write("error: no database specified, use db_connection_uri")
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
        defaultConnection=True,
    )


def main():
    app()


if __name__ == "__main__":
    main()
