from calendar import monthrange
from datetime import date, datetime
import logging

import faker

from sqlobject import DateCol, DateTimeCol, JSONCol, RelatedJoin, StringCol  # type: ignore
import sqlobject.sqlbuilder  # type: ignore

from test_db._full_sqlobject import FullSQLObject


logger = logging.getLogger(__name__)


fake = faker.Faker()


def fake_credit_card_expire_to_date() -> date:
    """Generates a future expiration date for a credit/debit card"""
    fake_credit_card_expire = fake.credit_card_expire()
    expire_date = datetime.strptime(fake_credit_card_expire, "%m/%y").date()
    _, num_days = monthrange(expire_date.year, expire_date.month)
    return expire_date.replace(day=num_days)


class DebitCard(FullSQLObject):
    """DebitCard SQLObject

    Attributes:
        gID (StringCol): global ID for the object
        attributes (JSONCol): JSON attributes for the object
                              Note: the DB isn't updated until the object is saved
                                    (no DB updates when individual fields are changed)
        description (StringCol): description of the object
        cardNumber (StringCol): debit card number (generated when not provided)
        cvv (StringCol): debit card security code (generated when not provided)
        expirationDate (DateCol): four digit year (generated when not provided)
        organizations (RelatedJoin): list of employers related to the debit card
        people (RelatedJoin): list of people related to the debit card
        createdAt (DateTimeCol): creation date
        updatedAt (DateTimeCol): last updated date
    """

    _gIDPrefix: str = "dc"

    gID: StringCol = StringCol(alternateID=True, default=None)
    attributes: JSONCol = JSONCol(default=None)
    description: StringCol = StringCol(default=None)

    # Note: cardNumber cannot be an alternateId because many test environments
    # have a limited set of card numbers that may be used, requiring duplicate entries
    cardNumber: StringCol = StringCol(length=16, default=fake.credit_card_number)
    cvv: StringCol = StringCol(length=3, default=fake.credit_card_security_code)
    expirationDate: DateCol = DateCol(default=fake_credit_card_expire_to_date)

    organizations: RelatedJoin = RelatedJoin("Organization")
    people: RelatedJoin = RelatedJoin("Person")

    createdAt: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )
    updatedAt: DateTimeCol = DateTimeCol(
        default=sqlobject.sqlbuilder.func.strftime("%Y-%m-%d %H:%M:%f", "now")
    )

    def _set_gID(self, value):
        if value:
            if self.validGID(value):
                self._SO_set_gID(value)
            else:
                raise ValueError(f"Invalid gID value: {value}")
        else:
            self._SO_set_gID(self._generateGID())
