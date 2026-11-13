"""test_db maintenance script"""

import logging
import logging.handlers
import pathlib
import sys
from importlib.metadata import version as get_version
from typing import Annotated

import typer
from pydantic import SecretStr
from sqlobject.dberrors import DatabaseError

import test_db
from test_db import cli
from test_db._cli_settings import (
    Settings,
    initialize_default_paths,
    uses_default_database,
)

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


@app.command()
def version():
    print(get_version(__package__ or "not available"))


@app.callback()
def tdb_app_callback(
    ctx: typer.Context,
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
    if ctx.invoked_subcommand == "version":
        return

    settings = Settings()
    using_default_database = not db_connection_uri and uses_default_database(settings)
    if using_default_database:
        initialize_default_paths()
        settings = Settings()

    selected_db_connection_uri = (
        SecretStr(db_connection_uri)
        if db_connection_uri
        else settings.db_connection_uri
    )

    if (
        not selected_db_connection_uri
        or not selected_db_connection_uri.get_secret_value()
    ):
        sys.stderr.write("error: no database specified, use db_connection_uri")
        sys.exit(1)

    if using_default_database and not settings.log_path.is_dir():
        sys.stderr.write(
            f"error: incorrect log_path {settings.log_path}, must be existing directory"
        )
        sys.exit(1)

    handlers = []
    if settings.log_path.is_dir():
        try:
            logging_file_handler = logging.handlers.RotatingFileHandler(
                pathlib.Path(settings.log_path, "tdb.log"),
                encoding="utf-8",
                maxBytes=2 * 1024 * 1024,  # 2 MB
                backupCount=10,
            )
        except OSError:
            if using_default_database:
                raise
        else:
            logging_file_handler.setLevel(settings.log_level_file)
            logging_file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(module)s - %(levelname)s - %(name)s - %(message)s"
                )
            )
            handlers.append(logging_file_handler)

    logging_stream_handler = logging.StreamHandler(sys.stdout)
    logging_stream_handler.setLevel(settings.log_level_screen)
    logging_stream_handler.setFormatter(
        logging.Formatter("%(module)s - %(levelname)s - %(message)s")
    )
    handlers.append(logging_stream_handler)
    for handler in handlers:
        root_logger.addHandler(handler)
    root_logger.setLevel(min(handler.level for handler in handlers))

    logger.debug("settings=%s", settings)

    try:
        try:
            db = test_db.DatabaseController(
                selected_db_connection_uri, defaultConnection=True, upgrade=False
            )
        except ValueError as exc:
            if not upgrade or str(exc) != "test_db file needs upgrade":
                raise
            if not typer.confirm(
                "Upgrade the database? This removes encrypted test data."
            ):
                raise typer.Abort()
            db = test_db.DatabaseController(
                selected_db_connection_uri, defaultConnection=True, upgrade=True
            )
    except typer.Abort:
        raise
    except (ValueError, DatabaseError) as exc:
        raise typer.BadParameter(str(exc)) from exc
    ctx.call_on_close(db.close)


def main():
    app()


if __name__ == "__main__":
    main()
