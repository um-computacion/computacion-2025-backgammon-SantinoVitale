"""
Pygame UI for Backgammon game.
Main entry point for the graphical user interface using Pygame library.
"""

from typing import Optional
import pygame
from backgammon.pygame_ui.backgammon_board import BackgammonBoard


class PygameUI:
    """
    Pygame-based user interface for Backgammon game.

    This is the main entry point for the Pygame UI. It manages:
    - Window creation and display
    - Main game loop
    - Event handling
    - Coordination with BackgammonBoard

    Attributes:
        game: Reference to the BackgammonGame instance
        screen: Pygame display surface
        clock: Pygame clock for FPS control
        running: Flag to control the game loop
        width: Screen width in pixels
        height: Screen height in pixels
        board: BackgammonBoard coordinator instance
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

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Backgammon Game")
        self.clock = pygame.time.Clock()

        self.board: BackgammonBoard = BackgammonBoard(self.width, self.height)

        self.BACKGROUND_COLOR = (50, 50, 50)

    def set_game(self, game: object) -> None:
        """
        Set the game instance for the UI.

        Args:
            game: BackgammonGame instance
        """
        self.game = game
        self.board.set_game(game)

    def display_message(self, message: str) -> None:
        """
        Display a message to the user.

        Args:
            message: Message to display
        """
        print(f"Pygame UI: {message}")

    def display_board(self) -> None:
        """Display the game board state."""
        self.screen.fill(self.BACKGROUND_COLOR)
        self.board.render(self.screen)
        pygame.display.flip()

    def handle_events(self) -> bool:
        """
        Handle Pygame events.

        Returns:
            True if should continue running, False otherwise
        """
        mouse_pos = pygame.mouse.get_pos()
        self.board.update_hover_state(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.board.handle_mouse_click(event.pos)
        return True

    def run_game(self) -> None:
        """Run the main game loop with Pygame interface."""
        self.running = True

        print("\nStarting Backgammon with Pygame interface...")
        print("Close the window or press ESC to exit")

        while self.running:
            self.running = self.handle_events()
            self.display_board()
            self.clock.tick(60)

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
