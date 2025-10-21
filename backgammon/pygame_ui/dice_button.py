"""
Dice button renderer for Backgammon game.
Provides a clickable button to roll dice at the start of each turn.
"""

from typing import Tuple
import pygame
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.board_dimensions import BoardDimensions


class DiceButton:
    """
    Renders and manages a clickable button for rolling dice.

    Attributes:
        colors: ColorScheme instance for color definitions
        dimensions: BoardDimensions instance for layout calculations
        button_rect: pygame.Rect defining the button's clickable area
        is_hovered: Boolean indicating if mouse is over button
        is_enabled: Boolean indicating if button can be clicked
    """

    def __init__(self, colors: ColorScheme, dimensions: BoardDimensions) -> None:
        """
        Initialize the DiceButton.

        Args:
            colors: ColorScheme instance
            dimensions: BoardDimensions instance
        """
        self.colors: ColorScheme = colors
        self.dimensions: BoardDimensions = dimensions
        self.button_rect: pygame.Rect = self._calculate_button_rect()
        self.is_hovered: bool = False
        self.is_enabled: bool = True

    def _calculate_button_rect(self) -> pygame.Rect:
        """
        Calculate the button's position and size.

        Returns:
            pygame.Rect for the button
        """
        panel_rect = self.dimensions.get_side_panel_rect()

        # Position button in the middle section of the side panel
        button_width = 120
        button_height = 50
        button_x = panel_rect[0] + (panel_rect[2] - button_width) // 2

        # Center vertically in middle third of panel
        section_height = panel_rect[3] // 3
        button_y = (
            panel_rect[1] + section_height + (section_height - button_height) // 2
        )

        return pygame.Rect(button_x, button_y, button_width, button_height)

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
        Render the dice roll button.

        Args:
            surface: Pygame surface to draw on
        """
        # Determine button color based on state
        if not self.is_enabled:
            button_color = (100, 100, 100)  # Gray when disabled
            text_color = (150, 150, 150)  # Light gray text
            border_color = (80, 80, 80)  # Dark gray border
        elif self.is_hovered:
            button_color = (70, 180, 70)  # Bright green when hovered
            text_color = (255, 255, 255)  # White text
            border_color = (50, 150, 50)  # Dark green border
        else:
            button_color = (50, 150, 50)  # Green when normal
            text_color = (255, 255, 255)  # White text
            border_color = (30, 100, 30)  # Darker green border

        # Draw button background with rounded corners
        pygame.draw.rect(surface, button_color, self.button_rect, border_radius=10)

        # Draw button border
        pygame.draw.rect(surface, border_color, self.button_rect, 3, border_radius=10)

        # Draw button text
        try:
            font = pygame.font.Font(None, 32)
            text_surface = font.render("ROLL DICE", True, text_color)
            text_rect = text_surface.get_rect(center=self.button_rect.center)
            surface.blit(text_surface, text_rect)
        except Exception:
            # Fallback if font fails to load
            pass

        # Draw dice icon (two small squares) if enabled
        if self.is_enabled:
            self._render_dice_icon(surface)

    def _render_dice_icon(self, surface: pygame.Surface) -> None:
        """
        Render small dice icons on the button.

        Args:
            surface: Pygame surface to draw on
        """
        icon_size = 12
        icon_spacing = 5
        center_x = self.button_rect.centerx
        center_y = self.button_rect.centery + 15  # Below text

        # Left die
        left_rect = pygame.Rect(
            center_x - icon_size - icon_spacing // 2,
            center_y - icon_size // 2,
            icon_size,
            icon_size,
        )
        pygame.draw.rect(surface, (255, 255, 255), left_rect, border_radius=2)
        pygame.draw.rect(surface, (0, 0, 0), left_rect, 1, border_radius=2)

        # Draw single pip on left die
        pip_radius = 2
        pygame.draw.circle(
            surface, (0, 0, 0), (left_rect.centerx, left_rect.centery), pip_radius
        )

        # Right die
        right_rect = pygame.Rect(
            center_x + icon_spacing // 2,
            center_y - icon_size // 2,
            icon_size,
            icon_size,
        )
        pygame.draw.rect(surface, (255, 255, 255), right_rect, border_radius=2)
        pygame.draw.rect(surface, (0, 0, 0), right_rect, 1, border_radius=2)

        # Draw two pips on right die
        offset = 3
        pygame.draw.circle(
            surface,
            (0, 0, 0),
            (right_rect.centerx - offset, right_rect.centery - offset),
            pip_radius,
        )
        pygame.draw.circle(
            surface,
            (0, 0, 0),
            (right_rect.centerx + offset, right_rect.centery + offset),
            pip_radius,
        )
