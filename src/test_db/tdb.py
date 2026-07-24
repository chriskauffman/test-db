"""test_db maintenance script"""

import logging
import logging.handlers
import pathlib
import sys
from importlib.metadata import version as get_version
from typing import Annotated

import typer

import test_db
from test_db import cli
from test_db._cli_settings import Settings

root_logger = logging.getLogger()
logger = logging.getLogger(__name__)

app = typer.Typer()
app.add_typer(cli.job_app, name="job")
app.add_typer(cli.job_key_value_app, name="job-key-value")
app.add_typer(cli.key_value_app, name="key-value")
app.add_typer(cli.organization_app, name="organization")
app.add_typer(cli.organization_address_app, name="organization-address")
app.add_typer(cli.organization_bank_account_app, name="organization-bank-account")
app.add_typer(cli.organization_key_value_app, name="organization-key-value")
app.add_typer(cli.person_app, name="person")
app.add_typer(cli.person_address_app, name="person-address")
app.add_typer(cli.person_bank_account_app, name="person-bank-account")
app.add_typer(cli.person_debit_card_app, name="person-debit-card")
app.add_typer(cli.person_key_value_app, name="person-key-value")
app.add_typer(cli.person_secure_key_value_app, name="person-secure-key-value")


@app.command()
def version():
    print(get_version(__package__ or "not available"))


@app.callback()
def tdb_app_callback(
    db_connection_uri: Annotated[
        str | None,
        typer.Option("--db-connection-uri", "-d", help="sqlobject connection string"),
    ] = None,
    interactive: Annotated[
        bool,
        typer.Option(
            "--interactive", "-i", help="allow interactive prompts for user input"
        ),
    ] = False,
    upgrade: Annotated[
        bool,
        typer.Option(
            "--upgrade", "-u", help="upgrade the database if it is out of date"
        ),
    ] = False,
) -> None:
    """main callback for test_db typer applications"""
    cli.interactive = interactive
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

    logging_file_handler = logging.handlers.RotatingFileHandler(
        pathlib.Path(settings.log_path, "tdb.log"),
        encoding="utf-8",
        maxBytes=2 * 1024 * 1024,  # 2 MB
        backupCount=10,
    )
    logging_file_handler.setLevel(settings.log_level_file)
    logging_file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(module)s - %(levelname)s - %(name)s - %(message)s"
        )
    )
    root_logger.addHandler(logging_file_handler)

    logging_stream_handler = logging.StreamHandler(sys.stdout)
    logging_stream_handler.setLevel(settings.log_level_screen)
    logging_stream_handler.setFormatter(
        logging.Formatter("%(module)s - %(levelname)s - %(message)s")
    )
    root_logger.addHandler(logging_stream_handler)
    root_logger.setLevel(min(logging_file_handler.level, logging_stream_handler.level))

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
