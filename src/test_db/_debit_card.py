from calendar import monthrange
from datetime import date, datetime
import logging

import faker

from sqlobject import DateCol, RelatedJoin, StringCol  # type: ignore

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
        cardNumber (StringCol): debit card number (generated when not provided)
        cvv (StringCol): debit card security code (generated when not provided)
        expirationDate (DateCol): four digit year (generated when not provided)
        organizations (RelatedJoin): list of employers related to the debit card
        people (RelatedJoin): list of people related to the debit card
    """

    _gIDPrefix: str = "dc"

    # Note: cardNumber cannot be an alternateId because many test environments
    # have a limited set of card numbers that may be used, requiring duplicate entries
    cardNumber: StringCol = StringCol(length=16, default=fake.credit_card_number)
    cvv: StringCol = StringCol(length=3, default=fake.credit_card_security_code)
    expirationDate: DateCol = DateCol(default=fake_credit_card_expire_to_date)

    organizations: RelatedJoin = RelatedJoin("Organization")
    people: RelatedJoin = RelatedJoin("Person")
