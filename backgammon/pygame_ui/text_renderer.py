"""
Text renderer for Backgammon game.
Responsible for rendering text information on the board.
"""

from typing import Tuple, Optional
import pygame
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.board_dimensions import BoardDimensions


class TextRenderer:
    """
    Renders text information on the Backgammon board.

    This class is responsible for displaying player names, scores,
    current turn, and other game information.

    Attributes:
        colors: ColorScheme instance for color definitions
        dimensions: BoardDimensions instance for layout calculations
        font_large: Large font for titles
        font_medium: Medium font for player names
        font_small: Small font for details
    """

    def __init__(self, colors: ColorScheme, dimensions: BoardDimensions) -> None:
        """
        Initialize the TextRenderer.

        Args:
            colors: ColorScheme instance
            dimensions: BoardDimensions instance
        """
        self.colors: ColorScheme = colors
        self.dimensions: BoardDimensions = dimensions

        # Initialize fonts
        pygame.font.init()
        self.font_large: pygame.font.Font = pygame.font.Font(None, 36)
        self.font_medium: pygame.font.Font = pygame.font.Font(None, 28)
        self.font_small: pygame.font.Font = pygame.font.Font(None, 20)

    def _render_text(
        self,
        surface: pygame.Surface,
        text: str,
        position: Tuple[int, int],
        font: pygame.font.Font,
        color: Tuple[int, int, int],
        center: bool = False,
    ) -> None:
        """
        Render text at the specified position.

        Args:
            surface: Pygame surface to draw on
            text: Text to render
            position: (x, y) tuple for text position
            font: Pygame font to use
            color: RGB color tuple
            center: If True, center text at position
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if center:
            text_rect.center = position
        else:
            text_rect.topleft = position

        surface.blit(text_surface, text_rect)

    def render_player_info(
        self,
        surface: pygame.Surface,
        player1_name: str,
        player2_name: str,
        current_player_name: str,
        player1_off: int,
        player2_off: int,
    ) -> None:
        """
        Render player information in the side panel bottom section.

        Args:
            surface: Pygame surface to draw on
            player1_name: Name of player 1
            player2_name: Name of player 2
            current_player_name: Name of current player
            player1_off: Number of checkers player 1 has borne off
            player2_off: Number of checkers player 2 has borne off
        """
        panel_rect = self.dimensions.get_side_panel_rect()
        section_height = panel_rect[3] // 3
        bottom_section_y = panel_rect[1] + (2 * section_height)

        # Starting position for text
        text_x = panel_rect[0] + 10
        text_y = bottom_section_y + 20
        line_spacing = 30

        # Render player 1 info
        player1_color = (255, 255, 255) if current_player_name == player1_name else (150, 150, 150)
        self._render_text(
            surface,
            f"{player1_name}",
            (text_x, text_y),
            self.font_medium,
            player1_color,
        )
        self._render_text(
            surface,
            f"Off: {player1_off}/15",
            (text_x, text_y + 25),
            self.font_small,
            player1_color,
        )

        # Render player 2 info
        player2_color = (255, 255, 255) if current_player_name == player2_name else (150, 150, 150)
        self._render_text(
            surface,
            f"{player2_name}",
            (text_x, text_y + line_spacing * 2),
            self.font_medium,
            player2_color,
        )
        self._render_text(
            surface,
            f"Off: {player2_off}/15",
            (text_x, text_y + line_spacing * 2 + 25),
            self.font_small,
            player2_color,
        )

    def render_turn_indicator(
        self, surface: pygame.Surface, current_player_name: str
    ) -> None:
        """
        Render current turn indicator.

        Args:
            surface: Pygame surface to draw on
            current_player_name: Name of the current player
        """
        # Render at the top of the screen
        screen_center_x = self.dimensions.screen_width // 2
        text = f"Turn: {current_player_name}"

        self._render_text(
            surface,
            text,
            (screen_center_x, 10),
            self.font_large,
            (255, 255, 255),
            center=True,
        )

    def render_instructions(self, surface: pygame.Surface) -> None:
        """
        Render basic instructions at the bottom of the screen.

        Args:
            surface: Pygame surface to draw on
        """
        instructions = "ESC to exit | Click checkers to move"
        screen_center_x = self.dimensions.screen_width // 2
        screen_bottom_y = self.dimensions.screen_height - 15

        self._render_text(
            surface,
            instructions,
            (screen_center_x, screen_bottom_y),
            self.font_small,
            (200, 200, 200),
            center=True,
        )

    def render_message(
        self, surface: pygame.Surface, message: str, color: Optional[Tuple[int, int, int]] = None
    ) -> None:
        """
        Render a temporary message in the center of the screen.

        Args:
            surface: Pygame surface to draw on
            message: Message to display
            color: Optional RGB color tuple (default: white)
        """
        if color is None:
            color = (255, 255, 255)

        screen_center_x = self.dimensions.screen_width // 2
        screen_center_y = self.dimensions.screen_height // 2

        # Render with a semi-transparent background
        text_surface = self.font_large.render(message, True, color)
        text_rect = text_surface.get_rect(center=(screen_center_x, screen_center_y))

        # Draw background rectangle
        background_rect = text_rect.inflate(40, 20)
        pygame.draw.rect(surface, (0, 0, 0, 180), background_rect)
        pygame.draw.rect(surface, color, background_rect, 2)

        # Draw text
        surface.blit(text_surface, text_rect)
