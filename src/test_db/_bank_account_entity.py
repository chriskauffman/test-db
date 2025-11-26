from sqlobject import DatabaseIndex, ForeignKey, SQLObject  # type: ignore


class BankAccountEntity(SQLObject):
    class sqlmeta:
        table = "bank_account_entity"

    bankAccount: ForeignKey = ForeignKey("BankAccount")
    entity: ForeignKey = ForeignKey("Entity")

    debitCardEntityIndex: DatabaseIndex = DatabaseIndex(
        bankAccount, entity, unique=True
    )
