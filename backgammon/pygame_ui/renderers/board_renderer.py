"""
Board renderer for Backgammon board.
Responsible for rendering the main board structure and coordinating other renderers.
"""

from typing import Optional, List, Tuple, Union
import pygame
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.board_dimensions import BoardDimensions
from backgammon.pygame_ui.renderers.visual_renderer import (
    PointRenderer,
    CheckerRenderer,
    DiceRenderer,
    HighlightRenderer,
    TextRenderer,
)
from backgammon.pygame_ui.renderers.decorative_renderer import (
    BarRenderer,
    SidePanelRenderer,
)


class BoardRenderer:
    """
    Main board renderer that coordinates all board component rendering.

    Attributes:
        colors: ColorScheme instance for color definitions
        dimensions: BoardDimensions instance for layout calculations
        point_renderer: PointRenderer for rendering points
        bar_renderer: BarRenderer for rendering central bar
        side_panel_renderer: SidePanelRenderer for rendering side panel
        checker_renderer: CheckerRenderer for rendering checkers
        dice_renderer: DiceRenderer for rendering dice
        text_renderer: TextRenderer for rendering text information
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
        self.checker_renderer: CheckerRenderer = CheckerRenderer(
            self.colors, self.dimensions
        )
        self.dice_renderer: DiceRenderer = DiceRenderer(self.colors, self.dimensions)
        self.text_renderer: TextRenderer = TextRenderer(self.colors, self.dimensions)
        self.highlight_renderer: HighlightRenderer = HighlightRenderer(
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

    def render(
        self,
        surface: pygame.Surface,
        board: Optional[object] = None,
        dice_values: Optional[List[int]] = None,
        available_moves: Optional[List[int]] = None,
        player_info: Optional[Tuple[str, str, str, int, int]] = None,
        selected_point: Optional[int] = None,
        valid_move_destinations: Optional[List[Union[int, str]]] = None,
        selected_bar: bool = False,
    ) -> None:
        """
        Render the complete Backgammon board.

        Args:
            surface: Pygame surface to draw on
            board: Optional Board instance to render checkers from
            dice_values: Optional list of current dice values
            available_moves: Optional list of available move values
            player_info: Optional tuple of (player1_name, player2_name,
                current_player, p1_off, p2_off)
            selected_point: Optional point number that is currently selected
            valid_move_destinations: Optional list of valid destination points
                or "off" for bearing off
            selected_bar: Boolean indicating if the bar is currently selected
        """
        # Render background
        self._render_board_background(surface)

        # Render all points (triangles)
        self.point_renderer.render_all_points(surface)

        # Render central bar
        self.bar_renderer.render(surface)

        # Render side panel
        self.side_panel_renderer.render(surface)

        # Render checkers if board state is provided
        if board is not None:
            self._render_checkers_from_board(surface, board)

        # Render highlights for selected point and valid moves
        if selected_point is not None and board is not None:
            # Get the number of checkers on the selected point to highlight the top one
            checkers_on_point = board.points[selected_point]
            total_checkers = len(checkers_on_point)
            stack_index = total_checkers - 1 if total_checkers > 0 else 0
            self.highlight_renderer.render_selected_point(
                surface, selected_point, stack_index, total_checkers
            )

        # Render highlight for selected bar
        if selected_bar and board is not None:
            self.highlight_renderer.render_selected_bar(surface, board)

        if valid_move_destinations is not None and len(valid_move_destinations) > 0:
            self.highlight_renderer.render_valid_moves(surface, valid_move_destinations)

        # Render dice if provided
        if dice_values:
            self.dice_renderer.render_dice_in_panel(surface, dice_values)

        # Render available moves if provided
        if available_moves:
            self.dice_renderer.render_available_moves(surface, available_moves)

        # Render player information if provided
        if player_info:
            player1_name, player2_name, current_player, p1_off, p2_off = player_info
            self.text_renderer.render_player_info(
                surface, player1_name, player2_name, current_player, p1_off, p2_off
            )
            self.text_renderer.render_turn_indicator(surface, current_player)

        # Always render instructions
        self.text_renderer.render_instructions(surface)

    def _render_checkers_from_board(
        self, surface: pygame.Surface, board: object
    ) -> None:
        """
        Render all checkers based on the board state.

        Args:
            surface: Pygame surface to draw on
            board: Board instance containing checker positions
        """
        # Render checkers on each point (0-23)
        for point_index in range(24):
            checkers = board.points[point_index]
            if checkers:  # If there are checkers on this point
                self.checker_renderer.render_point_checkers(
                    surface, point_index, checkers
                )

        # Render checkers on the bar
        for color in ["white", "black"]:
            bar_checkers = board.bar[color]
            for stack_index in range(len(bar_checkers)):
                self.checker_renderer.render_bar_checker(surface, color, stack_index)

        # Render checkers that are borne off
        for color in ["white", "black"]:
            off_checkers = board.off[color]
            max_visible_stack = 5
            for stack_index in range(min(len(off_checkers), max_visible_stack)):
                self.checker_renderer.render_off_checker(surface, color, stack_index)
            # Draw indicator if more than max_visible_stack
            if len(off_checkers) > max_visible_stack:
                self.text_renderer.render_off_count_indicator(
                    surface, color, len(off_checkers), max_visible_stack
                )
