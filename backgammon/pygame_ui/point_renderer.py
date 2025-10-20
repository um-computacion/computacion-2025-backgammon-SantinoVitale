"""
Point renderer for Backgammon board.
Responsible for rendering the triangular points on the board.
"""

from typing import List, Tuple
import pygame
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.board_dimensions import BoardDimensions


class PointRenderer:
    """
    Renders triangular points on the Backgammon board.

    Attributes:
        colors: ColorScheme instance for color definitions
        dimensions: BoardDimensions instance for layout calculations
    """

    def __init__(self, colors: ColorScheme, dimensions: BoardDimensions) -> None:
        """
        Initialize the PointRenderer.

        Args:
            colors: ColorScheme instance
            dimensions: BoardDimensions instance
        """
        self.colors: ColorScheme = colors
        self.dimensions: BoardDimensions = dimensions

    def _get_point_color(self, point_number: int) -> Tuple[int, int, int]:
        """
        Get the color for a specific point based on alternating pattern.

        Args:
            point_number: Point number (0-23)

        Returns:
            RGB color tuple
        """
        if point_number % 2 == 0:
            return self.colors.DARK_BROWN_POINT
        else:
            return self.colors.LIGHT_BEIGE

    def _calculate_triangle_points(self, point_number: int) -> List[Tuple[int, int]]:
        """
        Calculate the vertices of a triangular point.

        Args:
            point_number: Point number (0-23)

        Returns:
            List of three (x, y) tuples representing triangle vertices
        """
        x = self.dimensions.get_point_x(point_number)
        width = self.dimensions.point_width
        height = self.dimensions.point_height

        # Determine if point is on top or bottom
        is_top = point_number <= 11
        base_y = self.dimensions.get_point_base_y(is_top)

        if is_top:
            # Triangle points downward
            tip_y = base_y + height
            return [
                (x, base_y),  # Top left
                (x + width, base_y),  # Top right
                (x + width // 2, tip_y),  # Bottom center (tip)
            ]
        else:
            # Triangle points upward
            tip_y = base_y - height
            return [
                (x, base_y),  # Bottom left
                (x + width, base_y),  # Bottom right
                (x + width // 2, tip_y),  # Top center (tip)
            ]

    def render_point(self, surface: pygame.Surface, point_number: int) -> None:
        """
        Render a single triangular point.

        Args:
            surface: Pygame surface to draw on
            point_number: Point number (0-23)
        """
        color = self._get_point_color(point_number)
        points = self._calculate_triangle_points(point_number)
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, self.colors.BLACK, points, 1)

    def render_all_points(self, surface: pygame.Surface) -> None:
        """
        Render all 24 triangular points on the board.

        Args:
            surface: Pygame surface to draw on
        """
        for point_number in range(24):
            self.render_point(surface, point_number)
