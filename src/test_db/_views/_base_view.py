import logging

from typing_extensions import Optional

logger = logging.getLogger(__name__)


class BaseView:
    def __init__(self, **kwargs):
        self._user_inputs_required = kwargs.get("user_inputs_required")
        if self._user_inputs_required is None:
            self._user_inputs_required = True

    @staticmethod
    def _get_input(
        prompt: str, expected_type: type, default: Optional[str] = None
    ) -> str:
        while True:
            try:
                if default:
                    value = str(input(f"{prompt} ({default}): ") or default)
                else:
                    value = str(input(f"{prompt}: "))
                if value and isinstance(value, expected_type):
                    return value
                else:
                    print("Input is required")
            except ValueError:
                print("Invalid input type, try again")

    @staticmethod
    def info(message: str):
        """Info print

        Args:
            message (str): error message to display"""
        print(message)

    @staticmethod
    def error(message: str):
        """Error print

        Args:
            message (str): error message to display"""
        print(f"Error: {message}")
