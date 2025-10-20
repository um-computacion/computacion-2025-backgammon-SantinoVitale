"""
Pygame UI for Backgammon game.
Provides a graphical user interface using Pygame library.
"""

from typing import Optional
import pygame


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

    def __init__(self, width: int = 1280, height: int = 720) -> None:
        """
        Initialize the Pygame UI.

        Args:
            width: Screen width in pixels (default: 1280)
            height: Screen height in pixels (default: 720)
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

        # Colors
        self.BACKGROUND_COLOR = (139, 69, 19)  # Brown
        self.BOARD_COLOR = (210, 180, 140)  # Tan
        self.TEXT_COLOR = (255, 255, 255)  # White
        self.BLACK_COLOR = (0, 0, 0)  # Black

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

        # Draw board rectangle
        board_rect = pygame.Rect(50, 50, self.width - 100, self.height - 100)
        pygame.draw.rect(self.screen, self.BOARD_COLOR, board_rect)
        pygame.draw.rect(self.screen, self.BLACK_COLOR, board_rect, 3)

        # Draw title
        font = pygame.font.Font(None, 48)
        title_text = font.render("Backgammon", True, self.TEXT_COLOR)
        title_rect = title_text.get_rect(center=(self.width // 2, 30))
        self.screen.blit(title_text, title_rect)

        # Draw placeholder text
        info_font = pygame.font.Font(None, 32)
        info_text = info_font.render(
            "Pygame UI - In Development", True, self.BLACK_COLOR
        )
        info_rect = info_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(info_text, info_rect)

        # Draw instructions
        instruction_font = pygame.font.Font(None, 24)
        instruction_text = instruction_font.render(
            "Press ESC to exit", True, self.BLACK_COLOR
        )
        instruction_rect = instruction_text.get_rect(
            center=(self.width // 2, self.height // 2 + 50)
        )
        self.screen.blit(instruction_text, instruction_rect)

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
        return True

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
        print("\n👋 Pygame window closed. Thanks for playing!")

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
        print(f"🏆 Winner: {winner_name}")
