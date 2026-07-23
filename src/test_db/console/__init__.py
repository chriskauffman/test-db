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

import logging

from ._job import JobCommandSet as JobCommandSet
from ._job_key_value import JobKeyValueCommandSet as JobKeyValueCommandSet
from ._key_value import KeyValueCommandSet as KeyValueCommandSet
from ._organization import OrgnizationCommandSet as OrgnizationCommandSet
from ._organization_address import (
    OrganizationAddressCommandSet as OrganizationAddressCommandSet,
)
from ._organization_bank_account import (
    OrganizationBankAccountCommandSet as OrganizationBankAccountCommandSet,
)
from ._organization_key_value import (
    OrganizationKeyValueCommandSet as OrganizationKeyValueCommandSet,
)
from ._person import PersonCommandSet as PersonCommandSet
from ._person_address import PersonAddressCommandSet as PersonAddressCommandSet
from ._person_bank_account import (
    PersonBankAccountCommandSet as PersonBankAccountCommandSet,
)
from ._person_debit_card import PersonDebitCardCommandSet as PersonDebitCardCommandSet
from ._person_key_value import PersonKeyValueCommandSet as PersonKeyValueCommandSet
from ._person_secure_key_value import (
    PersonSecureKeyValueCommandSet as PersonSecureKeyValueCommandSet,
)

logger = logging.getLogger(__name__)
