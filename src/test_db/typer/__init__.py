"""test-db typer applications

Provides typer applications for various test-db entities to assist
in building command-line applications that utilize test-db data.

Example:
    import typer
    from test_db.typer import key_value_app

    app = typer.Typer()
    app.add_typer(key_value_app, name="key-value")"
"""

from ._address import address_app as address_app
from ._bank_account import bank_account_app as bank_account_app
from ._debit_card import debit_card_app as debit_card_app
from ._entity_key_value import entity_key_value_app as entity_key_value_app
from ._entity_secure_key_value import (
    entity_secure_key_value_app as entity_secure_key_value_app,
)
from ._job import job_app as job_app
from ._key_value import key_value_app as key_value_app
from ._organization import organization_app as organization_app
from ._person import person_app as person_app

# Options: Available through _TyperOptions
interactive = False
