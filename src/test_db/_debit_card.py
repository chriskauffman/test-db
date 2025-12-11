from calendar import monthrange
from datetime import date, datetime
import logging

import faker
from sqlobject import (  # type: ignore
    DateCol,
    DateTimeCol,
    JSONCol,
    RelatedJoin,
    SQLObject,
    StringCol,
)
from typeid import TypeID

from test_db._type_id_col import TypeIDCol
from test_db._gid import validGID


logger = logging.getLogger(__name__)


fake = faker.Faker()


def fake_credit_card_expire_to_date() -> date:
    """Generates a future expiration date for a credit/debit card"""
    fake_credit_card_expire = fake.credit_card_expire()
    expire_date = datetime.strptime(fake_credit_card_expire, "%m/%y").date()
    _, num_days = monthrange(expire_date.year, expire_date.month)
    return expire_date.replace(day=num_days)


class DebitCard(SQLObject):
    """DebitCard SQLObject

    Attributes:
        gID (TypeIDCol): global ID for the object
        attributes (JSONCol): JSON attributes for the object. **Note** - The DB
                              isn't updated until the object is saved (no DB updates
                              when individual fields are changed)
        description (StringCol): name of the object
        cardNumber (StringCol): debit card number (generated when not provided)
        cvv (StringCol): debit card security code (generated when not provided)
        expirationDate (DateCol): four digit year (generated when not provided)
        entities (RelatedJoin): list of people related to the debit card
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    _gIDPrefix: str = "dc"

    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)
    attributes: JSONCol = JSONCol(default={}, notNull=True)
    description: StringCol = StringCol(default=None)

    cardNumber: StringCol = StringCol(
        alternateID=True, length=16, default=fake.credit_card_number
    )
    cvv: StringCol = StringCol(length=3, default=fake.credit_card_security_code)
    expirationDate: DateCol = DateCol(default=fake_credit_card_expire_to_date)

    entities: RelatedJoin = RelatedJoin(
        "Entity", intermediateTable="debit_card_entity", createRelatedTable=False
    )

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    @property
    def visualID(self):
        return f"{self.gID}, {self.cardNumber}, {self.expirationDate.strftime('%m/%y')}"

    def _set_gID(self, value):
        if value:
            if validGID(value, self._gIDPrefix):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(TypeID(self._gIDPrefix))
