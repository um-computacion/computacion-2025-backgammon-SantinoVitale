"""
Board interaction handler for Backgammon game.
Manages mouse interactions, selection state, and move validation.
"""

from typing import Optional, List, Union
from backgammon.pygame_ui.click_detector import ClickDetector


class BoardInteraction:
    """
    Handles all mouse interactions with the game board.

    This class manages:
    - Checker selection and deselection
    - Valid move calculation
    - Move execution through game logic
    - Visual feedback state (highlighting)

    Attributes:
        click_detector: ClickDetector instance for coordinate conversion
        game: Reference to BackgammonGame instance
        selected_point: Currently selected point (0-23) or None
        valid_move_destinations: List of valid destination points or "off" for bearing off
        dice_rolled: Flag tracking if dice have been rolled this turn
    """

    def __init__(self, click_detector: ClickDetector) -> None:
        """
        Initialize the BoardInteraction handler.

        Args:
            click_detector: ClickDetector instance for coordinate conversion
        """
        self.click_detector: ClickDetector = click_detector
        self.game: Optional[object] = None
        self.selected_point: Optional[int] = None
        self.selected_bar: bool = False
        self.valid_move_destinations: List[Union[int, str]] = []
        self.dice_rolled: bool = False

    def set_game(self, game: object) -> None:
        """
        Set the game instance.

        Args:
            game: BackgammonGame instance
        """
        self.game = game

    def handle_point_click(self, clicked_point: int) -> None:
        """
        Handle click on a board point.

        Args:
            clicked_point: Point number that was clicked (0-23)
        """
        if self.selected_point is None and not self.selected_bar:
            self._try_select_point(clicked_point)
        else:
            if not self.selected_bar and clicked_point == self.selected_point:
                self._deselect_point()
            elif clicked_point in self.valid_move_destinations:
                if self.selected_bar:
                    self._execute_move_from_bar(clicked_point)
                else:
                    self._execute_move(clicked_point)
            else:
                self._try_select_point(clicked_point)

    def handle_off_area_click(self) -> None:
        """
        Handle click on the off area (bearing off destination).
        """
        if self.selected_point is None and not self.selected_bar:
            print("No checker selected for bearing off")
            return

        if self.selected_bar:
            print("Cannot bear off from bar - must enter the board first")
            self._deselect_point()
            return

        if "off" in self.valid_move_destinations:
            self._execute_move_to_off()
        else:
            print("Bearing off is not a valid move from this position")
            self._deselect_point()

    def handle_bar_click(self) -> None:
        """
        Handle click on the bar area (where captured checkers are placed).
        """
        if not self.game or not hasattr(self.game, "board"):
            return

        current_player = self.game.get_current_player()
        if not current_player:
            return

        checkers_on_bar = self.game.board.bar.get(current_player.color, [])
        if not checkers_on_bar:
            print(f"No {current_player.color} checkers on bar")
            return

        self.selected_bar = True
        self.selected_point = None
        self.valid_move_destinations = self._calculate_valid_destinations_from_bar()
        print(f"Selected bar - {len(checkers_on_bar)} {current_player.color} checkers")
        print(f"Valid destinations: {self.valid_move_destinations}")

    def _try_select_point(self, point: int) -> None:
        """
        Try to select a point with checkers.

        Args:
            point: Point number to select
        """
        if not self.game or not hasattr(self.game, "board"):
            return

        # Check if player has checkers on bar - they must move those first
        current_player = self.game.get_current_player()
        if not current_player:
            return

        checkers_on_bar = self.game.board.bar.get(current_player.color, [])
        if checkers_on_bar:
            print("Cannot select point - you must move checkers from bar first")
            print("Click on the bar area to select checker")
            return

        checkers = self.game.board.points[point]
        if not checkers:
            print(f"No checkers on point {point}")
            return

        if checkers[0].color != current_player.color:
            print(
                f"Cannot select point {point} - these are {checkers[0].color} checkers"
            )
            print(f"Current turn: {current_player.color}")
            return

        self.selected_point = point
        self.selected_bar = False
        self.valid_move_destinations = self._calculate_valid_destinations(point)
        print(f"Selected point {point}")
        print(f"Checkers on point: {len(checkers)} {checkers[0].color}")
        print(f"Valid destinations: {self.valid_move_destinations}")

    def _deselect_point(self) -> None:
        """Deselect the currently selected point."""
        self.selected_point = None
        self.selected_bar = False
        self.valid_move_destinations = []
        print("Deselected point")

    def _execute_move(self, to_point: int) -> None:
        """
        Execute a move from selected point to destination.

        Args:
            to_point: Destination point number
        """
        if self.selected_point is None:
            return

        print(f"Attempting move from {self.selected_point} to {to_point}")

        if not self.game or not hasattr(self.game, "make_move"):
            print("Game instance not available for move execution")
            self._deselect_point()
            return

        from_notation = self.selected_point + 1
        to_notation = to_point + 1

        print(f"Game notation: {from_notation} -> {to_notation}")
        success = self.game.make_move(from_notation, to_notation)

        if success:
            print(f"Move successful: {self.selected_point} -> {to_point}")
            self._deselect_point()

            # Check if turn should end after this move
            self._check_turn_completion()
        else:
            print(f"Move failed: {self.selected_point} -> {to_point}")

    def _execute_move_from_bar(self, to_point: int) -> None:
        """
        Execute a move from bar to destination point.

        Args:
            to_point: Destination point number (0-23)
        """
        print(f"Attempting move from bar to {to_point}")

        if not self.game or not hasattr(self.game, "make_move"):
            print("Game instance not available for move execution")
            self._deselect_point()
            return

        to_notation = to_point + 1

        print(f"Game notation: bar -> {to_notation}")
        success = self.game.make_move("bar", to_notation)

        if success:
            print(f"Move from bar successful: bar -> {to_point}")
            self._deselect_point()

            # Check if turn should end after this move
            self._check_turn_completion()
        else:
            print(f"Move from bar failed: bar -> {to_point}")

    def _execute_move_to_off(self) -> None:
        """
        Execute a bearing off move from selected point to off area.
        """
        if self.selected_point is None:
            return

        print(f"Attempting to bear off from {self.selected_point}")

        if not self.game or not hasattr(self.game, "make_move"):
            print("Game instance not available for move execution")
            self._deselect_point()
            return

        from_notation = self.selected_point + 1

        print(f"Game notation: {from_notation} -> off")
        success = self.game.make_move(from_notation, "off")

        if success:
            print(f"Bear off successful from point {self.selected_point}")
            self._deselect_point()

            # Check if turn should end after this move
            self._check_turn_completion()
        else:
            print(f"Bear off failed from point {self.selected_point}")

    def _check_turn_completion(self) -> None:
        """
        Check if the current turn is complete and switch turns if necessary.
        Turn ends when:
        - All dice have been used
        - No more valid moves are available

        Note: reset_turn_state() is called by BackgammonBoard._update_button_state()
        after the turn change is detected.
        """
        if not self.game:
            return

        # Check if all dice have been consumed
        available_moves = self.game.dice.get_available_moves()
        if not available_moves:
            print("All dice consumed - ending turn")
            self.game.complete_turn()
            # Don't reset turn state here - it will be done when button state is updated
            return

        # Check if there are any valid moves remaining
        has_moves = self.game.has_valid_moves()
        if not has_moves:
            print("No more valid moves available - ending turn")
            self.game.complete_turn()
            # Don't reset turn state here - it will be done when button state is updated
            return

        print(f"Turn continues - {len(available_moves)} dice remaining")

    def _calculate_valid_destinations(self, from_point: int) -> List[Union[int, str]]:
        """
        Calculate valid destination points for a selected checker.

        Args:
            from_point: The point number where the checker is (0-23)

        Returns:
            List of valid destination point numbers or "off" for bearing off
        """
        valid_destinations = []

        if not self.game or not hasattr(self.game, "dice"):
            return valid_destinations

        if not self.game.dice.last_roll:
            return valid_destinations

        available_moves = self.game.dice.get_available_moves()
        if not available_moves:
            return valid_destinations

        current_player = self.game.get_current_player()
        if not current_player:
            return valid_destinations

        player_color = current_player.color

        if not hasattr(self.game, "board"):
            return valid_destinations

        checkers = self.game.board.points[from_point]
        if not checkers or checkers[0].color != player_color:
            return valid_destinations

        seen_destinations = set()

        for move in available_moves:
            if player_color == "white":
                destination = from_point - move
            else:
                destination = from_point + move

            # Check for bearing off
            if (player_color == "white" and destination < 0) or (
                player_color == "black" and destination > 23
            ):
                # Check if bearing off is valid
                from_notation = from_point + 1
                if self.game.is_valid_move(from_notation, "off"):
                    if "off" not in seen_destinations:
                        valid_destinations.append("off")
                        seen_destinations.add("off")
                continue

            if destination in seen_destinations:
                continue

            seen_destinations.add(destination)

            if 0 <= destination <= 23:
                from_notation = from_point + 1
                to_notation = destination + 1

                if self.game.is_valid_move(from_notation, to_notation):
                    valid_destinations.append(destination)

        return valid_destinations

    def _calculate_valid_destinations_from_bar(self) -> List[int]:
        """
        Calculate valid destination points for a checker on the bar.

        Returns:
            List of valid destination point numbers
        """
        valid_destinations = []

        if not self.game or not hasattr(self.game, "dice"):
            return valid_destinations

        if not self.game.dice.last_roll:
            return valid_destinations

        available_moves = self.game.dice.get_available_moves()
        if not available_moves:
            return valid_destinations

        current_player = self.game.get_current_player()
        if not current_player:
            return valid_destinations

        player_color = current_player.color

        seen_destinations = set()

        for move in available_moves:
            # For white: entering from point 24 (bar) towards point 1
            # Entry points are 24, 23, 22, 21, 20, 19 (home board)
            # For black: entering from point -1 (bar) towards point 24
            # Entry points are 1, 2, 3, 4, 5, 6 (home board)

            if player_color == "white":
                # White enters from high numbers (24-move)
                destination = 24 - move
            else:
                # Black enters from low numbers (move-1)
                destination = move - 1

            if destination in seen_destinations:
                continue

            seen_destinations.add(destination)

            if 0 <= destination <= 23:
                to_notation = destination + 1

                if self.game.is_valid_move("bar", to_notation):
                    valid_destinations.append(destination)

        return valid_destinations

    def clear_selection(self) -> None:
        """Clear current selection state."""
        self.selected_point = None
        self.selected_bar = False
        self.valid_move_destinations = []

    def reset_turn_state(self) -> None:
        """Reset state for a new turn."""
        self.dice_rolled = False
        self.clear_selection()
