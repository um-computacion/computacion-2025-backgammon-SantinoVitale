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

from .BackgammonCLI import BackgammonCLI
from .BoardRenderer import BoardRenderer
from .CommandParser import CommandParser
from .InputValidator import InputValidator
from .GameController import GameController
from .UserInterface import UserInterface

__all__ = [
    "BackgammonCLI",
    "BoardRenderer",
    "CommandParser",
    "InputValidator",
    "GameController",
    "UserInterface",
]
