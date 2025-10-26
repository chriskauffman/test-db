import logging

from test_db import DebitCard
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class DebitCardView(BaseView):
    """Debit card views

    Args:
        debit_card (DebitCard):
        **kwargs:
            - user_inputs_required (bool):
    """

    _user_inputs_required: bool = True

    @classmethod
    def list(cls):
        """List all people"""
        for debit_card in DebitCard.select():
            DebitCardView(debit_card).view()

    def __init__(self, debit_card: DebitCard, **kwargs):
        super().__init__(**kwargs)
        self._debit_card = debit_card

    def view(self):
        """Display brief details of the debit card"""
        print(
            f"{self._debit_card.description}, "
            f"{self._debit_card.cardNumber}, "
            f"{self._debit_card.cvv}, "
            f"{self._debit_card.expirationDate.strftime('%m/%y')}"
        )
