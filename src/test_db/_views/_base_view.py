import datetime
import logging

from typing_extensions import Optional

logger = logging.getLogger(__name__)


class BaseView:
    interactive: bool = True

    def __init__(self, **kwargs):
        self._user_inputs_required = kwargs.get("user_inputs_required")
        if self._user_inputs_required is None:
            self._user_inputs_required = True

    @staticmethod
    def _get_date_input(
        prompt: str, default: Optional[str] = None
    ) -> datetime.datetime:
        while True:
            date_input = BaseView._get_input(f"{prompt} MM/DD/YYYY", default)
            try:
                return datetime.datetime.strptime(date_input, "%m/%d/%Y")
            except ValueError:
                logger.error("bad date - MM-DD-YYYY required")

    @staticmethod
    def _get_str_input(
        prompt: str, default: Optional[str] = None, numeric: Optional[bool] = False
    ) -> str:
        while True:
            string_input = BaseView._get_input(prompt, default)
            if numeric:
                try:
                    int(string_input)
                except ValueError:
                    logger.error("string input must be numeric")
            try:
                return str(string_input)
            except ValueError:
                logger.error("invalid string input")

    @staticmethod
    def _get_input(prompt: str, default: Optional[str] = None) -> str:
        while True:
            if default:
                value = input(f"{prompt} ({default}): ") or default
            else:
                value = input(f"{prompt}: ")
            if value:
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

    def view(self):
        """Display the person"""
        pass

    def viewDetails(self):
        """Display the person"""
        self.view()
