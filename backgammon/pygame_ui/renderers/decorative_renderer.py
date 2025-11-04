"""
Decorative renderer for Backgammon board.
Consolidates rendering of decorative elements: bar and side panel.
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
        pygame.draw.rect(surface, self.colors.GREEN_BAR, rect)

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

        top_hinge_rect = pygame.Rect(
            rect.x + 5, rect.y + hinge_margin, rect.width - 10, hinge_height
        )
        pygame.draw.rect(surface, self.colors.BRASS, top_hinge_rect)
        pygame.draw.rect(surface, self.colors.BLACK, top_hinge_rect, 2)

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

        bottom_hinge_rect = pygame.Rect(
            rect.x + 5,
            rect.y + rect.height - hinge_margin - hinge_height,
            rect.width - 10,
            hinge_height,
        )
        pygame.draw.rect(surface, self.colors.BRASS, bottom_hinge_rect)
        pygame.draw.rect(surface, self.colors.BLACK, bottom_hinge_rect, 2)

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

        self._render_wood_texture(surface, bar_rect)
        self._render_hinges(surface, bar_rect)
        pygame.draw.rect(surface, self.colors.BLACK, bar_rect, 2)


class SidePanelRenderer:
    """
    Renders the right side panel on the Backgammon board.

    Attributes:
        colors: ColorScheme instance for color definitions
        dimensions: BoardDimensions instance for layout calculations
    """

    def __init__(self, colors: ColorScheme, dimensions: BoardDimensions) -> None:
        """
        Initialize the SidePanelRenderer.

        Args:
            colors: ColorScheme instance
            dimensions: BoardDimensions instance
        """
        self.colors: ColorScheme = colors
        self.dimensions: BoardDimensions = dimensions

    def _render_diagonal_stripes(
        self, surface: pygame.Surface, rect: pygame.Rect, stripe_width: int = 10
    ) -> None:
        """
        Render diagonal green and yellow stripes.

        Args:
            surface: Pygame surface to draw on
            rect: Rectangle defining the stripe area
            stripe_width: Width of each stripe
        """
        temp_surface = pygame.Surface((rect.width, rect.height))
        temp_surface.fill(self.colors.GREEN_STRIPE)

        diagonal_spacing = stripe_width * 2
        max_offset = rect.width + rect.height

        for offset in range(-max_offset, max_offset, diagonal_spacing):
            points = [
                (offset, 0),
                (offset + stripe_width, 0),
                (offset + stripe_width + rect.height, rect.height),
                (offset + rect.height, rect.height),
            ]
            pygame.draw.polygon(temp_surface, self.colors.YELLOW_STRIPE, points)

        surface.blit(temp_surface, (rect.x, rect.y))

    def render(self, surface: pygame.Surface) -> None:
        """
        Render the complete side panel with diagonal stripes and wood center.

        Args:
            surface: Pygame surface to draw on
        """
        panel_rect_tuple = self.dimensions.get_side_panel_rect()
        panel_rect = pygame.Rect(panel_rect_tuple)

        section_height = panel_rect.height // 3

        top_rect = pygame.Rect(
            panel_rect.x, panel_rect.y, panel_rect.width, section_height
        )
        self._render_diagonal_stripes(surface, top_rect)

        middle_rect = pygame.Rect(
            panel_rect.x,
            panel_rect.y + section_height,
            panel_rect.width,
            section_height,
        )
        pygame.draw.rect(surface, self.colors.WOOD_ORANGE, middle_rect)

        bottom_rect = pygame.Rect(
            panel_rect.x,
            panel_rect.y + (2 * section_height),
            panel_rect.width,
            panel_rect.height - (2 * section_height),
        )
        self._render_diagonal_stripes(surface, bottom_rect)

        pygame.draw.line(
            surface,
            self.colors.BLACK,
            (panel_rect.x, panel_rect.y + section_height),
            (panel_rect.x + panel_rect.width, panel_rect.y + section_height),
            2,
        )
        pygame.draw.line(
            surface,
            self.colors.BLACK,
            (panel_rect.x, panel_rect.y + (2 * section_height)),
            (panel_rect.x + panel_rect.width, panel_rect.y + (2 * section_height)),
            2,
        )

        pygame.draw.rect(surface, self.colors.BLACK, panel_rect, 2)
