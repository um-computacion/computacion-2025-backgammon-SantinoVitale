"""
Pygame UI for Backgammon game.
Provides a graphical user interface using Pygame library.
"""

from typing import Optional
import pygame
from backgammon.pygame_ui.board_renderer import BoardRenderer
from backgammon.pygame_ui.click_detector import ClickDetector


class PygameUI:
    """
    Pygame-based user interface for Backgammon game.

    Attributes:
        game: Reference to the BackgammonGame instance
        screen: Pygame display surface
        clock: Pygame clock for FPS control
        running: Flag to control the game loop
        width: Screen width in pixels
        height: Screen height in pixels
    """

    def __init__(self, width: int = 1600, height: int = 900) -> None:
        """
        Initialize the Pygame UI.

        Args:
            width: Screen width in pixels (default: 1600)
            height: Screen height in pixels (default: 900)
        """
        self.game: Optional[object] = None
        self.width: int = width
        self.height: int = height
        self.running: bool = False

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Backgammon Game")
        self.clock = pygame.time.Clock()

        # Initialize board renderer
        self.board_renderer: BoardRenderer = BoardRenderer(self.width, self.height)

        # Initialize click detector
        self.click_detector: ClickDetector = ClickDetector(
            self.board_renderer.dimensions
        )

        # Selection state for highlighting
        self.selected_point: Optional[int] = None
        self.valid_move_destinations: list = []

        # Click debugging visualization
        self.last_click_pos: Optional[tuple] = None
        self.click_display_frames: int = 0

        # Background color for screen
        self.BACKGROUND_COLOR = (50, 50, 50)  # Dark gray background

    def set_game(self, game: object) -> None:
        """
        Set the game instance for the UI.

        Args:
            game: BackgammonGame instance
        """
        self.game = game

    def display_message(self, message: str) -> None:
        """
        Display a message to the user.

        Args:
            message: Message to display
        """
        print(f"Pygame UI: {message}")

    def display_board(self) -> None:
        """Display the game board state."""
        # Fill background
        self.screen.fill(self.BACKGROUND_COLOR)

        # Prepare render data
        board = None
        dice_values = None
        available_moves = None
        player_info = None

        # If we have a game instance, extract render data
        if self.game is not None:
            if hasattr(self.game, 'board'):
                board = self.game.board

            if hasattr(self.game, 'dice') and self.game.dice.last_roll:
                dice_values = self.game.dice.last_roll
                available_moves = self.game.dice.get_available_moves()

            # Extract player information
            if hasattr(self.game, 'players') and len(self.game.players) >= 2:
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

        # Render the complete board
        self.board_renderer.render(
            self.screen,
            board=board,
            dice_values=dice_values,
            available_moves=available_moves,
            player_info=player_info,
            selected_point=self.selected_point,
            valid_move_destinations=self.valid_move_destinations,
        )

        # Draw click indicator for debugging (red circle)
        if self.click_display_frames > 0:
            if self.last_click_pos:
                pygame.draw.circle(
                    self.screen, (255, 0, 0), self.last_click_pos, 20, 3
                )
            self.click_display_frames -= 1

    def handle_events(self) -> bool:
        """
        Handle Pygame events.

        Returns:
            True if should continue running, False otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self._handle_mouse_click(event.pos)
        return True

    def _handle_mouse_click(self, mouse_pos: tuple) -> None:
        """
        Handle mouse click events for selection and moves.

        Args:
            mouse_pos: Tuple of (x, y) mouse coordinates
        """
        # Store click for visual feedback (debugging)
        self.last_click_pos = mouse_pos
        self.click_display_frames = 60  # Show for 1 second at 60 FPS

        # Check if roll button was clicked
        if self.click_detector.is_roll_button_clicked(mouse_pos):
            print("ROLL DICE BUTTON CLICKED!")
            # TODO: Implement dice rolling in future step
            return

        # Check what was clicked
        clicked_position = self.click_detector.get_clicked_position(mouse_pos)

        if not clicked_position:
            # Click outside board - deselect
            self.selected_point = None
            self.valid_move_destinations = []
            return

        position_type, value = clicked_position

        # Only handle point clicks for now
        if position_type != "point":
            return

        clicked_point = value

        # If no point is selected, select the clicked point
        if self.selected_point is None:
            # Check if the clicked point has checkers
            if self.game and hasattr(self.game, 'board'):
                checkers = self.game.board.points[clicked_point]
                if checkers:
                    # Select this point
                    self.selected_point = clicked_point
                    # Calculate valid destinations (simplified for now)
                    # In future, this will use game logic to get valid moves
                    self.valid_move_destinations = self._get_valid_destinations(clicked_point)
                    print(f"Selected point {clicked_point}")
                else:
                    print(f"No checkers on point {clicked_point}")
        else:
            # A point is already selected
            if clicked_point == self.selected_point:
                # Clicking the same point - deselect
                self.selected_point = None
                self.valid_move_destinations = []
                print("Deselected point")
            elif clicked_point in self.valid_move_destinations:
                # Clicked a valid destination - execute move
                print(f"Move from {self.selected_point} to {clicked_point}")
                # TODO: Execute move in future step
                # Clear selection after move
                self.selected_point = None
                self.valid_move_destinations = []
            else:
                # Clicked a different point - change selection
                if self.game and hasattr(self.game, 'board'):
                    checkers = self.game.board.points[clicked_point]
                    if checkers:
                        self.selected_point = clicked_point
                        self.valid_move_destinations = self._get_valid_destinations(clicked_point)
                        print(f"Selected point {clicked_point}")
                    else:
                        # No checkers - deselect
                        self.selected_point = None
                        self.valid_move_destinations = []

    def _get_valid_destinations(self, from_point: int) -> list:
        """
        Get valid destination points for a selected checker.
        This is a simplified version for demonstration.

        Args:
            from_point: The point number where the checker is

        Returns:
            List of valid destination point numbers
        """
        # Simplified logic - in future this will use game rules
        # For now, just show points within dice range
        valid_destinations = []

        if self.game and hasattr(self.game, 'dice') and self.game.dice.last_roll:
            available_moves = self.game.dice.get_available_moves()
            for move in available_moves:
                # Calculate destination based on current player direction
                # White moves from 0 to 23, Black moves from 23 to 0
                destination = from_point + move  # Simplified: assuming white player
                if 0 <= destination <= 23:
                    valid_destinations.append(destination)

        return valid_destinations

    def run_game(self) -> None:
        """Run the main game loop with Pygame interface."""
        self.running = True

        print("\nStarting Backgammon with Pygame interface...")
        print("Close the window or press ESC to exit")

        while self.running:
            # Handle events
            self.running = self.handle_events()

            # Draw everything
            self.display_board()

            # Update display
            pygame.display.flip()

            # Control FPS
            self.clock.tick(60)

        # Cleanup
        pygame.quit()
        print("\nPygame window closed. Thanks for playing!")

    def get_player_move(self) -> Optional[tuple]:
        """
        Get player move input (placeholder).

        Returns:
            Tuple representing the move or None
        """
        return None

    def display_winner(self, winner_name: str) -> None:
        """
        Display the game winner.

        Args:
            winner_name: Name of the winning player
        """
        print(f"Winner: {winner_name}")
