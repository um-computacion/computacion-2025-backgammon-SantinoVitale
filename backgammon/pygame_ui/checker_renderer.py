"""
Checker renderer for Backgammon board.
Responsible for rendering checkers (game pieces) on the board.
"""

from typing import Tuple, List
import pygame
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.board_dimensions import BoardDimensions


class CheckerRenderer:
    """
    Renders checkers (game pieces) on the Backgammon board.

    This class is responsible for drawing the circular checker pieces
    at their correct positions on the board points, bar, and off areas.

    Attributes:
        colors: ColorScheme instance for color definitions
        dimensions: BoardDimensions instance for layout calculations
        checker_radius: Radius of each checker piece in pixels
    """

    def __init__(self, colors: ColorScheme, dimensions: BoardDimensions) -> None:
        """
        Initialize the CheckerRenderer.

        Args:
            colors: ColorScheme instance
            dimensions: BoardDimensions instance
        """
        self.colors: ColorScheme = colors
        self.dimensions: BoardDimensions = dimensions

        # Calculate checker radius based on point width
        # Checkers should fit nicely within the points
        # Reduced size to prevent overlapping with larger screen
        self.checker_radius: int = (self.dimensions.point_width // 3) - 8

    def _get_checker_color(self, color: str) -> Tuple[int, int, int]:
        """
        Get the RGB color for a checker based on its color name.

        Args:
            color: Color name ('white' or 'black')

        Returns:
            RGB color tuple
        """
        if color == "white":
            return (240, 240, 240)  # Almost white
        elif color == "black":
            return (20, 20, 20)  # Almost black
        else:
            return (128, 128, 128)  # Gray as default

    def _calculate_checker_position(
        self, point_number: int, stack_index: int, total_checkers: int = 1
    ) -> Tuple[int, int]:
        """
        Calculate the center position for a checker on a specific point.

        Args:
            point_number: Point number (0-23)
            stack_index: Index of the checker in the stack (0 = bottom, 1 = second, etc.)
            total_checkers: Total number of checkers on this point (for adaptive spacing)

        Returns:
            Tuple of (x, y) coordinates for the checker center
        """
        # Get point's X position and calculate center
        point_x = self.dimensions.get_point_x(point_number)
        center_x = point_x + (self.dimensions.point_width // 2)

        # Determine if point is on top or bottom
        is_top = point_number <= 11
        base_y = self.dimensions.get_point_base_y(is_top)

        # Calculate adaptive spacing based on number of checkers
        # If there are many checkers, reduce spacing to fit them all
        base_spacing = self.checker_radius * 2 + 4  # 4 pixels gap between checkers

        # Adaptive spacing: reduce spacing if there are more than 5 checkers
        if total_checkers > 5:
            # Gradually reduce spacing for tall stacks
            max_height = self.dimensions.point_height - self.checker_radius
            available_height = max_height - self.checker_radius
            checker_spacing = min(base_spacing, available_height // total_checkers)
        else:
            checker_spacing = base_spacing

        if is_top:
            # For top points, stack downwards
            center_y = base_y + self.checker_radius + (stack_index * checker_spacing)
        else:
            # For bottom points, stack upwards
            center_y = base_y - self.checker_radius - (stack_index * checker_spacing)

        return (center_x, center_y)

    def _render_checker_with_shadow(
        self, surface: pygame.Surface, position: Tuple[int, int], color: str
    ) -> None:
        """
        Render a single checker with a shadow effect.

        Args:
            surface: Pygame surface to draw on
            position: (x, y) tuple for checker center
            color: Color of the checker ('white' or 'black')
        """
        x, y = position

        # Draw shadow (slightly offset)
        shadow_offset = 3
        pygame.draw.circle(
            surface,
            (50, 50, 50),
            (x + shadow_offset, y + shadow_offset),
            self.checker_radius,
        )

        # Draw main checker
        checker_color = self._get_checker_color(color)
        pygame.draw.circle(surface, checker_color, (x, y), self.checker_radius)

        # Draw border/outline
        border_color = (0, 0, 0) if color == "white" else (200, 200, 200)
        pygame.draw.circle(surface, border_color, (x, y), self.checker_radius, 2)

        # Add highlight for 3D effect
        highlight_color = (255, 255, 255, 150) if color == "white" else (100, 100, 100)
        highlight_offset = self.checker_radius // 3
        pygame.draw.circle(
            surface,
            highlight_color,
            (x - highlight_offset, y - highlight_offset),
            self.checker_radius // 4,
        )

    def render_checker(
        self,
        surface: pygame.Surface,
        point_number: int,
        stack_index: int,
        color: str,
        total_checkers: int = 1,
    ) -> None:
        """
        Render a single checker at a specific point and stack position.

        Args:
            surface: Pygame surface to draw on
            point_number: Point number (0-23)
            stack_index: Position in the stack (0 = bottom)
            color: Color of the checker ('white' or 'black')
            total_checkers: Total checkers on this point (for adaptive spacing)
        """
        position = self._calculate_checker_position(
            point_number, stack_index, total_checkers
        )
        self._render_checker_with_shadow(surface, position, color)

    def render_point_checkers(
        self, surface: pygame.Surface, point_number: int, checkers: List[object]
    ) -> None:
        """
        Render all checkers on a specific point.

        Args:
            surface: Pygame surface to draw on
            point_number: Point number (0-23)
            checkers: List of Checker objects on this point
        """
        total_checkers = len(checkers)
        for stack_index, checker in enumerate(checkers):
            self.render_checker(
                surface, point_number, stack_index, checker.color, total_checkers
            )

    def render_bar_checker(
        self, surface: pygame.Surface, color: str, stack_index: int
    ) -> None:
        """
        Render a checker on the bar (captured checkers).

        Args:
            surface: Pygame surface to draw on
            color: Color of the checker ('white' or 'black')
            stack_index: Position in the bar stack
        """
        bar_rect = self.dimensions.get_bar_rect()
        center_x = bar_rect[0] + (bar_rect[2] // 2)

        # Stack checkers vertically in the bar
        # White checkers on top half, black on bottom half
        if color == "white":
            base_y = bar_rect[1] + (bar_rect[3] // 4)
        else:
            base_y = bar_rect[1] + (3 * bar_rect[3] // 4)

        checker_spacing = self.checker_radius * 2 + 2
        center_y = base_y + (stack_index * checker_spacing)

        self._render_checker_with_shadow(surface, (center_x, center_y), color)

    def render_off_checker(
        self, surface: pygame.Surface, color: str, stack_index: int
    ) -> None:
        """
        Render a checker in the off area (borne off checkers).

        Args:
            surface: Pygame surface to draw on
            color: Color of the checker ('white' or 'black')
            stack_index: Position in the off stack
        """
        side_panel_rect = self.dimensions.get_side_panel_rect()

        # Calculate position in the middle section of side panel
        center_x = side_panel_rect[0] + (side_panel_rect[2] // 2)

        # White checkers on top of middle section, black on bottom
        section_height = side_panel_rect[3] // 3
        middle_section_y = side_panel_rect[1] + section_height

        if color == "white":
            base_y = middle_section_y + 20
        else:
            base_y = middle_section_y + section_height - 20

        # Stack checkers, but compact them if there are many
        max_visible_stack = 5
        if stack_index < max_visible_stack:
            checker_spacing = self.checker_radius * 2 + 2
            center_y = base_y + (stack_index * checker_spacing)
        else:
            # For checkers beyond max_visible_stack, just show the count
            center_y = base_y + (max_visible_stack * (self.checker_radius * 2 + 2))

        self._render_checker_with_shadow(surface, (center_x, center_y), color)
