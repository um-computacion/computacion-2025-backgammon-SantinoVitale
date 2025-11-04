"""
Unit tests for GameController class.
Tests game state management functionality following SOLID principles.
"""

import unittest
from unittest.mock import Mock
from backgammon.cli.game_controller import GameController


class TestGameController(unittest.TestCase):
    """Test cases for GameController class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_game = Mock()
        self.controller = GameController(self.mock_game)

    def test_init(self):
        """Test GameController initialization."""
        controller = GameController(self.mock_game)
        self.assertIsInstance(controller, GameController)
        self.assertEqual(controller.game, self.mock_game)

    def test_set_game(self):
        """Test setting a new game instance."""
        new_game = Mock()
        self.controller.set_game(new_game)
        self.assertEqual(self.controller.game, new_game)

    def test_setup_game(self):
        """Test setting up the game."""
        self.mock_game.setup_players = Mock()
        self.mock_game.setup_board = Mock()
        self.mock_game.is_started = False
        self.mock_game.start_time = None

        self.controller.setup_game("Player1", "Player2")

        self.mock_game.setup_players.assert_called_once_with("Player1", "Player2")
        self.mock_game.setup_board.assert_called_once()
        self.assertTrue(self.mock_game.is_started)
        self.assertIsNotNone(self.mock_game.start_time)

    def test_setup_game_no_methods(self):
        """Test setup_game when game has no setup methods."""
        game_no_methods = Mock(spec=[])
        controller = GameController(game_no_methods)
        controller.setup_game("Player1", "Player2")

    def test_is_game_over_true(self):
        """Test is_game_over returns True."""
        self.mock_game.is_game_over = Mock(return_value=True)
        self.assertTrue(self.controller.is_game_over())

    def test_is_game_over_false(self):
        """Test is_game_over returns False."""
        self.mock_game.is_game_over = Mock(return_value=False)
        self.assertFalse(self.controller.is_game_over())

    def test_is_game_over_no_method(self):
        """Test is_game_over when game has no method."""
        game_no_method = Mock(spec=[])
        controller = GameController(game_no_method)
        self.assertFalse(controller.is_game_over())

    def test_get_winner(self):
        """Test getting the winner."""
        mock_player = Mock()
        self.mock_game.get_winner = Mock(return_value=mock_player)

        winner = self.controller.get_winner()
        self.assertEqual(winner, mock_player)

    def test_get_winner_no_method(self):
        """Test get_winner when game has no method."""
        game_no_method = Mock(spec=[])
        controller = GameController(game_no_method)
        self.assertIsNone(controller.get_winner())

    def test_get_current_player(self):
        """Test getting the current player."""
        mock_player = Mock()
        self.mock_game.get_current_player = Mock(return_value=mock_player)

        player = self.controller.get_current_player()
        self.assertEqual(player, mock_player)

    def test_get_board(self):
        """Test getting the board."""
        mock_board = Mock()
        self.mock_game.board = mock_board

        board = self.controller.get_board()
        self.assertEqual(board, mock_board)

    def test_roll_dice(self):
        """Test rolling dice."""
        self.mock_game.roll_dice = Mock(return_value=[3, 5])

        dice_values = self.controller.roll_dice()
        self.assertEqual(dice_values, [3, 5])

    def test_get_dice_values(self):
        """Test getting dice values."""
        self.mock_game.dice = Mock()
        self.mock_game.dice.last_roll = [2, 4]

        values = self.controller.get_dice_values()
        self.assertEqual(values, [2, 4])

    def test_get_available_moves(self):
        """Test getting available moves."""
        self.mock_game.dice = Mock()
        self.mock_game.dice.get_available_moves = Mock(return_value=[3, 5])

        moves = self.controller.get_available_moves()
        self.assertEqual(moves, [3, 5])

    def test_has_valid_moves_true(self):
        """Test has_valid_moves returns True."""
        self.mock_game.has_valid_moves = Mock(return_value=True)

        self.assertTrue(self.controller.has_valid_moves())

    def test_has_valid_moves_false(self):
        """Test has_valid_moves returns False."""
        self.mock_game.has_valid_moves = Mock(return_value=False)

        self.assertFalse(self.controller.has_valid_moves())

    def test_get_possible_moves(self):
        """Test getting possible moves."""
        expected_moves = [(1, 5), (12, 8)]
        self.mock_game.get_possible_moves = Mock(return_value=expected_moves)

        moves = self.controller.get_possible_moves()
        self.assertEqual(moves, expected_moves)

    def test_get_possible_moves_no_method(self):
        """Test get_possible_moves when game has no method."""
        game_no_method = Mock(spec=[])
        controller = GameController(game_no_method)
        self.assertEqual(controller.get_possible_moves(), [])

    def test_make_move_success(self):
        """Test making a successful move."""
        self.mock_game.make_move = Mock(return_value=True)

        result = self.controller.make_move(12, 8)
        self.assertTrue(result)
        self.mock_game.make_move.assert_called_once_with(12, 8)

    def test_make_move_failure(self):
        """Test making an unsuccessful move."""
        self.mock_game.make_move = Mock(return_value=False)

        result = self.controller.make_move(12, 8)
        self.assertFalse(result)

    def test_calculate_move_distance(self):
        """Test calculating move distance."""
        self.mock_game.calculate_move_distance = Mock(return_value=4)

        distance = self.controller.calculate_move_distance(12, 8)
        self.assertEqual(distance, 4)

    def test_use_dice_move(self):
        """Test using a dice move."""
        self.mock_game.dice = Mock()
        self.mock_game.dice.use_move = Mock(return_value=True)

        result = self.controller.use_dice_move(4)
        self.assertTrue(result)

    def test_has_moves_remaining_true(self):
        """Test has_moves_remaining returns True."""
        self.mock_game.dice = Mock()
        self.mock_game.dice.has_moves = Mock(return_value=True)

        self.assertTrue(self.controller.has_moves_remaining())

    def test_has_moves_remaining_false(self):
        """Test has_moves_remaining returns False."""
        self.mock_game.dice = Mock()
        self.mock_game.dice.has_moves = Mock(return_value=False)

        self.assertFalse(self.controller.has_moves_remaining())

    def test_can_continue_turn_with_method(self):
        """Test can_continue_turn when game has method."""
        self.mock_game.can_continue_turn = Mock(return_value=True)

        self.assertTrue(self.controller.can_continue_turn())

    def test_can_continue_turn_without_method(self):
        """Test can_continue_turn fallback logic."""
        game = Mock(spec=["dice", "has_valid_moves"])
        game.dice = Mock()
        game.dice.has_moves = Mock(return_value=True)
        game.has_valid_moves = Mock(return_value=True)

        controller = GameController(game)
        self.assertTrue(controller.can_continue_turn())

    def test_complete_turn_with_complete_turn_method(self):
        """Test complete_turn when game has complete_turn method."""
        self.mock_game.complete_turn = Mock()

        self.controller.complete_turn()
        self.mock_game.complete_turn.assert_called_once()

    def test_complete_turn_with_switch_turns_method(self):
        """Test complete_turn fallback to switch_turns."""
        game = Mock(spec=["switch_turns"])
        game.switch_turns = Mock()

        controller = GameController(game)
        controller.complete_turn()
        game.switch_turns.assert_called_once()

    def test_get_statistics(self):
        """Test getting game statistics."""
        stats = {"moves": 10, "captures": 2}
        self.mock_game.get_statistics = Mock(return_value=stats)

        result = self.controller.get_statistics()
        self.assertEqual(result, stats)

    def test_get_statistics_no_method(self):
        """Test get_statistics when game has no method."""
        game_no_method = Mock(spec=[])
        controller = GameController(game_no_method)
        self.assertEqual(controller.get_statistics(), {})


if __name__ == "__main__":
    unittest.main()
