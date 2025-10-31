"""
Visual renderer for Backgammon board.
Consolidates all visual rendering components: points, checkers, dice, highlights, and text.
"""

from typing import List, Tuple, Optional
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

        is_top = point_number <= 11
        base_y = self.dimensions.get_point_base_y(is_top)

        if is_top:
            tip_y = base_y + height
            return [
                (x, base_y),
                (x + width, base_y),
                (x + width // 2, tip_y),
            ]
        tip_y = base_y - height
        return [
            (x, base_y),
            (x + width, base_y),
            (x + width // 2, tip_y),
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


class CheckerRenderer:
    """
    Renders checkers (game pieces) on the Backgammon board.

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
            return (240, 240, 240)
        if color == "black":
            return (20, 20, 20)
        return (128, 128, 128)

    def _calculate_checker_position(
        self, point_number: int, stack_index: int, total_checkers: int = 1
    ) -> Tuple[int, int]:
        """
        Calculate the center position for a checker on a specific point.

        Args:
            point_number: Point number (0-23)
            stack_index: Index of the checker in the stack (0 = bottom)
            total_checkers: Total number of checkers on this point

        Returns:
            Tuple of (x, y) coordinates for the checker center
        """
        point_x = self.dimensions.get_point_x(point_number)
        center_x = point_x + (self.dimensions.point_width // 2)

        is_top = point_number <= 11
        base_y = self.dimensions.get_point_base_y(is_top)

        base_spacing = self.checker_radius * 2 + 4

        if total_checkers > 5:
            max_height = self.dimensions.point_height - self.checker_radius
            available_height = max_height - self.checker_radius
            checker_spacing = min(base_spacing, available_height // total_checkers)
        else:
            checker_spacing = base_spacing

        if is_top:
            center_y = base_y + self.checker_radius + (stack_index * checker_spacing)
        else:
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

        shadow_offset = 3
        pygame.draw.circle(
            surface,
            (50, 50, 50),
            (x + shadow_offset, y + shadow_offset),
            self.checker_radius,
        )

        checker_color = self._get_checker_color(color)
        pygame.draw.circle(surface, checker_color, (x, y), self.checker_radius)

        border_color = (0, 0, 0) if color == "white" else (200, 200, 200)
        pygame.draw.circle(surface, border_color, (x, y), self.checker_radius, 2)

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
            total_checkers: Total checkers on this point
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

        center_x = side_panel_rect[0] + (side_panel_rect[2] // 2)

        section_height = side_panel_rect[3] // 3
        middle_section_y = side_panel_rect[1] + section_height

        if color == "white":
            base_y = middle_section_y + 20
        else:
            base_y = middle_section_y + section_height - 20

        max_visible_stack = 5
        if stack_index < max_visible_stack:
            checker_spacing = self.checker_radius * 2 + 2
            center_y = base_y + (stack_index * checker_spacing)
        else:
            center_y = base_y + (max_visible_stack * (self.checker_radius * 2 + 2))

        self._render_checker_with_shadow(surface, (center_x, center_y), color)


class DiceRenderer:
    """
    Renders dice on the Backgammon board.

    Attributes:
        colors: ColorScheme instance for color definitions
        dimensions: BoardDimensions instance for layout calculations
        dice_size: Size of each die in pixels
    """

    def __init__(self, colors: ColorScheme, dimensions: BoardDimensions) -> None:
        """
        Initialize the DiceRenderer.

        Args:
            colors: ColorScheme instance
            dimensions: BoardDimensions instance
        """
        self.colors: ColorScheme = colors
        self.dimensions: BoardDimensions = dimensions
        self.dice_size: int = 40

    def _get_pip_positions(self, value: int) -> List[Tuple[float, float]]:
        """
        Get the positions of pips for a given dice value.

        Args:
            value: Dice value (1-6)

        Returns:
            List of (x, y) tuples representing pip positions (0-1 normalized)
        """
        positions = {
            1: [(0.5, 0.5)],
            2: [(0.25, 0.25), (0.75, 0.75)],
            3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
            4: [
                (0.25, 0.25),
                (0.75, 0.25),
                (0.25, 0.75),
                (0.75, 0.75),
            ],
            5: [
                (0.25, 0.25),
                (0.75, 0.25),
                (0.5, 0.5),
                (0.25, 0.75),
                (0.75, 0.75),
            ],
            6: [
                (0.25, 0.25),
                (0.75, 0.25),
                (0.25, 0.5),
                (0.75, 0.5),
                (0.25, 0.75),
                (0.75, 0.75),
            ],
        }
        return positions.get(value, [])

    def _render_die(
        self, surface: pygame.Surface, position: Tuple[int, int], value: int
    ) -> None:
        """
        Render a single die at the specified position.

        Args:
            surface: Pygame surface to draw on
            position: (x, y) tuple for top-left corner of die
            value: Dice value (1-6)
        """
        x, y = position

        die_rect = pygame.Rect(x, y, self.dice_size, self.dice_size)
        pygame.draw.rect(surface, (255, 255, 255), die_rect, border_radius=5)
        pygame.draw.rect(surface, (0, 0, 0), die_rect, 2, border_radius=5)

        pip_positions = self._get_pip_positions(value)
        pip_radius = self.dice_size // 8

        for pip_x, pip_y in pip_positions:
            actual_x = int(x + pip_x * self.dice_size)
            actual_y = int(y + pip_y * self.dice_size)
            pygame.draw.circle(surface, (0, 0, 0), (actual_x, actual_y), pip_radius)

    def render_dice(
        self, surface: pygame.Surface, dice_values: List[int], position: Tuple[int, int]
    ) -> None:
        """
        Render multiple dice at the specified position.

        Args:
            surface: Pygame surface to draw on
            dice_values: List of dice values to render
            position: (x, y) tuple for starting position
        """
        x, y = position
        spacing = 10

        for i, value in enumerate(dice_values):
            die_x = x + i * (self.dice_size + spacing)
            self._render_die(surface, (die_x, y), value)

    def render_dice_in_panel(
        self, surface: pygame.Surface, dice_values: List[int]
    ) -> None:
        """
        Render dice in the side panel area.

        Args:
            surface: Pygame surface to draw on
            dice_values: List of dice values to render
        """
        if not dice_values:
            return

        panel_rect = self.dimensions.get_side_panel_rect()

        section_height = panel_rect[3] // 3
        center_x = panel_rect[0] + (panel_rect[2] // 2)
        center_y = panel_rect[1] + (section_height // 2)

        total_width = len(dice_values) * self.dice_size + (len(dice_values) - 1) * 10
        start_x = center_x - (total_width // 2)
        start_y = center_y - (self.dice_size // 2)

        self.render_dice(surface, dice_values, (start_x, start_y))

    def render_available_moves(
        self, surface: pygame.Surface, available_moves: List[int]
    ) -> None:
        """
        Render available moves as small dice below the main dice.

        Args:
            surface: Pygame surface to draw on
            available_moves: List of available move values
        """
        if not available_moves:
            return

        panel_rect = self.dimensions.get_side_panel_rect()

        section_height = panel_rect[3] // 3
        center_x = panel_rect[0] + (panel_rect[2] // 2)
        start_y = panel_rect[1] + (section_height // 2) + 60

        original_size = self.dice_size
        self.dice_size = 25

        total_width = (
            len(available_moves) * self.dice_size + (len(available_moves) - 1) * 5
        )
        start_x = center_x - (total_width // 2)

        self.render_dice(surface, available_moves, (start_x, start_y))

        self.dice_size = original_size


class HighlightRenderer:
    """
    Renders visual feedback for player interactions.

    Attributes:
        colors: ColorScheme instance for color definitions
        dimensions: BoardDimensions instance for layout calculations
        checker_radius: Radius of checker pieces (must match CheckerRenderer)
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

        # Use EXACT same checker_radius calculation as CheckerRenderer
        self.checker_radius: int = (self.dimensions.point_width // 3) - 8

        self.selected_color: Tuple[int, int, int] = (255, 215, 0)
        self.valid_move_color: Tuple[int, int, int] = (50, 205, 50)
        self.invalid_move_color: Tuple[int, int, int] = (220, 20, 60)

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

        if is_top:
            center_y = base_y + 30
        else:
            center_y = base_y - 30

        return (center_x, center_y)

    def render_selected_point(
        self,
        surface: pygame.Surface,
        point_number: int,
        stack_index: int = 0,
        total_checkers: int = 1,
    ) -> None:
        """
        Render a highlight around a selected checker.

        Args:
            surface: Pygame surface to draw on
            point_number: Point number (0-23)
            stack_index: Index of the selected checker in the stack
            total_checkers: Total number of checkers on this point
        """
        point_x = self.dimensions.get_point_x(point_number)
        center_x = point_x + (self.dimensions.point_width // 2)

        is_top = point_number <= 11
        base_y = self.dimensions.get_point_base_y(is_top)

        # Use same spacing calculation as CheckerRenderer
        base_spacing = self.checker_radius * 2 + 4

        # Use same logic as CheckerRenderer._calculate_checker_position
        if total_checkers > 5:
            max_height = self.dimensions.point_height - self.checker_radius
            available_height = max_height - self.checker_radius
            checker_spacing = min(base_spacing, available_height // total_checkers)
        else:
            checker_spacing = base_spacing

        if is_top:
            center_y = base_y + self.checker_radius + (stack_index * checker_spacing)
        else:
            center_y = base_y - self.checker_radius - (stack_index * checker_spacing)

        ring_thickness = 3
        pygame.draw.circle(
            surface,
            self.selected_color,
            (center_x, center_y),
            self.checker_radius + 3,
            ring_thickness,
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

        radius = self.dimensions.point_width // 3
        pygame.draw.circle(surface, self.valid_move_color, (center_x, center_y), radius)
        pygame.draw.circle(surface, (0, 100, 0), (center_x, center_y), radius, 3)

    def render_bar_highlight(
        self, surface: pygame.Surface, is_selected: bool = False
    ) -> None:
        """
        Render a highlight on the bar area.

        Args:
            surface: Pygame surface to draw on
            is_selected: If True, render selection highlight
        """
        bar_rect = self.dimensions.get_bar_rect()
        color = self.selected_color if is_selected else self.valid_move_color

        overlay = pygame.Surface((bar_rect[2], bar_rect[3]), pygame.SRCALPHA)
        overlay.fill((*color, 80))
        surface.blit(overlay, (bar_rect[0], bar_rect[1]))

        pygame.draw.rect(surface, color, bar_rect, 4)

    def render_selected_bar(self, surface: pygame.Surface, board: object) -> None:
        """
        Render a highlight for selected bar with checker highlight.

        Args:
            surface: Pygame surface to draw on
            board: Board instance to check checker colors
        """
        self.render_bar_highlight(surface, is_selected=True)

    def render_off_area_highlight(self, surface: pygame.Surface) -> None:
        """
        Render a highlight on the off area (bearing off destination).
        Shows visual indicators similar to valid move points.

        Args:
            surface: Pygame surface to draw on
        """
        panel_rect = self.dimensions.get_side_panel_rect()

        section_height = panel_rect[3] // 3
        center_x = panel_rect[0] + (panel_rect[2] // 2)

        # White player off area (top section)
        white_center_y = panel_rect[1] + (section_height // 2)

        # Black player off area (bottom section)
        black_center_y = panel_rect[1] + section_height * 2 + (section_height // 2)

        # Render indicators for both off areas
        radius = 30

        # Draw pulsating circles to indicate valid bearing off location
        pygame.draw.circle(
            surface, self.valid_move_color, (center_x, white_center_y), radius
        )
        pygame.draw.circle(surface, (0, 100, 0), (center_x, white_center_y), radius, 3)

        pygame.draw.circle(
            surface, self.valid_move_color, (center_x, black_center_y), radius
        )
        pygame.draw.circle(surface, (0, 100, 0), (center_x, black_center_y), radius, 3)

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

        size = 20
        pygame.draw.line(
            surface,
            self.invalid_move_color,
            (center_x - size, center_y - size),
            (center_x + size, center_y + size),
            4,
        )
        pygame.draw.line(
            surface,
            self.invalid_move_color,
            (center_x + size, center_y - size),
            (center_x - size, center_y + size),
            4,
        )


class TextRenderer:
    def render_off_count_indicator(
        self, surface: "pygame.Surface", color: str, count: int, max_visible_stack: int
    ) -> None:
        """
        Render a numeric indicator for the number of borne-off checkers.

        Args:
            surface: Pygame surface to draw on
            color: Color of the checker ('white' or 'black')
            count: Total number of borne-off checkers
            max_visible_stack: Number of checkers shown visually
        """
        side_panel_rect = self.dimensions.get_side_panel_rect()
        center_x = side_panel_rect[0] + (side_panel_rect[2] // 2)
        section_height = side_panel_rect[3] // 3
        checker_spacing = 2 * 20 + 2  # Approximate spacing (radius=20)
        if color == "white":
            base_y = (
                side_panel_rect[1]
                + section_height
                + 20
                + (max_visible_stack * checker_spacing)
            )
        else:
            base_y = (
                side_panel_rect[1]
                + 2 * section_height
                + section_height
                - 20
                + (max_visible_stack * checker_spacing)
            )
        font = pygame.font.Font(None, 32)
        text_surface = font.render(f"x{count}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(center_x, base_y))
        surface.blit(text_surface, text_rect)

    """
    Renders text information on the Backgammon board.

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

        text_x = panel_rect[0] + 10
        text_y = bottom_section_y + 20
        line_spacing = 30

        player1_color = (
            (255, 255, 255) if current_player_name == player1_name else (150, 150, 150)
        )
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

        player2_color = (
            (255, 255, 255) if current_player_name == player2_name else (150, 150, 150)
        )
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
        self,
        surface: pygame.Surface,
        message: str,
        color: Optional[Tuple[int, int, int]] = None,
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

        text_surface = self.font_large.render(message, True, color)
        text_rect = text_surface.get_rect(center=(screen_center_x, screen_center_y))

        background_rect = text_rect.inflate(40, 20)
        pygame.draw.rect(surface, (0, 0, 0, 180), background_rect)
        pygame.draw.rect(surface, color, background_rect, 2)

        surface.blit(text_surface, text_rect)
