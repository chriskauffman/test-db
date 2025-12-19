"""test-db views

Provides view classes for various test-db entities to assist apps
and utilities in displaying and interacting with test-db data.

Example:
    from test_db._views import KeyValueView

    new_kv = KeyValueView.add(key="example_key", value="example_value")
    KeyValueView.list() # Lists all key-value pairs in the test database
    keyValueView(new_kv).edit() # Opens an editor to modify the key-value pair
"""

from ._address import AddressView as AddressView
from ._bank_account import BankAccountView as BankAccountView
from ._debit_card import DebitCardView as DebitCardView
from ._entity_key_value import EntityKeyValueView as EntityKeyValueView
from ._entity_secure_key_value import (
    EntitySecureKeyValueView as EntitySecureKeyValueView,
)
from ._job import JobView as JobView
from ._key_value import KeyValueView as KeyValueView
from ._organization import OrganizationView as OrganizationView
from ._person import PersonView as PersonView
