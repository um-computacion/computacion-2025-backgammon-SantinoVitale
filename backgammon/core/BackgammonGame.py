"""
BackgammonGame class - Main game orchestrator for Backgammon.
Manages the complete game flow, players, board, dice, and UI interactions.
"""

# pylint: disable=invalid-name  # BackgammonGame follows PascalCase class naming convention

import time
from typing import List, Tuple, Union, Dict, Any, Optional
from .Board import Board
from .Player import Player
from .Dice import Dice


class BackgammonGame:  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """
    Main game class that orchestrates the entire Backgammon game.

    Manages:
    - Game initialization and setup
    - Player management and turns
    - Game flow and state
    - UI interactions (CLI/Pygame)
    - Game rules enforcement
    - Save/load functionality
    """

    def __init__(self, ui=None) -> None:
        """
        Initialize the BackgammonGame.

        Args:
            ui: User interface instance (CLI, PygameUI, etc.)
        """
        self.board = Board()
        self.dice = Dice()
        self.players: List[Player] = []
        self.current_player_index = 0
        self.ui = ui
        self.is_started = False
        self.is_paused = False
        self.move_history: List[Tuple[Union[int, str], Union[int, str], str]] = []
        self.move_count = 0
        self.start_time = None
        self.end_time = None

    def set_ui(self, ui) -> None:
        """
        Set the user interface for the game.

        Args:
            ui: User interface instance (CLI, PygameUI, etc.)
        """
        self.ui = ui
        # If UI has a set_game method, connect it to this game
        if hasattr(ui, "set_game"):
            ui.set_game(self)

    def setup_board(self) -> None:
        """Setup the board with initial Backgammon position."""
        self.board.setup_initial_position()

    def setup_players(self, player1_name: str = None, player2_name: str = None) -> None:
        """
        Setup two players for the game.

        Args:
            player1_name: Name for white player (optional)
            player2_name: Name for black player (optional)
        """
        if player1_name is None:
            player1_name = "White Player"
        if player2_name is None:
            player2_name = "Black Player"

        self.players = [Player(player1_name, "white"), Player(player2_name, "black")]

    def start_game(self) -> None:
        """Start a new game by setting up board and players."""
        self.setup_board()
        self.setup_players()
        self.is_started = True
        self.start_time = time.time()

        # Display initial board state
        if self.ui:
            self.ui.display_message("Game started! Here's the initial board:")
            self.ui.display_board(self.board)

    def switch_turns(self) -> None:
        """Switch to the next player's turn."""
        self.current_player_index = (self.current_player_index + 1) % 2

    def get_current_player(self) -> Player:
        """
        Get the current player.

        Returns:
            Current Player object
        """
        return self.players[self.current_player_index]

    def get_opponent_player(self) -> Player:
        """
        Get the opponent player.

        Returns:
            Opponent Player object
        """
        return self.players[(self.current_player_index + 1) % 2]

    def roll_dice(self) -> List[int]:
        """
        Roll the dice for the current turn.

        Returns:
            List of dice values [die1, die2]
        """
        return self.dice.roll()

    def is_game_over(self) -> bool:
        """
        Check if the game is over.

        Returns:
            True if any player has won, False otherwise
        """
        return any(player.has_won() for player in self.players)

    def get_winner(self) -> Optional[Player]:
        """
        Get the winning player.

        Returns:
            Player object if someone has won, None otherwise
        """
        for player in self.players:
            if player.has_won():
                return player
        return None

    def make_move(self, from_pos: Union[int, str], to_pos: Union[int, str]) -> bool:
        """
        Make a move for the current player.

        Args:
            from_pos: Starting position (int 0-23, "bar")
            to_pos: Ending position (int 0-23, "off")

        Returns:
            True if move was successful, False otherwise
        """
        current_player = self.get_current_player()

        # Handle different types of moves
        success = False

        if from_pos == "bar":
            # Move from bar to board
            if isinstance(to_pos, int):
                # Convert from human notation (1-24) to board indexing (0-23)
                if to_pos < 1 or to_pos > 24:
                    return False
                board_pos = to_pos - 1
                success = self.board.move_from_bar(current_player.color, board_pos)
        elif to_pos == "off":
            # Bear off move
            if isinstance(from_pos, int):
                # Convert from human notation (1-24) to board indexing (0-23)
                if from_pos < 1 or from_pos > 24:
                    return False
                board_pos = from_pos - 1
                success = self.board.bear_off(board_pos, current_player.color)
        else:
            # Normal point-to-point move
            if isinstance(from_pos, int) and isinstance(to_pos, int):
                # Convert from human notation (1-24) to board indexing (0-23)
                if from_pos < 1 or from_pos > 24 or to_pos < 1 or to_pos > 24:
                    return False
                from_board = from_pos - 1
                to_board = to_pos - 1
                success = self.board.move_checker(
                    from_board, to_board, current_player.color
                )

        if success:
            self.move_history.append((from_pos, to_pos, current_player.color))
            self.move_count += 1

        return success

    def _calculate_move_distance(
        self, from_pos: Union[int, str], to_pos: Union[int, str]
    ) -> int:
        """
        Calculate the distance of a move for dice consumption.

        Args:
            from_pos: Starting position
            to_pos: Ending position

        Returns:
            int: Distance of the move
        """
        current_player = self.get_current_player()

        if isinstance(from_pos, int) and isinstance(to_pos, int):
            # For regular moves, consider direction of play
            if current_player.color == "white":
                # White moves from higher to lower numbers (24→1)
                if from_pos > to_pos:
                    return from_pos - to_pos
                else:
                    return 0  # Invalid direction for white
            else:
                # Black moves from lower to higher numbers (1→24)
                if to_pos > from_pos:
                    return to_pos - from_pos
                else:
                    return 0  # Invalid direction for black
        elif from_pos == "bar" and isinstance(to_pos, int):
            # For bar moves, distance is based on entry point
            if current_player.color == "white":
                # White enters from point 25 (conceptually) to to_pos
                return 25 - to_pos
            else:
                # Black enters from point 0 (conceptually) to to_pos
                return to_pos
        elif isinstance(from_pos, int) and to_pos == "off":
            # For bearing off, distance is from point to off
            if current_player.color == "white":
                # White bears off from from_pos to 0
                return from_pos
            else:
                # Black bears off from from_pos to 25
                return 25 - from_pos
        return 0

    def calculate_move_distance(
        self, from_pos: Union[int, str], to_pos: Union[int, str]
    ) -> int:
        """
        Public method to calculate move distance.

        Args:
            from_pos: Starting position
            to_pos: Ending position

        Returns:
            Distance of the move
        """
        return self._calculate_move_distance(from_pos, to_pos)

    def is_valid_move(self, from_pos: Union[int, str], to_pos: Union[int, str]) -> bool:
        """
        Check if a move is valid.

        Args:
            from_pos: Starting position (1-24 or "bar")
            to_pos: Ending position (1-24 or "off")

        Returns:
            True if move is valid, False otherwise
        """
        current_player = self.get_current_player()

        # Calculate move distance using the proper method
        distance = self._calculate_move_distance(from_pos, to_pos)

        # First check if dice allows this move
        if not self.dice.can_use_move(distance):
            return False

        # Convert coordinates for board validation
        # For board methods, we need to check the actual move mechanics
        if from_pos == "bar":
            if isinstance(to_pos, int):
                if to_pos < 1 or to_pos > 24:
                    return False
                board_pos = to_pos - 1
                return len(
                    self.board.bar[current_player.color]
                ) > 0 and self.board.is_point_available(board_pos, current_player.color)
        elif to_pos == "off":
            if isinstance(from_pos, int):
                if from_pos < 1 or from_pos > 24:
                    return False
                board_pos = from_pos - 1
                return (
                    self.board.can_bear_off(current_player.color)
                    and len(self.board.points[board_pos]) > 0
                    and self.board.get_point_top_color(board_pos)
                    == current_player.color
                )
        else:
            # Normal point-to-point move
            if isinstance(from_pos, int) and isinstance(to_pos, int):
                if from_pos < 1 or from_pos > 24 or to_pos < 1 or to_pos > 24:
                    return False
                from_board = from_pos - 1
                to_board = to_pos - 1
                return (
                    len(self.board.points[from_board]) > 0
                    and self.board.get_point_top_color(from_board)
                    == current_player.color
                    and self.board.is_point_available(to_board, current_player.color)
                )

        return False

    def get_possible_moves(self) -> List[Tuple[Union[int, str], Union[int, str]]]:
        """
        Get all possible moves for the current player.

        Returns:
            List of tuples representing possible moves
        """
        current_player = self.get_current_player()
        return self.board.get_possible_moves(
            current_player.color, self.dice.get_available_moves()
        )

    def has_valid_moves(self) -> bool:
        """
        Check if the current player has any valid moves.

        Returns:
            True if valid moves exist, False otherwise
        """
        return len(self.get_possible_moves()) > 0

    def play_turn(self) -> None:
        """
        Initialize a turn for the current player by rolling dice.

        This is a pure game logic method that only handles:
        - Rolling dice if no moves are available
        - Setting up the turn state

        UI interactions should be handled by the CLI.
        """
        # Setup players if they don't exist (for testing purposes)
        if not self.players:
            self.setup_players()

        # Roll dice only if no moves are available (start of turn)
        if not self.dice.get_available_moves():
            self.roll_dice()

    def can_continue_turn(self) -> bool:
        """
        Check if the current player can continue their turn.

        Returns:
            True if player has available dice and valid moves, False otherwise
        """
        return self.dice.get_available_moves() and self.has_valid_moves()

    def complete_turn(self) -> None:
        """
        Complete the current turn and switch to next player.

        Should be called when all dice are used or no more valid moves available.
        """
        # Reset dice for next turn
        self.dice.reset()
        self.switch_turns()

    def play_game(self) -> None:
        """
        Play the complete game until someone wins.

        This method is now deprecated in favor of CLI.run_game().
        Kept for backward compatibility with existing tests.
        """
        while not self.is_game_over():
            if not self.is_paused:
                self.play_turn()
                # In the new architecture, this would be handled by CLI
                # This is a simplified version for testing compatibility
                if not self.can_continue_turn():
                    self.complete_turn()
            self.end_time = time.time()

    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.board.reset()
        self.dice.reset()
        for player in self.players:
            player.reset()
        self.current_player_index = 0
        self.is_started = False
        self.is_paused = False
        self.move_history.clear()
        self.move_count = 0
        self.start_time = None
        self.end_time = None

    def pause_game(self) -> None:
        """Pause the game."""
        self.is_paused = True

    def resume_game(self) -> None:
        """Resume the game."""
        self.is_paused = False

    def get_game_state(self) -> Dict[str, Any]:
        """
        Get the complete game state for saving.

        Returns:
            Dictionary containing all game state information
        """
        return {
            "board": self.board.get_state(),
            "dice": self.dice.get_state(),
            "players": [player.get_state() for player in self.players],
            "current_player_index": self.current_player_index,
            "is_started": self.is_started,
            "is_paused": self.is_paused,
            "move_history": self.move_history,
            "move_count": self.move_count,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    def set_game_state(self, state: Dict[str, Any]) -> None:
        """
        Load game state from a dictionary.

        Args:
            state: Dictionary containing game state information
        """
        self.board.set_state(state["board"])
        self.dice.set_state(state["dice"])

        # Restore players
        for i, player_state in enumerate(state["players"]):
            self.players[i].set_state(player_state)

        self.current_player_index = state["current_player_index"]
        self.is_started = state["is_started"]
        self.is_paused = state.get("is_paused", False)
        self.move_history = state.get("move_history", [])
        self.move_count = state.get("move_count", 0)
        self.start_time = state.get("start_time")
        self.end_time = state.get("end_time")

    def validate_move_coordinates(  # pylint: disable=too-many-return-statements
        self, from_pos: Union[int, str], to_pos: Union[int, str]
    ) -> bool:
        """
        Validate move coordinates.

        Args:
            from_pos: Starting position
            to_pos: Ending position

        Returns:
            True if coordinates are valid, False otherwise
        """
        # Validate from_pos
        if isinstance(from_pos, int):
            if from_pos < 1 or from_pos > 24:
                return False
        elif isinstance(from_pos, str):
            if from_pos not in ["bar"]:
                return False
        else:
            return False

        # Validate to_pos
        if isinstance(to_pos, int):
            if to_pos < 1 or to_pos > 24:
                return False
        elif isinstance(to_pos, str):
            if to_pos not in ["off"]:
                return False
        else:
            return False

        return True

    def get_game_statistics(self) -> Dict[str, Any]:
        """
        Get game statistics.

        Returns:
            Dictionary containing game statistics
        """
        duration = 0
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
        elif self.start_time:
            duration = time.time() - self.start_time

        return {
            "moves": self.move_count,
            "duration": int(duration),
            "winner": self.get_winner().name if self.get_winner() else None,
            "current_player": self.get_current_player().name if self.players else None,
        }

    def undo_last_move(self) -> bool:
        """
        Undo the last move.

        Returns:
            True if undo was successful, False if no moves to undo
        """
        if not self.move_history:
            return False

        # Remove last move from history
        last_move = self.move_history.pop()
        from_pos, to_pos, color = last_move

        # Reverse the move on the board (simplified implementation)
        # In a full implementation, this would need to handle all edge cases
        self.board.move_checker(to_pos, from_pos, color)
        self.move_count -= 1

        return True

    def copy(self) -> "BackgammonGame":
        """
        Create a copy of the game state.

        Returns:
            New BackgammonGame instance with copied state
        """
        new_game = BackgammonGame(self.ui)
        new_game.set_game_state(self.get_game_state())
        return new_game

    def __str__(self) -> str:
        """String representation of the game."""
        status = "Started" if self.is_started else "Not Started"
        if self.is_paused:
            status += " (Paused)"

        current_player = self.get_current_player().name if self.players else "None"

        return (
            f"BackgammonGame(status={status}, "
            f"current_player={current_player}, "
            f"moves={self.move_count})"
        )

    def __repr__(self) -> str:
        """Repr representation of the game."""
        ui_type = type(self.ui).__name__ if self.ui else "None"
        return (
            f"BackgammonGame(ui={ui_type}, "
            f"is_started={self.is_started}, "
            f"current_player_index={self.current_player_index})"
        )
