"""
Bar renderer for Backgammon board.
Responsible for rendering the central bar that divides the board.
"""

import pygame
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.board_dimensions import BoardDimensions


class BarRenderer:
    """
    Renders the central bar on the Backgammon board.

    Attributes:
        colors: ColorScheme instance for color definitions
        dimensions: BoardDimensions instance for layout calculations
    """

    def __init__(self, colors: ColorScheme, dimensions: BoardDimensions) -> None:
        """
        Initialize the BarRenderer.

        Args:
            colors: ColorScheme instance
            dimensions: BoardDimensions instance
        """
        self.colors: ColorScheme = colors
        self.dimensions: BoardDimensions = dimensions

    def _render_wood_texture(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """
        Render a simple wood texture pattern on the bar.

        Args:
            surface: Pygame surface to draw on
            rect: Rectangle defining the bar area
        """
        # Draw base green color
        pygame.draw.rect(surface, self.colors.GREEN_BAR, rect)

        # Add subtle wood grain lines
        for i in range(0, rect.height, 20):
            line_color = (
                self.colors.GREEN_BAR[0] - 10,
                self.colors.GREEN_BAR[1] - 10,
                self.colors.GREEN_BAR[2] - 10,
            )
            pygame.draw.line(
                surface,
                line_color,
                (rect.x + 5, rect.y + i),
                (rect.x + rect.width - 5, rect.y + i),
                1,
            )

    def _render_hinges(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """
        Render brass hinges on the bar (top and bottom).

        Args:
            surface: Pygame surface to draw on
            rect: Rectangle defining the bar area
        """
        hinge_height = 30
        hinge_margin = 15

        # Top hinge
        top_hinge_rect = pygame.Rect(
            rect.x + 5, rect.y + hinge_margin, rect.width - 10, hinge_height
        )
        pygame.draw.rect(surface, self.colors.BRASS, top_hinge_rect)
        pygame.draw.rect(surface, self.colors.BLACK, top_hinge_rect, 2)

        # Add screws (small circles)
        screw_radius = 3
        pygame.draw.circle(
            surface,
            self.colors.BLACK,
            (rect.x + 15, rect.y + hinge_margin + 10),
            screw_radius,
        )
        pygame.draw.circle(
            surface,
            self.colors.BLACK,
            (rect.x + rect.width - 15, rect.y + hinge_margin + 10),
            screw_radius,
        )

        # Bottom hinge
        bottom_hinge_rect = pygame.Rect(
            rect.x + 5,
            rect.y + rect.height - hinge_margin - hinge_height,
            rect.width - 10,
            hinge_height,
        )
        pygame.draw.rect(surface, self.colors.BRASS, bottom_hinge_rect)
        pygame.draw.rect(surface, self.colors.BLACK, bottom_hinge_rect, 2)

        # Add screws
        pygame.draw.circle(
            surface,
            self.colors.BLACK,
            (rect.x + 15, rect.y + rect.height - hinge_margin - 20),
            screw_radius,
        )
        pygame.draw.circle(
            surface,
            self.colors.BLACK,
            (rect.x + rect.width - 15, rect.y + rect.height - hinge_margin - 20),
            screw_radius,
        )

    def render(self, surface: pygame.Surface) -> None:
        """
        Render the complete central bar with texture and hinges.

        Args:
            surface: Pygame surface to draw on
        """
        bar_rect_tuple = self.dimensions.get_bar_rect()
        bar_rect = pygame.Rect(bar_rect_tuple)

        # Render wood texture
        self._render_wood_texture(surface, bar_rect)

        # Render hinges
        self._render_hinges(surface, bar_rect)

        # Draw border
        pygame.draw.rect(surface, self.colors.BLACK, bar_rect, 2)
