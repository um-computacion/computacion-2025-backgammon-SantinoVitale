"""
Highlight renderer for Backgammon board.
Responsible for rendering visual feedback (selection highlights, valid moves).
"""

from typing import Optional, List, Tuple
import pygame
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.board_dimensions import BoardDimensions


class HighlightRenderer:
    """
    Renders visual feedback for player interactions.

    This class handles highlighting selected checkers and showing valid move destinations.

    Attributes:
        colors: ColorScheme instance for color definitions
        dimensions: BoardDimensions instance for layout calculations
    """

    def __init__(self, colors: ColorScheme, dimensions: BoardDimensions) -> None:
        """
        Initialize the HighlightRenderer.

        Args:
            colors: ColorScheme instance
            dimensions: BoardDimensions instance
        """
        self.colors: ColorScheme = colors
        self.dimensions: BoardDimensions = dimensions

        # Highlight colors
        self.SELECTED_COLOR: Tuple[int, int, int] = (255, 215, 0)  # Gold
        self.VALID_MOVE_COLOR: Tuple[int, int, int] = (50, 205, 50)  # Lime green
        self.INVALID_MOVE_COLOR: Tuple[int, int, int] = (220, 20, 60)  # Crimson

    def _get_point_center(self, point_number: int) -> Tuple[int, int]:
        """
        Get the center coordinates of a point.

        Args:
            point_number: Point number (0-23)

        Returns:
            Tuple of (x, y) coordinates for the point center
        """
        point_x = self.dimensions.get_point_x(point_number)
        center_x = point_x + (self.dimensions.point_width // 2)

        is_top = point_number <= 11
        base_y = self.dimensions.get_point_base_y(is_top)

        # Center is at the base of the triangle
        if is_top:
            center_y = base_y + 30  # Slightly down from top
        else:
            center_y = base_y - 30  # Slightly up from bottom

        return (center_x, center_y)

    def render_selected_point(
        self, surface: pygame.Surface, point_number: int, stack_index: int = 0
    ) -> None:
        """
        Render a highlight around a selected checker.

        Args:
            surface: Pygame surface to draw on
            point_number: Point number (0-23)
            stack_index: Index of the selected checker in the stack
        """
        # Calculate checker position (similar to CheckerRenderer)
        point_x = self.dimensions.get_point_x(point_number)
        center_x = point_x + (self.dimensions.point_width // 2)

        is_top = point_number <= 11
        base_y = self.dimensions.get_point_base_y(is_top)

        # Calculate checker radius (matching CheckerRenderer)
        checker_radius = (self.dimensions.point_width // 2) - 8

        # Calculate Y position for the specific checker
        checker_spacing = checker_radius * 2 + 4
        if is_top:
            center_y = base_y + checker_radius + (stack_index * checker_spacing)
        else:
            center_y = base_y - checker_radius - (stack_index * checker_spacing)

        # Draw golden ring around selected checker
        ring_thickness = 4
        pygame.draw.circle(
            surface,
            self.SELECTED_COLOR,
            (center_x, center_y),
            checker_radius + 5,
            ring_thickness,
        )

        # Draw pulsing inner circle for emphasis
        pygame.draw.circle(
            surface,
            self.SELECTED_COLOR,
            (center_x, center_y),
            checker_radius - 5,
            2,
        )

    def render_valid_move_point(
        self, surface: pygame.Surface, point_number: int
    ) -> None:
        """
        Render a highlight on a point that is a valid move destination.

        Args:
            surface: Pygame surface to draw on
            point_number: Point number (0-23)
        """
        center_x, center_y = self._get_point_center(point_number)

        # Draw green circle at the base of the point
        radius = self.dimensions.point_width // 3
        pygame.draw.circle(surface, self.VALID_MOVE_COLOR, (center_x, center_y), radius)

        # Draw border
        pygame.draw.circle(
            surface, (0, 100, 0), (center_x, center_y), radius, 3
        )  # Dark green border

    def render_bar_highlight(
        self, surface: pygame.Surface, is_selected: bool = False
    ) -> None:
        """
        Render a highlight on the bar area.

        Args:
            surface: Pygame surface to draw on
            is_selected: If True, render selection highlight; otherwise valid move highlight
        """
        bar_rect = self.dimensions.get_bar_rect()
        color = self.SELECTED_COLOR if is_selected else self.VALID_MOVE_COLOR

        # Draw semi-transparent overlay
        overlay = pygame.Surface((bar_rect[2], bar_rect[3]), pygame.SRCALPHA)
        overlay.fill((*color, 80))  # 80 is alpha (transparency)
        surface.blit(overlay, (bar_rect[0], bar_rect[1]))

        # Draw border
        pygame.draw.rect(surface, color, bar_rect, 4)

    def render_off_area_highlight(self, surface: pygame.Surface) -> None:
        """
        Render a highlight on the off area (bearing off destination).

        Args:
            surface: Pygame surface to draw on
        """
        panel_rect = self.dimensions.get_side_panel_rect()

        # Highlight the middle section (where borne off checkers appear)
        section_height = panel_rect[3] // 3
        middle_rect = (
            panel_rect[0],
            panel_rect[1] + section_height,
            panel_rect[2],
            section_height,
        )

        # Draw semi-transparent green overlay
        overlay = pygame.Surface((middle_rect[2], middle_rect[3]), pygame.SRCALPHA)
        overlay.fill((*self.VALID_MOVE_COLOR, 80))
        surface.blit(overlay, (middle_rect[0], middle_rect[1]))

        # Draw border
        pygame.draw.rect(surface, self.VALID_MOVE_COLOR, middle_rect, 4)

    def render_valid_moves(
        self,
        surface: pygame.Surface,
        destinations: List[int],
    ) -> None:
        """
        Render highlights for all valid move destinations.

        Args:
            surface: Pygame surface to draw on
            destinations: List of valid destination point numbers
        """
        for dest in destinations:
            if isinstance(dest, int) and 0 <= dest <= 23:
                self.render_valid_move_point(surface, dest)
            elif dest == "off":
                self.render_off_area_highlight(surface)

    def render_invalid_selection(
        self, surface: pygame.Surface, point_number: int
    ) -> None:
        """
        Render a visual indicator that the selected point has no valid moves.

        Args:
            surface: Pygame surface to draw on
            point_number: Point number (0-23)
        """
        center_x, center_y = self._get_point_center(point_number)

        # Draw red X
        size = 20
        pygame.draw.line(
            surface,
            self.INVALID_MOVE_COLOR,
            (center_x - size, center_y - size),
            (center_x + size, center_y + size),
            4,
        )
        pygame.draw.line(
            surface,
            self.INVALID_MOVE_COLOR,
            (center_x + size, center_y - size),
            (center_x - size, center_y + size),
            4,
        )
