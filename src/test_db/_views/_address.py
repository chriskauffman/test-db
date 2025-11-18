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

    _user_inputs_required: bool = True

    @classmethod
    def add(self, occupant: Union[Organization, Person, None] = None) -> Address:
        """Add an address

        Args:
            occupant (Union[Organization, Person, None]): The occupant of the address

        Returns:
            Address: The created address
        """
        address = Address()
        if occupant:
            return occupant.addAddress(address)
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
        self._address.description = self._get_str_input(
            "Description", self._address.description
        )
        self._address.street = self._get_str_input("Street", self._address.street)
        self._address.locality = self._get_str_input("Locality", self._address.locality)
        self._address.region = self._get_str_input("Region", self._address.region)
        self._address.postalCode = self._get_str_input(
            "Postal Code", self._address.postalCode
        )
        self._address.country = self._get_str_input("Country", self._address.country)

    def view(self):
        """Display brief details of the address"""
        print(
            f"{self._address.gID}, {self._address.street}, {self._address.locality}, {self._address.region} {self._address.postalCode}"
        )

    def viewDetails(self):
        """Display the person"""
        self.view()
