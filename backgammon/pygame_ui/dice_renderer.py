"""
Dice renderer for Backgammon game.
Responsible for rendering dice with proper pip positions.
"""

from typing import Tuple, List
import pygame
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.board_dimensions import BoardDimensions


class DiceRenderer:
    """
    Renders dice on the Backgammon board.

    This class is responsible for drawing dice with the correct number
    of pips (dots) to show the current roll.

    Attributes:
        colors: ColorScheme instance for color definitions
        dimensions: BoardDimensions instance for layout calculations
        dice_size: Size of each die in pixels
    """

    def __init__(self, colors: ColorScheme, dimensions: BoardDimensions) -> None:
        """
        Initialize the DiceRenderer.

        Args:
            colors: ColorScheme instance
            dimensions: BoardDimensions instance
        """
        self.colors: ColorScheme = colors
        self.dimensions: BoardDimensions = dimensions
        self.dice_size: int = 40  # Size of each die

    def _get_pip_positions(self, value: int) -> List[Tuple[float, float]]:
        """
        Get the positions of pips for a given dice value.

        Args:
            value: Dice value (1-6)

        Returns:
            List of (x, y) tuples representing pip positions (0-1 normalized)
        """
        # Pip positions are normalized (0-1) relative to dice size
        # Center is at (0.5, 0.5)
        positions = {
            1: [(0.5, 0.5)],  # Center
            2: [(0.25, 0.25), (0.75, 0.75)],  # Diagonal
            3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],  # Diagonal with center
            4: [
                (0.25, 0.25),
                (0.75, 0.25),
                (0.25, 0.75),
                (0.75, 0.75),
            ],  # Corners
            5: [
                (0.25, 0.25),
                (0.75, 0.25),
                (0.5, 0.5),
                (0.25, 0.75),
                (0.75, 0.75),
            ],  # Corners + center
            6: [
                (0.25, 0.25),
                (0.75, 0.25),
                (0.25, 0.5),
                (0.75, 0.5),
                (0.25, 0.75),
                (0.75, 0.75),
            ],  # Two columns
        }
        return positions.get(value, [])

    def _render_die(
        self, surface: pygame.Surface, position: Tuple[int, int], value: int
    ) -> None:
        """
        Render a single die at the specified position.

        Args:
            surface: Pygame surface to draw on
            position: (x, y) tuple for top-left corner of die
            value: Dice value (1-6)
        """
        x, y = position

        # Draw die background (white square with rounded corners)
        die_rect = pygame.Rect(x, y, self.dice_size, self.dice_size)
        pygame.draw.rect(surface, (255, 255, 255), die_rect, border_radius=5)

        # Draw die border
        pygame.draw.rect(surface, (0, 0, 0), die_rect, 2, border_radius=5)

        # Draw pips
        pip_positions = self._get_pip_positions(value)
        pip_radius = self.dice_size // 8

        for pip_x, pip_y in pip_positions:
            # Convert normalized position to actual pixels
            actual_x = int(x + pip_x * self.dice_size)
            actual_y = int(y + pip_y * self.dice_size)

            # Draw pip (black circle)
            pygame.draw.circle(surface, (0, 0, 0), (actual_x, actual_y), pip_radius)

    def render_dice(
        self, surface: pygame.Surface, dice_values: List[int], position: Tuple[int, int]
    ) -> None:
        """
        Render multiple dice at the specified position.

        Args:
            surface: Pygame surface to draw on
            dice_values: List of dice values to render
            position: (x, y) tuple for starting position
        """
        x, y = position
        spacing = 10  # Space between dice

        for i, value in enumerate(dice_values):
            die_x = x + i * (self.dice_size + spacing)
            self._render_die(surface, (die_x, y), value)

    def render_dice_in_panel(
        self, surface: pygame.Surface, dice_values: List[int]
    ) -> None:
        """
        Render dice in the side panel area.

        Args:
            surface: Pygame surface to draw on
            dice_values: List of dice values to render
        """
        if not dice_values:
            return

        # Get side panel rect
        panel_rect = self.dimensions.get_side_panel_rect()

        # Calculate center position in top section of panel
        section_height = panel_rect[3] // 3
        center_x = panel_rect[0] + (panel_rect[2] // 2)
        center_y = panel_rect[1] + (section_height // 2)

        # Calculate starting position to center the dice
        total_width = len(dice_values) * self.dice_size + (len(dice_values) - 1) * 10
        start_x = center_x - (total_width // 2)
        start_y = center_y - (self.dice_size // 2)

        self.render_dice(surface, dice_values, (start_x, start_y))

    def render_available_moves(
        self, surface: pygame.Surface, available_moves: List[int]
    ) -> None:
        """
        Render available moves as small dice below the main dice.

        Args:
            surface: Pygame surface to draw on
            available_moves: List of available move values
        """
        if not available_moves:
            return

        # Get side panel rect
        panel_rect = self.dimensions.get_side_panel_rect()

        # Position below main dice
        section_height = panel_rect[3] // 3
        center_x = panel_rect[0] + (panel_rect[2] // 2)
        start_y = panel_rect[1] + (section_height // 2) + 60

        # Save original dice size and use smaller size for available moves
        original_size = self.dice_size
        self.dice_size = 25

        # Calculate starting position
        total_width = len(available_moves) * self.dice_size + (len(available_moves) - 1) * 5
        start_x = center_x - (total_width // 2)

        self.render_dice(surface, available_moves, (start_x, start_y))

        # Restore original size
        self.dice_size = original_size
