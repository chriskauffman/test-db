import logging

from typing_extensions import List, Union

from sqlobject import SQLObject  # type: ignore

from test_db import DebitCard, Organization, Person
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class DebitCardView(BaseView):
    """Debit card views

    Args:
        debit_card (DebitCard):
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def add(self, entity: Union[Organization, Person, None] = None) -> DebitCard:
        """Add a debit card"""
        debit_card = DebitCard()
        if entity:
            debit_card.addEntity(entity)
        if BaseView.interactive:
            DebitCardView(debit_card).edit()
        print(debit_card.gID)
        return debit_card

    @classmethod
    def list(cls, debit_cards: Union[List[DebitCard], SQLObject.select, None] = None):
        """List all people"""
        if debit_cards is None:
            debit_cards = DebitCard.select()
        for debit_card in debit_cards:
            DebitCardView(debit_card).view()

    def __init__(self, debit_card: DebitCard, **kwargs):
        super().__init__(**kwargs)
        self._debit_card = debit_card

    def edit(self):
        """Edit the debit card"""
        self._debit_card.description = self._getStrInput(
            "Description", self._debit_card.description, acceptNull=True
        )
        self._debit_card.cardNumber = self._getStrInput(
            "Card Number", self._debit_card.cardNumber, numeric=True
        )
        self._debit_card.cvv = self._getStrInput(
            "CVV", self._debit_card.cvv, numeric=True
        )
        self._debit_card.expirationDate = self._getDateInput(
            "Expiration Date",
            self._debit_card.expirationDate.strftime("%m/%d/%Y"),
        )

    def view(self):
        """Display brief details of the debit card"""
        print(
            f"{self._debit_card.gID}, "
            f"{self._debit_card.cardNumber}, "
            f"{self._debit_card.cvv}, "
            f"{self._debit_card.expirationDate.strftime('%m/%y')}, "
            f"{str(self._debit_card.description)[:10]}"
        )
