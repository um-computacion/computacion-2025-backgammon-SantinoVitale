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
        Handle mouse click events for debugging.

        Args:
            mouse_pos: Tuple of (x, y) mouse coordinates
        """
        # Store click for visual feedback
        self.last_click_pos = mouse_pos
        self.click_display_frames = 60  # Show for 1 second at 60 FPS

        print("\n=== MOUSE CLICK DEBUG ===")
        print(f"Mouse position: {mouse_pos}")

        # Check what was clicked
        clicked_position = self.click_detector.get_clicked_position(mouse_pos)

        if clicked_position:
            position_type, value = clicked_position
            print(f"Clicked: {position_type}")
            if position_type == "point":
                print(f"Point number: {value}")
            print("=" * 25)
        else:
            print("Clicked outside board")
            print("=" * 25)

        # Check if roll button was clicked
        if self.click_detector.is_roll_button_clicked(mouse_pos):
            print("ROLL DICE BUTTON CLICKED!")
            print("=" * 25)

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
