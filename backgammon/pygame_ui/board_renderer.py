"""
Board renderer for Backgammon board.
Responsible for rendering the main board structure and coordinating other renderers.
"""

import pygame
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.board_dimensions import BoardDimensions
from backgammon.pygame_ui.point_renderer import PointRenderer
from backgammon.pygame_ui.bar_renderer import BarRenderer
from backgammon.pygame_ui.side_panel_renderer import SidePanelRenderer


class BoardRenderer:
    """
    Main board renderer that coordinates all board component rendering.

    Attributes:
        colors: ColorScheme instance for color definitions
        dimensions: BoardDimensions instance for layout calculations
        point_renderer: PointRenderer for rendering points
        bar_renderer: BarRenderer for rendering central bar
        side_panel_renderer: SidePanelRenderer for rendering side panel
    """

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """
        Initialize the BoardRenderer.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.colors: ColorScheme = ColorScheme()
        self.dimensions: BoardDimensions = BoardDimensions(screen_width, screen_height)

        # Initialize component renderers
        self.point_renderer: PointRenderer = PointRenderer(self.colors, self.dimensions)
        self.bar_renderer: BarRenderer = BarRenderer(self.colors, self.dimensions)
        self.side_panel_renderer: SidePanelRenderer = SidePanelRenderer(
            self.colors, self.dimensions
        )

    def _render_board_background(self, surface: pygame.Surface) -> None:
        """
        Render the board background with border.

        Args:
            surface: Pygame surface to draw on
        """
        # Draw outer border (dark brown)
        outer_rect = pygame.Rect(self.dimensions.get_board_rect())
        pygame.draw.rect(surface, self.colors.DARK_BROWN, outer_rect)

        # Draw inner board (wood texture)
        inner_rect = pygame.Rect(self.dimensions.get_inner_board_rect())
        pygame.draw.rect(surface, self.colors.WOOD_ORANGE, inner_rect)

    def render(self, surface: pygame.Surface) -> None:
        """
        Render the complete Backgammon board.

        Args:
            surface: Pygame surface to draw on
        """
        # Render background
        self._render_board_background(surface)

        # Render all points (triangles)
        self.point_renderer.render_all_points(surface)

        # Render central bar
        self.bar_renderer.render(surface)

        # Render side panel
        self.side_panel_renderer.render(surface)
