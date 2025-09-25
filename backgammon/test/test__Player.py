import unittest
from unittest.mock import Mock, patch
from backgammon.core import Player, Checker, Board
# pylint: disable=C0116  # many simple test methods without individual docstrings

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player_white = Player("Player1", "white")
        self.player_black = Player("Player2", "black")
        self.player_default = Player()

    def test_player_initialization_with_params(self):
        self.assertEqual(self.player_white.name, "Player1")
        self.assertEqual(self.player_white.color, "white")
        self.assertEqual(self.player_white.checkers_on_board, 15)
        self.assertEqual(self.player_white.checkers_off_board, 0)
        self.assertEqual(self.player_white.checkers_on_bar, 0)

    def test_player_initialization_default(self):
        self.assertIsNone(self.player_default.name)
        self.assertIsNone(self.player_default.color)
        self.assertEqual(self.player_default.checkers_on_board, 15)
        self.assertEqual(self.player_default.checkers_off_board, 0)
        self.assertEqual(self.player_default.checkers_on_bar, 0)

    def test_invalid_color_initialization(self):
        with self.assertRaises(ValueError):
            Player("Test", "red")
        with self.assertRaises(ValueError):
            Player("Test", "blue")

    def test_set_name(self):
        self.player_default.set_name("NewPlayer")
        self.assertEqual(self.player_default.name, "NewPlayer")

    def test_set_color(self):
        self.player_default.set_color("black")
        self.assertEqual(self.player_default.color, "black")

    def test_set_invalid_color(self):
        with self.assertRaises(ValueError):
            self.player_default.set_color("green")

    def test_move_checker_off_board(self):
        initial_on_board = self.player_white.checkers_on_board
        initial_off_board = self.player_white.checkers_off_board

        self.player_white.move_checker_off()

        self.assertEqual(self.player_white.checkers_on_board, initial_on_board - 1)
        self.assertEqual(self.player_white.checkers_off_board, initial_off_board + 1)

    def test_move_checker_off_board_no_checkers(self):
        self.player_white.checkers_on_board = 0

        with self.assertRaises(ValueError):
            self.player_white.move_checker_off()

    def test_move_checker_to_bar(self):
        initial_on_board = self.player_white.checkers_on_board
        initial_on_bar = self.player_white.checkers_on_bar

        self.player_white.move_checker_to_bar()

        self.assertEqual(self.player_white.checkers_on_board, initial_on_board - 1)
        self.assertEqual(self.player_white.checkers_on_bar, initial_on_bar + 1)

    def test_move_checker_from_bar(self):
        self.player_white.move_checker_to_bar()

        initial_on_board = self.player_white.checkers_on_board
        initial_on_bar = self.player_white.checkers_on_bar

        self.player_white.move_checker_from_bar()

        self.assertEqual(self.player_white.checkers_on_board, initial_on_board + 1)
        self.assertEqual(self.player_white.checkers_on_bar, initial_on_bar - 1)

    def test_move_checker_from_bar_no_checkers(self):
        with self.assertRaises(ValueError):
            self.player_white.move_checker_from_bar()

    def test_has_won_true(self):
        self.player_white.checkers_off_board = 15
        self.player_white.checkers_on_board = 0
        self.player_white.checkers_on_bar = 0

        self.assertTrue(self.player_white.has_won())

    def test_has_won_false(self):
        self.assertFalse(self.player_white.has_won())

        self.player_white.checkers_off_board = 10
        self.player_white.checkers_on_board = 5
        self.assertFalse(self.player_white.has_won())

    def test_has_checkers_on_bar(self):
        self.assertFalse(self.player_white.has_checkers_on_bar())

        self.player_white.move_checker_to_bar()
        self.assertTrue(self.player_white.has_checkers_on_bar())

    def test_can_bear_off_with_different_board_states(self):
        mock_board = Mock()

        # Test when all checkers are in home board
        mock_board.all_checkers_in_home_board.return_value = True
        self.assertTrue(self.player_white.can_bear_off(mock_board))
        mock_board.all_checkers_in_home_board.assert_called_with("white")

        # Test when not all checkers are in home board
        mock_board.all_checkers_in_home_board.return_value = False
        self.assertFalse(self.player_white.can_bear_off(mock_board))

    def test_get_checkers_count(self):
        total = self.player_white.get_total_checkers()
        self.assertEqual(total, 15)

        self.player_white.move_checker_off()
        total = self.player_white.get_total_checkers()
        self.assertEqual(total, 15)

    def test_get_checkers_distribution(self):
        distribution = self.player_white.get_checkers_distribution()

        self.assertEqual(distribution["on_board"], 15)
        self.assertEqual(distribution["off_board"], 0)
        self.assertEqual(distribution["on_bar"], 0)

    def test_reset_player(self):
        self.player_white.move_checker_off()
        self.player_white.move_checker_to_bar()

        self.player_white.reset()

        self.assertEqual(self.player_white.checkers_on_board, 15)
        self.assertEqual(self.player_white.checkers_off_board, 0)
        self.assertEqual(self.player_white.checkers_on_bar, 0)

    def test_get_direction(self):
        self.assertEqual(self.player_white.get_direction(), -1)

        self.assertEqual(self.player_black.get_direction(), 1)

    def test_get_home_board_range(self):
        white_home = self.player_white.get_home_board_range()
        self.assertEqual(white_home, range(1, 7))

        black_home = self.player_black.get_home_board_range()
        self.assertEqual(black_home, range(19, 25))

    def test_get_starting_position(self):
        white_start = self.player_white.get_starting_position()
        self.assertEqual(white_start, 25)

        black_start = self.player_black.get_starting_position()
        self.assertEqual(black_start, 0)

    def test_is_valid_move(self):
        mock_board = Mock()

        mock_board.is_valid_move.return_value = True
        self.assertTrue(self.player_white.is_valid_move(1, 4, mock_board))

        mock_board.is_valid_move.return_value = False
        self.assertFalse(self.player_white.is_valid_move(1, 4, mock_board))

    def test_get_possible_moves(self):
        mock_board = Mock()
        mock_dice = Mock()

        mock_board.get_possible_moves.return_value = [(1, 4), (6, 9)]

        moves = self.player_white.get_possible_moves(mock_board, mock_dice)
        self.assertEqual(moves, [(1, 4), (6, 9)])

    def test_make_move_calls_board_correctly(self):
        mock_board = Mock()
        mock_board.move_checker.return_value = True

        result = self.player_white.make_move(5, 8, mock_board)

        self.assertTrue(result)
        mock_board.move_checker.assert_called_once_with(5, 8, "white")

    def test_str_representation(self):
        player_str = str(self.player_white)
        self.assertIn("Player1", player_str)
        self.assertIn("white", player_str)

    def test_repr_representation(self):
        player_repr = repr(self.player_white)
        self.assertIn("Player", player_repr)
        self.assertIn("Player1", player_repr)
        self.assertIn("white", player_repr)

    def test_player_equality(self):
        player1 = Player("Test", "white")
        player2 = Player("Test", "white")
        player3 = Player("Other", "white")

        self.assertEqual(player1.name, player2.name)
        self.assertEqual(player1.color, player2.color)
        self.assertNotEqual(player1.name, player3.name)

    def test_copy_player(self):
        copied_player = self.player_white.copy()

        self.assertEqual(copied_player.name, self.player_white.name)
        self.assertEqual(copied_player.color, self.player_white.color)
        self.assertEqual(
            copied_player.checkers_on_board, self.player_white.checkers_on_board
        )
        self.assertIsNot(copied_player, self.player_white)

    def test_get_opponent_color(self):
        self.assertEqual(self.player_white.get_opponent_color(), "black")
        self.assertEqual(self.player_black.get_opponent_color(), "white")

    def test_checkers_invariant(self):
        total = (
            self.player_white.checkers_on_board
            + self.player_white.checkers_off_board
            + self.player_white.checkers_on_bar
        )
        self.assertEqual(total, 15)

        self.player_white.move_checker_to_bar()
        total = (
            self.player_white.checkers_on_board
            + self.player_white.checkers_off_board
            + self.player_white.checkers_on_bar
        )
        self.assertEqual(total, 15)

        self.player_white.move_checker_from_bar()
        self.player_white.move_checker_off()
        total = (
            self.player_white.checkers_on_board
            + self.player_white.checkers_off_board
            + self.player_white.checkers_on_bar
        )
        self.assertEqual(total, 15)


if __name__ == "__main__":
    unittest.main()
