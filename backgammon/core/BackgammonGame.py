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
from .CLI import CLI


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

    def __init__(self, ui_mode: str = "cli") -> None:
        """
        Initialize the BackgammonGame.

        Args:
            ui_mode: Interface mode ("cli" or "pygame")
        """
        self.board = Board()
        self.dice = Dice()
        self.players: List[Player] = []
        self.current_player_index = 0
        self.ui_mode = ui_mode
        self.ui = None
        self.is_started = False
        self.is_paused = False
        self.move_history: List[Tuple[Union[int, str], Union[int, str], str]] = []
        self.move_count = 0
        self.start_time = None
        self.end_time = None

        self.initialize_ui()

    def initialize_ui(self) -> None:
        """Initialize the user interface based on ui_mode."""
        if self.ui_mode == "cli":
            self.ui = CLI()
        elif self.ui_mode == "pygame":
            # For now, we'll use CLI as a placeholder for PygameUI
            # This will be replaced when PygameUI is implemented
            self.ui = CLI()  # Temporary placeholder
        else:
            self.ui = CLI()  # Default to CLI

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
            from_pos: Starting position
            to_pos: Ending position

        Returns:
            True if move was successful, False otherwise
        """
        current_player = self.get_current_player()
        success = self.board.move_checker(from_pos, to_pos, current_player.color)

        if success:
            self.move_history.append((from_pos, to_pos, current_player.color))
            self.move_count += 1

        return success

    def is_valid_move(self, from_pos: Union[int, str], to_pos: Union[int, str]) -> bool:
        """
        Check if a move is valid.

        Args:
            from_pos: Starting position
            to_pos: Ending position

        Returns:
            True if move is valid, False otherwise
        """
        current_player = self.get_current_player()

        # Calculate move distance
        if isinstance(from_pos, int) and isinstance(to_pos, int):
            distance = abs(to_pos - from_pos)
        else:
            # Handle special cases like bar/off
            distance = 1  # Simplified for now

        return self.board.is_valid_move(
            from_pos, to_pos, current_player.color
        ) and self.dice.can_use_move(distance)

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
        """Play a complete turn for the current player."""
        # Setup players if they don't exist (for testing purposes)
        if not self.players:
            self.setup_players()

        current_player = self.get_current_player()

        # Roll dice
        dice_values = self.roll_dice()
        if self.ui:
            self.ui.display_current_player(current_player)
            self.ui.display_dice_roll(dice_values)

        # Check if player has valid moves
        if not self.has_valid_moves():
            if self.ui:
                self.ui.display_message("No valid moves available. Turn skipped.")
            self.switch_turns()
            return

        # Get move from player
        if self.ui:
            from_pos, to_pos = self.ui.get_move_input()

            # Attempt to make the move
            if self.make_move(from_pos, to_pos):
                if self.ui:
                    self.ui.display_message(f"Move successful: {from_pos} to {to_pos}")
                # Use dice move
                if isinstance(from_pos, int) and isinstance(to_pos, int):
                    distance = abs(to_pos - from_pos)
                    self.dice.use_move(distance)
            else:
                if self.ui:
                    self.ui.display_error("Invalid move. Try again.")
                return  # Don't switch turns on invalid move

        self.switch_turns()

    def play_game(self) -> None:
        """Play the complete game until someone wins."""
        while not self.is_game_over():
            if not self.is_paused:
                self.play_turn()

        winner = self.get_winner()
        if winner and self.ui:
            self.ui.display_winner(winner)
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
        new_game = BackgammonGame(self.ui_mode)
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
        return (
            f"BackgammonGame(ui_mode='{self.ui_mode}', "
            f"is_started={self.is_started}, "
            f"current_player_index={self.current_player_index})"
        )
