from sqlobject import DatabaseIndex, ForeignKey, SQLObject  # type: ignore


class AddressEntity(SQLObject):
    class sqlmeta:
        table = "address_entity"

    address: ForeignKey = ForeignKey("Address")
    entity: ForeignKey = ForeignKey("Entity")

    debitCardEntityIndex: DatabaseIndex = DatabaseIndex(address, entity, unique=True)
