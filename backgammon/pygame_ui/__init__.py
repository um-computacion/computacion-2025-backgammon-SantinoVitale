"""
Pygame UI module for Backgammon game.
"""

from backgammon.pygame_ui.pygame_ui import PygameUI
from backgammon.pygame_ui.backgammon_board import BackgammonBoard
from backgammon.pygame_ui.board_interaction import BoardInteraction
from backgammon.pygame_ui.button import Button
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.board_dimensions import BoardDimensions
from backgammon.pygame_ui.click_detector import ClickDetector

__all__ = [
    "PygameUI",
    "BackgammonBoard",
    "BoardInteraction",
    "Button",
    "ColorScheme",
    "BoardDimensions",
    "ClickDetector",
]
