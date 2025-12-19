"""test-db cmd2 command sets

Provides cmd2 command sets for various test-db entities to assist
in building cmd2 applications that utilize test-db data.

Example:
    impprt cmd2
    from test_db.cmd2 import KeyValueCommandSet

    class MyApp(cmd2.Cmd):
        pass

    console = MyApp(
        settings,
        log_file,
        command_sets=[AddressCommandSet(), ],
    )
    sys.exit(console.cmdloop())
"""

from ._address import AddressCommandSet as AddressCommandSet
from ._bank_account import BankAccountCommandSet as BankAccountCommandSet
from ._debit_card import DebitCardCommandSet as DebitCardCommandSet
from ._entity_key_value import EntityKeyValueCommandSet as EntityKeyValueCommandSet
from ._entity_secure_key_value import (
    EntitySecureKeyValueCommandSet as EntitySecureKeyValueCommandSet,
)
from ._job import JobCommandSet as JobCommandSet
from ._key_value import KeyValueCommandSet as KeyValueCommandSet
from ._organization import OrgnizationCommandSet as OrgnizationCommandSet
from ._person import PersonCommandSet as PersonCommandSet
