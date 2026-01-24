"""test-db typer applications

Provides typer applications for various test-db entities to assist
in building command-line applications that utilize test-db data.

Example:
    import typer
    from test_db.typer import key_value_app

    app = typer.Typer()
    app.add_typer(key_value_app, name="key-value")"
"""

import logging

from ._job import job_app as job_app
from ._job_key_value import job_key_value_app as job_key_value_app
from ._key_value import key_value_app as key_value_app
from ._organization import organization_app as organization_app
from ._organization_address import (
    organization_address_app as organization_address_app,
)
from ._organization_bank_account import (
    organization_bank_account_app as organization_bank_account_app,
)
from ._organization_key_value import (
    organization_key_value_app as organization_key_value_app,
)
from ._person import person_app as person_app
from ._person_address import person_address_app as person_address_app
from ._person_bank_account import (
    person_bank_account_app as person_bank_account_app,
)
from ._person_debit_card import person_debit_card_app as person_debit_card_app
from ._person_key_value import person_key_value_app as person_key_value_app
from ._person_secure_key_value import (
    person_secure_key_value_app as person_secure_key_value_app,
)

logger = logging.getLogger(__name__)

# Options: Available through _TyperOptions
interactive = False
