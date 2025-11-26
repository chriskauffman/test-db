from sqlobject import DatabaseIndex, ForeignKey, SQLObject  # type: ignore


class DebitCardEntity(SQLObject):
    """Custom Intermediate Table for DebitCard+Entity

    SQLObject doesn't offer a unique index on the joined tables which
    allows multiple duplicate joins to be created. TestDB wanted to prevent
    these duplicates, so this custom table was created with the appropriate
    index.

    https://www.sqlobject.org/FAQ.html#how-can-i-define-my-own-intermediate-table-in-my-many-to-many-relationship

    """

    class sqlmeta:
        table = "debit_card_entity"

    debitCard: ForeignKey = ForeignKey("DebitCard")
    entity: ForeignKey = ForeignKey("Entity")

    debitCardEntityIndex: DatabaseIndex = DatabaseIndex(debitCard, entity, unique=True)
