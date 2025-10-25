"""
Backgammon board coordinator.
Main coordinator class that manages board rendering and interaction.
"""

from typing import Optional, Tuple
import pygame
from backgammon.pygame_ui.board_dimensions import BoardDimensions
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.renderers.board_renderer import BoardRenderer
from backgammon.pygame_ui.click_detector import ClickDetector
from backgammon.pygame_ui.board_interaction import BoardInteraction
from backgammon.pygame_ui.button import Button


class BackgammonBoard:
    """
    Main coordinator for the Backgammon board UI.

    This class coordinates all board-related components:
    - Board rendering (delegated to BoardRenderer)
    - User interactions (delegated to BoardInteraction)
    - UI components (buttons)
    - Game state synchronization

    Attributes:
        dimensions: BoardDimensions instance for layout
        colors: ColorScheme instance for colors
        board_renderer: BoardRenderer for visual rendering
        click_detector: ClickDetector for mouse coordinate conversion
        interaction: BoardInteraction for handling player input
        dice_button: Button for rolling dice
        game: Reference to BackgammonGame instance
    """

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """
        Initialize the BackgammonBoard coordinator.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.dimensions: BoardDimensions = BoardDimensions(screen_width, screen_height)
        self.colors: ColorScheme = ColorScheme()
        self.board_renderer: BoardRenderer = BoardRenderer(screen_width, screen_height)
        self.click_detector: ClickDetector = ClickDetector(self.dimensions)
        self.interaction: BoardInteraction = BoardInteraction(self.click_detector)

        self._create_dice_button()

        self.game: Optional[object] = None
        self.last_player_index: int = -1

    def _create_dice_button(self) -> None:
        """Create the dice roll button."""
        panel_rect = self.dimensions.get_side_panel_rect()
        button_width = 120
        button_height = 50
        button_x = panel_rect[0] + (panel_rect[2] - button_width) // 2
        section_height = panel_rect[3] // 3
        button_y = panel_rect[1] + section_height + (section_height - button_height) // 2

        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        self.dice_button: Button = Button(
            self.colors, self.dimensions, "ROLL DICE", button_rect
        )

    def set_game(self, game: object) -> None:
        """
        Set the game instance for both board and interaction.

        Args:
            game: BackgammonGame instance
        """
        self.game = game
        self.interaction.set_game(game)
        # Initialize last_player_index with current player
        if hasattr(game, 'current_player_index'):
            self.last_player_index = game.current_player_index

    def handle_mouse_click(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Handle mouse click events.

        Args:
            mouse_pos: Tuple of (x, y) mouse coordinates
        """
        if self.dice_button.is_clicked(mouse_pos):
            self._handle_dice_button_click()
            return

        clicked_position = self.click_detector.get_clicked_position(mouse_pos)

        if not clicked_position:
            self.interaction.clear_selection()
            return

        position_type, value = clicked_position

        if position_type == "point":
            self.interaction.handle_point_click(value)
        elif position_type == "off":
            self.interaction.handle_off_area_click()

    def _handle_dice_button_click(self) -> None:
        """Handle dice button click."""
        if not self.interaction.dice_rolled:
            print("ROLLING DICE...")
            if self.game and hasattr(self.game, "roll_dice"):
                self.game.roll_dice()
                self.interaction.dice_rolled = True
                self.dice_button.set_enabled(False)
                print(f"Dice rolled: {self.game.dice.last_roll}")
            else:
                print("Game instance not available")
        else:
            print("Dice already rolled this turn")

    def update_hover_state(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update hover state for interactive elements.

        Args:
            mouse_pos: Current mouse position (x, y)
        """
        self.dice_button.update_hover_state(mouse_pos)

    def render(self, surface: pygame.Surface) -> None:
        """
        Render the complete board with all components.

        Args:
            surface: Pygame surface to draw on
        """
        board = None
        dice_values = None
        available_moves = None
        player_info = None

        if self.game is not None:
            if hasattr(self.game, "board"):
                board = self.game.board

            if hasattr(self.game, "dice") and self.game.dice.last_roll:
                dice_values = self.game.dice.last_roll
                available_moves = self.game.dice.get_available_moves()

            if hasattr(self.game, "players") and len(self.game.players) >= 2:
                player1 = self.game.players[0]
                player2 = self.game.players[1]
                current_player = self.game.get_current_player()

                player_info = (
                    player1.name or "Player 1",
                    player2.name or "Player 2",
                    current_player.name if current_player else "Unknown",
                    player1.checkers_off_board,
                    player2.checkers_off_board,
                )

        self.board_renderer.render(
            surface,
            board=board,
            dice_values=dice_values,
            available_moves=available_moves,
            player_info=player_info,
            selected_point=self.interaction.selected_point,
            valid_move_destinations=self.interaction.valid_move_destinations,
        )

        self.dice_button.render(surface)

        self._update_button_state(available_moves)

    def _update_button_state(self, available_moves: Optional[list]) -> None:
        """
        Update dice button state based on game state.
        Enables button when turn changes or dice need to be rolled.
        
        Args:
            available_moves: List of available dice moves or None
        """
        if not self.game:
            return
            
        # Check if player has changed (turn switched)
        current_player_index = self.game.current_player_index
        if current_player_index != self.last_player_index:
            print(f"Turn changed from player {self.last_player_index} to player {current_player_index}")
            self.last_player_index = current_player_index
            self.interaction.reset_turn_state()
            self.dice_button.set_enabled(True)
            return
        
        # If no moves available after rolling, keep button disabled until turn changes
        if available_moves is not None and len(available_moves) == 0 and self.interaction.dice_rolled:
            self.dice_button.set_enabled(False)
