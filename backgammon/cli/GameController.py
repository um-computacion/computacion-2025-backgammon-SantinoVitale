"""
GameController class for Backgammon game.
Responsible only for managing game state and flow.
"""

from typing import List, Tuple, Union, Optional


class GameController:
    """
    Handles game state management for Backgammon.

    Single Responsibility: Only manages game state and coordinates game flow.
    """

    def __init__(self, game) -> None:
        """
        Initialize the GameController.

        Args:
            game: BackgammonGame instance
        """
        self.game = game

    def set_game(self, game) -> None:
        """
        Set the BackgammonGame instance.

        Args:
            game: BackgammonGame instance
        """
        self.game = game

    def setup_game(self, player1_name: str, player2_name: str) -> None:
        """
        Setup players and start the game.

        Args:
            player1_name: Name of white player
            player2_name: Name of black player
        """
        if hasattr(self.game, "setup_players"):
            self.game.setup_players(player1_name, player2_name)
        if hasattr(self.game, "start_game"):
            self.game.start_game()

    def is_game_over(self) -> bool:
        """
        Check if the game is over.

        Returns:
            True if game is over, False otherwise
        """
        if hasattr(self.game, "is_game_over"):
            return self.game.is_game_over()
        return False

    def get_winner(self):
        """
        Get the winner of the game.

        Returns:
            Player object who won, or None if no winner yet
        """
        if hasattr(self.game, "get_winner"):
            return self.game.get_winner()
        return None

    def get_current_player(self):
        """
        Get the current player.

        Returns:
            Current player object
        """
        if hasattr(self.game, "get_current_player"):
            return self.game.get_current_player()
        return None

    def get_board(self):
        """
        Get the game board.

        Returns:
            Board object
        """
        if hasattr(self.game, "board"):
            return self.game.board
        return None

    def roll_dice(self) -> Optional[List[int]]:
        """
        Roll the dice for the current turn.

        Returns:
            List of dice values [die1, die2]
        """
        if hasattr(self.game, "roll_dice"):
            return self.game.roll_dice()
        return None

    def get_dice_values(self) -> Optional[List[int]]:
        """
        Get the current dice values.

        Returns:
            List of dice values
        """
        if hasattr(self.game, "dice") and hasattr(self.game.dice, "last_roll"):
            return self.game.dice.last_roll
        return None

    def get_available_moves(self) -> Optional[List[int]]:
        """
        Get available move distances.

        Returns:
            List of available move distances
        """
        if hasattr(self.game, "dice") and hasattr(
            self.game.dice, "get_available_moves"
        ):
            return self.game.dice.get_available_moves()
        return None

    def has_valid_moves(self) -> bool:
        """
        Check if the current player has valid moves.

        Returns:
            True if player has valid moves, False otherwise
        """
        if hasattr(self.game, "has_valid_moves"):
            return self.game.has_valid_moves()
        return False

    def get_possible_moves(self) -> List[Tuple[Union[int, str], Union[int, str]]]:
        """
        Get all possible moves for the current player.

        Returns:
            List of (from_pos, to_pos) tuples
        """
        if hasattr(self.game, "get_possible_moves"):
            return self.game.get_possible_moves()
        return []

    def make_move(self, from_pos: Union[int, str], to_pos: Union[int, str]) -> bool:
        """
        Attempt to make a move.

        Args:
            from_pos: Starting position
            to_pos: Ending position

        Returns:
            True if move was successful, False otherwise
        """
        if hasattr(self.game, "make_move"):
            return self.game.make_move(from_pos, to_pos)
        return False

    def calculate_move_distance(
        self, from_pos: Union[int, str], to_pos: Union[int, str]
    ) -> int:
        """
        Calculate the distance of a move.

        Args:
            from_pos: Starting position
            to_pos: Ending position

        Returns:
            Move distance
        """
        if hasattr(self.game, "calculate_move_distance"):
            return self.game.calculate_move_distance(from_pos, to_pos)
        return 0

    def use_dice_move(self, distance: int) -> bool:
        """
        Use a dice move.

        Args:
            distance: Distance to use

        Returns:
            True if move was used, False otherwise
        """
        if hasattr(self.game, "dice") and hasattr(self.game.dice, "use_move"):
            return self.game.dice.use_move(distance)
        return False

    def has_moves_remaining(self) -> bool:
        """
        Check if there are dice moves remaining.

        Returns:
            True if moves remain, False otherwise
        """
        if hasattr(self.game, "dice") and hasattr(self.game.dice, "has_moves"):
            return self.game.dice.has_moves()
        return False

    def can_continue_turn(self) -> bool:
        """
        Check if the current turn can continue.

        Returns:
            True if turn can continue, False otherwise
        """
        if hasattr(self.game, "can_continue_turn"):
            return self.game.can_continue_turn()
        return self.has_moves_remaining() and self.has_valid_moves()

    def complete_turn(self) -> None:
        """Complete the current turn and switch players."""
        if hasattr(self.game, "complete_turn"):
            self.game.complete_turn()
        elif hasattr(self.game, "switch_turns"):
            self.game.switch_turns()

    def get_statistics(self) -> dict:
        """
        Get game statistics.

        Returns:
            Dictionary of game statistics
        """
        if hasattr(self.game, "get_statistics"):
            return self.game.get_statistics()
        return {}
