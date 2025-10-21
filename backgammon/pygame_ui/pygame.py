"""
Pygame UI for Backgammon game.
Provides a graphical user interface using Pygame library.
"""

from typing import Optional
import pygame
from backgammon.pygame_ui.board_renderer import BoardRenderer
from backgammon.pygame_ui.click_detector import ClickDetector
from backgammon.pygame_ui.dice_button import DiceButton


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

        # Initialize dice button
        self.dice_button: DiceButton = DiceButton(
            self.board_renderer.colors, self.board_renderer.dimensions
        )

        # Selection state for highlighting
        self.selected_point: Optional[int] = None
        self.valid_move_destinations: list = []

        # Game state tracking
        self.dice_rolled: bool = False  # Track if dice have been rolled this turn

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
            if hasattr(self.game, "board"):
                board = self.game.board

            if hasattr(self.game, "dice") and self.game.dice.last_roll:
                dice_values = self.game.dice.last_roll
                available_moves = self.game.dice.get_available_moves()

            # Extract player information
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

        # Render dice button
        self.dice_button.render(self.screen)

        # Update button state based on available moves
        if available_moves is not None and len(available_moves) == 0:
            # All dice consumed - enable button for next turn
            if self.dice_rolled:
                self.dice_rolled = False
                self.dice_button.set_enabled(True)
                # Clear selection when turn ends
                self.selected_point = None
                self.valid_move_destinations = []

        # Draw click indicator for debugging (red circle)
        if self.click_display_frames > 0:
            if self.last_click_pos:
                pygame.draw.circle(self.screen, (255, 0, 0), self.last_click_pos, 20, 3)
            self.click_display_frames -= 1

    def handle_events(self) -> bool:
        """
        Handle Pygame events.

        Returns:
            True if should continue running, False otherwise
        """
        # Update dice button hover state
        mouse_pos = pygame.mouse.get_pos()
        self.dice_button.update_hover_state(mouse_pos)

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

        # Check if dice button was clicked
        if self.dice_button.is_clicked(mouse_pos):
            if not self.dice_rolled:
                print("🎲 ROLLING DICE...")
                if self.game and hasattr(self.game, "roll_dice"):
                    self.game.roll_dice()
                    self.dice_rolled = True
                    self.dice_button.set_enabled(False)
                    print(f"✓ Dice rolled: {self.game.dice.last_roll}")
                else:
                    print("✗ Game instance not available")
            else:
                print("✗ Dice already rolled this turn")
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
            if self.game and hasattr(self.game, "board"):
                checkers = self.game.board.points[clicked_point]
                if checkers:
                    # Check if these are the current player's checkers
                    current_player = self.game.get_current_player()
                    if current_player and checkers[0].color != current_player.color:
                        print(
                            f"✗ Cannot select point {clicked_point} - these are {checkers[0].color} checkers"
                        )
                        print(f"  Current turn: {current_player.color}")
                        return

                    # Select this point
                    self.selected_point = clicked_point
                    # Calculate valid destinations (simplified for now)
                    # In future, this will use game logic to get valid moves
                    self.valid_move_destinations = self._get_valid_destinations(
                        clicked_point
                    )
                    print(f"✓ Selected point {clicked_point}")
                    print(
                        f"  Checkers on point: {len(checkers)} {checkers[0].color if checkers else 'none'}"
                    )
                    print(f"  Valid destinations: {self.valid_move_destinations}")
                else:
                    print(f"✗ No checkers on point {clicked_point}")
        else:
            # A point is already selected
            if clicked_point == self.selected_point:
                # Clicking the same point - deselect
                self.selected_point = None
                self.valid_move_destinations = []
                print("Deselected point")
            elif clicked_point in self.valid_move_destinations:
                # Clicked a valid destination - execute move
                print(f"Attempting move from {self.selected_point} to {clicked_point}")

                # Execute the move through the game logic
                if self.game and hasattr(self.game, "make_move"):
                    # Convert from UI indexing (0-23) to game notation (1-24)
                    from_notation = self.selected_point + 1
                    to_notation = clicked_point + 1

                    print(f"  Game notation: {from_notation} → {to_notation}")
                    success = self.game.make_move(from_notation, to_notation)

                    if success:
                        print(
                            f"✓ Move successful: {self.selected_point} → {clicked_point}"
                        )
                        # Clear selection after successful move
                        self.selected_point = None
                        self.valid_move_destinations = []
                    else:
                        print(f"✗ Move failed: {self.selected_point} → {clicked_point}")
                        # Keep selection for retry
                else:
                    print("Game instance not available for move execution")
                    # Clear selection
                    self.selected_point = None
                    self.valid_move_destinations = []
            else:
                # Clicked a different point - change selection
                if self.game and hasattr(self.game, "board"):
                    checkers = self.game.board.points[clicked_point]
                    if checkers:
                        self.selected_point = clicked_point
                        self.valid_move_destinations = self._get_valid_destinations(
                            clicked_point
                        )
                        print(f"Selected point {clicked_point}")
                    else:
                        # No checkers - deselect
                        self.selected_point = None
                        self.valid_move_destinations = []

    def _get_valid_destinations(self, from_point: int) -> list:
        """
        Get valid destination points for a selected checker using game logic.

        Args:
            from_point: The point number where the checker is (0-23)

        Returns:
            List of valid destination point numbers
        """
        valid_destinations = []

        if not self.game or not hasattr(self.game, "dice"):
            print("  ✗ No game or dice available")
            return valid_destinations

        # Check if there are dice available
        if not self.game.dice.last_roll:
            print("  ✗ No dice have been rolled yet")
            return valid_destinations

        # Get available dice values
        available_moves = self.game.dice.get_available_moves()

        if not available_moves:
            print("  ✗ No available moves from dice")
            return valid_destinations

        # Get current player color
        current_player = self.game.get_current_player()
        if not current_player:
            print("  ✗ No current player")
            return valid_destinations

        player_color = current_player.color

        # Check if the clicked point has checkers of the current player
        if not hasattr(self.game, "board"):
            print("  ✗ No board available")
            return valid_destinations

        checkers = self.game.board.points[from_point]
        if not checkers or checkers[0].color != player_color:
            print("  ✗ Point has wrong color checkers")
            return valid_destinations

        # Try each available dice value (use set to avoid duplicates)
        seen_destinations = set()

        for move in available_moves:
            # Calculate destination based on player direction
            # White moves from high to low (23 → 0), Black moves from low to high (0 → 23)
            if player_color == "white":
                destination = from_point - move
            else:  # black
                destination = from_point + move

            # Skip if we've already checked this destination
            if destination in seen_destinations:
                continue

            seen_destinations.add(destination)

            # Validate the move using game logic
            if 0 <= destination <= 23:
                # Convert to 1-24 notation for BackgammonGame.is_valid_move()
                from_notation = from_point + 1
                to_notation = destination + 1

                # Check if the move is valid according to game rules
                if self.game.is_valid_move(from_notation, to_notation):
                    valid_destinations.append(destination)
                # else: move blocked by opponent
            else:
                # TODO: Handle bearing off (destination < 0 for white, > 23 for black)
                pass  # Silently skip out of bounds for now

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
