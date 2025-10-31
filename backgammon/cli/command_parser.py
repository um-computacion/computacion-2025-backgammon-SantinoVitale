"""
CommandParser class for Backgammon game.
Responsible only for parsing and routing user commands.
"""

from typing import Tuple, Union, Optional


class CommandParser:
    """
    Handles command parsing and routing for Backgammon CLI.

    Single Responsibility: Only handles parsing user input into commands.
    """

    SPECIAL_COMMANDS = [
        "ayuda",
        "reglas",
        "salir",
        "movimientos",
        "help",
        "rules",
        "quit",
        "moves",
    ]

    def __init__(self) -> None:
        """Initialize the CommandParser."""

    def parse_move_input(
        self, move_input: str
    ) -> Tuple[Union[int, str], Optional[Union[int, str]]]:
        """
        Parse user move input string.

        Args:
            move_input: Raw user input string

        Returns:
            Tuple of (from_position, to_position) or (command, None) for special commands

        Raises:
            ValueError: If input format is invalid
        """
        move_input = move_input.strip()

        if move_input.lower() in self.SPECIAL_COMMANDS:
            return move_input.lower(), None

        parts = move_input.split()

        if len(parts) != 2:
            raise ValueError(
                "Formato inválido. Necesita especificar posición DESDE y posición HASTA."
            )

        from_pos, to_pos = parts

        from_pos = self._normalize_position(from_pos)
        to_pos = self._normalize_position(to_pos)

        return from_pos, to_pos

    def _normalize_position(self, position: str) -> Union[int, str]:
        """
        Normalize a position string to standard format.

        Args:
            position: Position string from user

        Returns:
            Normalized position (int for points, str for bar/off)
        """
        if position.lower() == "barra":
            return "bar"
        if position.lower() == "fuera":
            return "off"
        if position.isdigit():
            return int(position)
        return position

    def is_special_command(self, command: str) -> bool:
        """
        Check if a command is a special command.

        Args:
            command: Command to check

        Returns:
            True if special command, False otherwise
        """
        return command.lower() in self.SPECIAL_COMMANDS

    def get_command_type(self, command: str) -> str:
        """
        Get the type of a special command.

        Args:
            command: Command string

        Returns:
            Command type: 'help', 'rules', 'quit', 'moves', or 'unknown'
        """
        command_lower = command.lower()

        if command_lower in ["help", "ayuda"]:
            return "help"
        if command_lower in ["rules", "reglas"]:
            return "rules"
        if command_lower in ["quit", "salir"]:
            return "quit"
        if command_lower in ["moves", "movimientos"]:
            return "moves"

        return "unknown"
