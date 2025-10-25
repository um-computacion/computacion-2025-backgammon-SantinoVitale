"""
Button component for Backgammon UI.
Provides a reusable button class for UI interactions.
"""

from typing import Tuple
import pygame
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.board_dimensions import BoardDimensions


class Button:
    """
    Generic button component for UI interactions.

    Attributes:
        colors: ColorScheme instance for color definitions
        dimensions: BoardDimensions instance for layout calculations
        button_rect: pygame.Rect defining the button's clickable area
        is_hovered: Boolean indicating if mouse is over button
        is_enabled: Boolean indicating if button can be clicked
        text: Button text label
        font_size: Font size for button text
    """

    def __init__(
        self,
        colors: ColorScheme,
        dimensions: BoardDimensions,
        text: str,
        rect: pygame.Rect,
        font_size: int = 32,
    ) -> None:
        """
        Initialize the Button.

        Args:
            colors: ColorScheme instance
            dimensions: BoardDimensions instance
            text: Button text label
            rect: pygame.Rect defining button position and size
            font_size: Font size for button text
        """
        self.colors: ColorScheme = colors
        self.dimensions: BoardDimensions = dimensions
        self.button_rect: pygame.Rect = rect
        self.text: str = text
        self.font_size: int = font_size
        self.is_hovered: bool = False
        self.is_enabled: bool = True

    def update_hover_state(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update whether the button is being hovered.

        Args:
            mouse_pos: Current mouse position (x, y)
        """
        self.is_hovered = self.button_rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """
        Check if the button was clicked at the given position.

        Args:
            mouse_pos: Click position (x, y)

        Returns:
            True if button was clicked and is enabled, False otherwise
        """
        return self.is_enabled and self.button_rect.collidepoint(mouse_pos)

    def set_enabled(self, enabled: bool) -> None:
        """
        Enable or disable the button.

        Args:
            enabled: True to enable, False to disable
        """
        self.is_enabled = enabled

    def render(self, surface: pygame.Surface) -> None:
        """
        Render the button.

        Args:
            surface: Pygame surface to draw on
        """
        if not self.is_enabled:
            button_color = (100, 100, 100)
            border_color = (70, 70, 70)
        elif self.is_hovered:
            button_color = (70, 180, 70)
            border_color = (40, 120, 40)
        else:
            button_color = (50, 150, 50)
            border_color = (30, 100, 30)

        pygame.draw.rect(surface, button_color, self.button_rect, border_radius=10)
        pygame.draw.rect(surface, border_color, self.button_rect, 3, border_radius=10)

        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        surface.blit(text_surface, text_rect)
