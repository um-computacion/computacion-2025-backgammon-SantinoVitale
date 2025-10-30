"""
CLI package for Backgammon game.

This package contains the command-line interface implementation
that uses BackgammonGame for game logic.

The package follows SOLID principles with specialized classes:
- BackgammonCLI: Main coordinator
- BoardRenderer: Board visualization
- CommandParser: Command parsing
- InputValidator: Input validation
- GameController: Game state management
- UserInterface: User I/O operations
- CLI: Legacy class (for backwards compatibility)
"""

from .backgammon_cli import BackgammonCLI
from .board_renderer import BoardRenderer
from .command_parser import CommandParser
from .input_validator import InputValidator
from .game_controller import GameController
from .user_interface import UserInterface

__all__ = [
    "BackgammonCLI",
    "BoardRenderer",
    "CommandParser",
    "InputValidator",
    "GameController",
    "UserInterface",
]
