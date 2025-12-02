import logging

from typing_extensions import List, Union

from sqlobject import SQLObject  # type: ignore

from test_db import Address, Organization, Person
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class AddressView(BaseView):
    """Address views

    Args:
        address (Address): The address to view
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def add(self, entity: Union[Organization, Person, None] = None) -> Address:
        """Add an address

        Args:
            entity (Union[Organization, Person, None]): The entity of the address

        Returns:
            Address: The created address
        """
        address = Address()
        if entity:
            entity.addAddress(address)
        if BaseView.interactive:
            AddressView(address).edit()
        print(address.gID)
        return address

    @classmethod
    def list(cls, addresses: Union[List[Address], SQLObject.select, None] = None):
        """List all organizations"""
        if addresses is None:
            addresses = Address.select()
        for address in addresses:
            AddressView(address).view()

    def __init__(self, address: Address, **kwargs):
        super().__init__(**kwargs)
        self._address = address

    def edit(self):
        """Edit the address"""
        if not BaseView.interactive:
            return
        self._address.description = self._getStrInput(
            "Description", self._address.description
        )
        self._address.street = self._getStrInput("Street", self._address.street)
        self._address.locality = self._getStrInput("Locality", self._address.locality)
        self._address.region = self._getStrInput("Region", self._address.region)
        self._address.postalCode = self._getStrInput(
            "Postal Code", self._address.postalCode
        )
        self._address.country = self._getStrInput("Country", self._address.country)

    def view(self):
        """Display brief details of the address"""
        print(
            f"{self._address.gID}, {self._address.street}, {self._address.postalCode}, {str(self._address.description)[:10]}"
        )

    def viewDetails(self):
        """Display the person"""
        print(f"\nAddress ID: {self._address.gID}")
        print(f"\n{self._address.street}")
        print(
            f"{self._address.locality}, {self._address.region} {self._address.postalCode}"
        )
        print(self._address.country)
        print(f"\nDescription: {str(self._address.description)[:10]}")
