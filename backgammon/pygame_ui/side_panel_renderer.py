"""
Side panel renderer for Backgammon board.
Responsible for rendering the right side panel with diagonal stripes.
"""

import pygame
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.board_dimensions import BoardDimensions


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
        # Create a temporary surface for the stripes
        temp_surface = pygame.Surface((rect.width, rect.height))

        # Fill with base green
        temp_surface.fill(self.colors.GREEN_STRIPE)

        # Draw diagonal yellow stripes
        diagonal_spacing = stripe_width * 2

        # Calculate how many diagonals we need
        max_offset = rect.width + rect.height

        for offset in range(-max_offset, max_offset, diagonal_spacing):
            points = [
                (offset, 0),
                (offset + stripe_width, 0),
                (offset + stripe_width + rect.height, rect.height),
                (offset + rect.height, rect.height),
            ]
            pygame.draw.polygon(temp_surface, self.colors.YELLOW_STRIPE, points)

        # Blit the temporary surface to the main surface
        surface.blit(temp_surface, (rect.x, rect.y))

    def render(self, surface: pygame.Surface) -> None:
        """
        Render the complete side panel with diagonal stripes and wood center.

        Args:
            surface: Pygame surface to draw on
        """
        panel_rect_tuple = self.dimensions.get_side_panel_rect()
        panel_rect = pygame.Rect(panel_rect_tuple)

        # Calculate section heights
        section_height = panel_rect.height // 3

        # Top section with diagonal stripes
        top_rect = pygame.Rect(
            panel_rect.x, panel_rect.y, panel_rect.width, section_height
        )
        self._render_diagonal_stripes(surface, top_rect)

        # Middle section with wood texture
        middle_rect = pygame.Rect(
            panel_rect.x,
            panel_rect.y + section_height,
            panel_rect.width,
            section_height,
        )
        pygame.draw.rect(surface, self.colors.WOOD_ORANGE, middle_rect)

        # Bottom section with diagonal stripes
        bottom_rect = pygame.Rect(
            panel_rect.x,
            panel_rect.y + (2 * section_height),
            panel_rect.width,
            panel_rect.height - (2 * section_height),
        )
        self._render_diagonal_stripes(surface, bottom_rect)

        # Draw borders between sections
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

        # Draw outer border
        pygame.draw.rect(surface, self.colors.BLACK, panel_rect, 2)
