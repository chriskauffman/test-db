from sqlobject import DatabaseIndex, ForeignKey, SQLObject  # type: ignore


class DebitCardEntity(SQLObject):
    class sqlmeta:
        table = "debit_card_entity"

    debitCard: ForeignKey = ForeignKey("DebitCard")
    entity: ForeignKey = ForeignKey("Entity")

    debitCardEntityIndex: DatabaseIndex = DatabaseIndex(debitCard, entity, unique=True)
