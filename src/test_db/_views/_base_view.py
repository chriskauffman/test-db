import datetime
import logging

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Optional

logger = logging.getLogger(__name__)


class BaseView:
    @staticmethod
    def _getDateInput(prompt: str, default: Optional[str] = None) -> datetime.datetime:
        while True:
            date_input = BaseView._getInput(f"{prompt} MM/DD/YYYY", default)
            try:
                return datetime.datetime.strptime(date_input, "%m/%d/%Y")
            except ValueError:
                logger.error("bad date - MM-DD-YYYY required")

    @staticmethod
    def _getStrInput(
        prompt: str,
        default: Optional[str] = None,
        numeric: Optional[bool] = False,
        acceptNull: Optional[bool] = False,
    ) -> str:
        while True:
            string_input = BaseView._getInput(prompt, default, acceptNull=acceptNull)
            if numeric:
                try:
                    int(string_input)
                except ValueError:
                    logger.error("string input must be numeric")
                    continue
            try:
                return str(string_input)
            except ValueError:
                logger.error("invalid string input")

    @staticmethod
    def _getInput(
        prompt: str, default: Optional[str] = None, acceptNull: Optional[bool] = False
    ) -> str:
        while True:
            if default:
                value = input(f"{prompt} ({default}): ") or default
            else:
                value = input(f"{prompt}: ")
            if value == "NULL":
                value = ""
            if value or acceptNull:
                return value
            else:
                print("Input is required")

    @staticmethod
    def info(message: str):
        """Info print

        Args:
            message (str): error message to display
        """
        print(message)

    @staticmethod
    def error(message: str):
        """Error print

        Args:
            message (str): error message to display
        """
        print(f"Error: {message}")

    @staticmethod
    def masked(message: str) -> str:
        """Masked print

        Args:
            message (str): message to mask

        Returns:
            str: masked message
        """
        return message

    def delete(self):
        """Delete the object"""
        pass

    def edit(self):
        """Edit the object"""
        pass

    def view(self):
        """Display the object"""
        pass

    def viewDetails(self):
        """Display the object's details"""
        self.view()
