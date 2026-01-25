import logging

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import List, Union

from sqlobject import SQLObject  # type: ignore
from sqlobject.dberrors import DuplicateEntryError  # type: ignore

from test_db import OrganizationAddress, PersonAddress
from test_db._views._base_view import BaseView

logger = logging.getLogger(__name__)


class AddressView(BaseView):
    """Address views

    Args:
        address (Union[OrganizationAddress, PersonAddress]): The address to view
        **kwargs:
            - user_inputs_required (bool):
    """

    @classmethod
    def list(
        cls,
        addresses: Union[
            List[OrganizationAddress], List[PersonAddress], SQLObject.select
        ],
        **kwargs,
    ):
        """List all addresses"""
        for address in addresses:
            AddressView(address).view()

    def __init__(self, address: Union[OrganizationAddress, PersonAddress], **kwargs):
        super().__init__(**kwargs)
        self._address = address

    def delete(self, interactive: bool = True):
        """Delete the address"""
        if (
            interactive
            and input(f"Delete {self._address.visualID}? [y/n] ").strip().lower() != "y"
        ):
            return
        self._address.destroySelf()

    def edit(self):
        """Edit the address"""
        while True:
            try:
                self._address.gID = self._getTypeIDInput("gID", self._address.gID)
                break
            except DuplicateEntryError:
                print("gID already exists. Please enter a different gID.")
            except ValueError:
                print("Invalid gID. Check prefix and suffix. Please try again.")

        self._address.description = self._getStrInput(
            "Description", self._address.description, acceptNull=True
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
        print(f"{self._address.visualID}")

    def viewDetails(self):
        """Display the address's details"""
        print(f"\nAddress ID: {self._address.gID}")
        print(f"Owner ID:   {self._address.ownerID}")
        print(f"\n{self._address.street}")
        print(
            f"{self._address.locality}, {self._address.region} {self._address.postalCode}"
        )
        print(self._address.country)
        print(f"\nDescription: {str(self._address.description)[:10]}")
        print(f"\nCreated At:\t{self._address.createdAt}")
        print(f"Updated At:\t{self._address.updatedAt}")
