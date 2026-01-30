from calendar import monthrange
from datetime import date, datetime
import logging

import faker
from sqlobject import (  # type: ignore
    DatabaseIndex,
    DateCol,
    DateTimeCol,
    ForeignKey,
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


class PersonDebitCard(SQLObject):
    """DebitCard SQLObject

    Attributes:
        person (ForeignKey): persn this debit card belongs to
        gID (TypeIDCol): global ID for the object
        description (StringCol): name of the object
        cardNumber (StringCol): debit card number (generated when not provided)
        cvv (StringCol): debit card security code (generated when not provided)
        expirationDate (DateCol): four digit year (generated when not provided)
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
        personCardNumberIndex (DatabaseIndex):
    """

    _gIDPrefix: str = "dc"

    person: ForeignKey = ForeignKey("Person", cascade=True, notNone=True)
    gID: TypeIDCol = TypeIDCol(alternateID=True, default=None)
    description: StringCol = StringCol(default=None)
    cardNumber: StringCol = StringCol(alternateID=True, default=fake.credit_card_number)
    cvv: StringCol = StringCol(default=fake.credit_card_security_code)
    expirationDate: DateCol = DateCol(default=fake_credit_card_expire_to_date)

    createdAt: DateTimeCol = DateTimeCol()
    updatedAt: DateTimeCol = DateTimeCol()

    personCardNumberIndex: DatabaseIndex = DatabaseIndex(
        person, cardNumber, unique=True
    )

    @property
    def ownerID(self):
        return self.person.gID

    @property
    def visualID(self):
        return f"{self.gID}, ...{self.cardNumber[-4:]}, {self.expirationDate.strftime('%m/%y')}, {self.person.gID}"

    def _set_gID(self, value):
        if value:
            if validGID(value, self._gIDPrefix):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(TypeID(self._gIDPrefix))
