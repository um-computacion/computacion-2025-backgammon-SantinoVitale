"""
InputValidator class for Backgammon game.
Responsible only for validating user inputs.
"""

from typing import Union


class InputValidator:
    """
    Handles input validation for Backgammon CLI.

    Single Responsibility: Only handles validation of user inputs.
    """

    def __init__(self) -> None:
        """Initialize the InputValidator."""

    def validate_position(self, position: Union[int, str]) -> bool:
        """
        Validate if a position is in valid format.

        Args:
            position: Position to validate

        Returns:
            True if valid, False otherwise
        """
        if isinstance(position, int):
            return 1 <= position <= 24
        if isinstance(position, str):
            return position.lower() in ["bar", "off", "barra", "fuera"]
        return False

    def validate_numeric_position(self, position: str) -> bool:
        """
        Validate if a string represents a valid numeric position.

        Args:
            position: String to validate

        Returns:
            True if valid numeric position, False otherwise
        """
        try:
            pos = int(position)
            return 1 <= pos <= 24
        except ValueError:
            return False

    def validate_confirmation(self, response: str) -> bool:
        """
        Validate if a user response is affirmative.

        Args:
            response: User response string

        Returns:
            True if affirmative, False otherwise
        """
        return response.strip().lower() in ["s", "sí", "si", "y", "yes"]

    def validate_move_format(self, move_input: str) -> bool:
        """
        Validate if move input has correct format.

        Args:
            move_input: Raw move input string

        Returns:
            True if format is valid, False otherwise
        """
        parts = move_input.strip().split()
        return len(parts) == 2
