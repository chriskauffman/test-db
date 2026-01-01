import logging

from sqlobject import DatabaseIndex, ForeignKey, SQLObject  # type: ignore

logger = logging.getLogger(__name__)


class BankAccountEntity(SQLObject):
    """Custom Intermediate Table for BankAccount+Entity

    SQLObject doesn't offer a unique index on the joined tables which
    allows multiple duplicate joins to be created. TestDB wanted to prevent
    these duplicates, so this custom table was created with the appropriate
    index.

    https://www.sqlobject.org/FAQ.html#how-can-i-define-my-own-intermediate-table-in-my-many-to-many-relationship

    """

    class sqlmeta:
        table = "bank_account_entity"

    bankAccount: ForeignKey = ForeignKey("BankAccount")
    entity: ForeignKey = ForeignKey("Entity")

    debitCardEntityIndex: DatabaseIndex = DatabaseIndex(
        bankAccount, entity, unique=True
    )
