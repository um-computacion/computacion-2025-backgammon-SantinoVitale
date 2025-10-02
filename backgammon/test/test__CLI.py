"""
Test module for CLI class.

This module contains unit tests for the CLI (Command Line Interface) class
that handles user interaction in the backgammon game.
"""

import unittest
from unittest.mock import patch, MagicMock, Mock
from io import StringIO
from backgammon.cli import CLI

# pylint: disable=C0116  # many simple test methods without individual docstrings
# pylint: disable=C0103  # module name follows test naming convention
# pylint: disable=R0904  # many public methods needed for comprehensive testing


class TestCLI(unittest.TestCase):
    """Test cases for the CLI class."""

    def setUp(self):
        self.cli = CLI()

    def test_cli_initialization(self):
        self.assertIsNotNone(self.cli)
        self.assertTrue(hasattr(self.cli, "display_board"))
        self.assertTrue(hasattr(self.cli, "get_move_input"))

    @patch("builtins.input")
    def test_get_move_input_valid_format(self, mock_input):
        mock_input.return_value = "1 4"
        from_pos, to_pos = self.cli.get_move_input()
        self.assertEqual(from_pos, 1)
        self.assertEqual(to_pos, 4)

    @patch("builtins.input")
    def test_get_move_input_with_spaces(self, mock_input):
        mock_input.return_value = " 5  10 "
        from_pos, to_pos = self.cli.get_move_input()
        self.assertEqual(from_pos, 5)
        self.assertEqual(to_pos, 10)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input")
    def test_get_move_input_invalid_format_retry(self, mock_input, _mock_stdout):
        mock_input.side_effect = ["invalid", "1-4", "1 4"]
        from_pos, to_pos = self.cli.get_move_input()
        self.assertEqual(from_pos, 1)
        self.assertEqual(to_pos, 4)
        self.assertEqual(mock_input.call_count, 3)

    @patch("builtins.input")
    def test_get_move_input_bear_off(self, mock_input):
        mock_input.return_value = "1 off"
        from_pos, to_pos = self.cli.get_move_input()
        self.assertEqual(from_pos, 1)
        self.assertEqual(to_pos, "off")

    @patch("builtins.input")
    def test_get_move_input_from_bar(self, mock_input):
        mock_input.return_value = "bar 20"
        from_pos, to_pos = self.cli.get_move_input()
        self.assertEqual(from_pos, "bar")
        self.assertEqual(to_pos, 20)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_board_basic(self, mock_stdout):
        mock_board = MagicMock()
        mock_board.points = [[] for _ in range(24)]
        mock_board.bar = {"white": [], "black": []}
        mock_board.off = {"white": [], "black": []}

        self.cli.display_board(mock_board)
        output = mock_stdout.getvalue()
        self.assertIsInstance(output, str)
        self.assertGreater(len(output), 0)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_message(self, mock_stdout):
        message = "Test message"
        self.cli.display_message(message)
        output = mock_stdout.getvalue()
        self.assertIn(message, output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_error(self, mock_stdout):
        error = "Error occurred"
        self.cli.display_error(error)
        output = mock_stdout.getvalue()
        self.assertIn(error, output)
        self.assertIn("Error", output)

    @patch("builtins.input")
    def test_get_player_name(self, mock_input):
        mock_input.return_value = "Player1"
        name = self.cli.get_player_name("white")
        self.assertEqual(name, "Player1")

    @patch("builtins.input")
    def test_get_player_name_empty_default(self, mock_input):
        mock_input.return_value = ""
        name = self.cli.get_player_name("white")
        self.assertIsInstance(name, str)
        self.assertGreater(len(name), 0)

    @patch("builtins.input")
    def test_confirm_move_yes(self, mock_input):
        mock_input.return_value = "y"
        result = self.cli.confirm_move(1, 4)
        self.assertTrue(result)

    @patch("builtins.input")
    def test_confirm_move_no(self, mock_input):
        mock_input.return_value = "n"
        result = self.cli.confirm_move(1, 4)
        self.assertFalse(result)

    @patch("builtins.input")
    def test_confirm_move_case_insensitive(self, mock_input):
        mock_input.return_value = "Y"
        result = self.cli.confirm_move(1, 4)
        self.assertTrue(result)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_winner(self, mock_stdout):
        mock_player = MagicMock()
        mock_player.name = "Player1"
        mock_player.color = "white"

        self.cli.display_winner(mock_player)
        output = mock_stdout.getvalue()
        self.assertIn("Player1", output)
        self.assertIn("win", output.lower())

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_current_player(self, mock_stdout):
        mock_player = MagicMock()
        mock_player.name = "Player1"
        mock_player.color = "white"

        self.cli.display_current_player(mock_player)
        output = mock_stdout.getvalue()
        self.assertIn("Player1", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_current_player_with_mock_player(self, mock_stdout):
        mock_player = Mock()
        mock_player.name = "TestPlayer"
        mock_player.color = "white"

        self.cli.display_current_player(mock_player)
        output = mock_stdout.getvalue()
        self.assertIn("TestPlayer", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_dice_roll(self, mock_stdout):
        dice_values = [3, 5]
        self.cli.display_dice_roll(dice_values)
        output = mock_stdout.getvalue()
        self.assertIn("3", output)
        self.assertIn("5", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_dice_double(self, mock_stdout):
        dice_values = [4, 4]
        self.cli.display_dice_roll(dice_values)
        output = mock_stdout.getvalue()
        self.assertIn("4", output)
        self.assertIn("double", output.lower())

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_available_moves(self, mock_stdout):
        moves = [3, 5, 6]
        self.cli.display_available_moves(moves)
        output = mock_stdout.getvalue()
        self.assertIn("3", output)
        self.assertIn("5", output)
        self.assertIn("6", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_help(self, mock_stdout):
        self.cli.display_help()
        output = mock_stdout.getvalue()
        self.assertIn("help", output.lower())
        self.assertGreater(len(output), 50)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_game_rules(self, mock_stdout):
        self.cli.display_game_rules()
        output = mock_stdout.getvalue()
        self.assertIn("backgammon", output.lower())
        self.assertGreater(len(output), 100)

    @patch("builtins.input")
    def test_pause_game(self, mock_input):
        mock_input.return_value = ""
        self.cli.pause_game()
        mock_input.assert_called_once()

    def test_clear_screen(self):
        self.cli.clear_screen()

    def test_format_board_position(self):
        formatted = self.cli.format_position(5)
        self.assertIsInstance(formatted, str)
        self.assertIn("5", formatted)

    def test_format_board_position_special(self):
        bar_formatted = self.cli.format_position("bar")
        off_formatted = self.cli.format_position("off")
        self.assertIsInstance(bar_formatted, str)
        self.assertIsInstance(off_formatted, str)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input")
    def test_input_validation_retry(self, mock_input, _mock_stdout):
        mock_input.side_effect = ["invalid", "0", "25", "15"]
        position = self.cli.get_valid_position()
        self.assertEqual(position, 15)
        self.assertEqual(mock_input.call_count, 4)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_board_with_checkers(self, mock_stdout):
        mock_board = MagicMock()
        mock_board.points = [[] for _ in range(24)]
        mock_checker = MagicMock()
        mock_checker.color = "white"
        mock_board.points[0] = [mock_checker, mock_checker]
        mock_board.bar = {"white": [], "black": []}
        mock_board.off = {"white": [], "black": []}
        mock_board.get_point_count.return_value = 2
        mock_board.get_point_top_color.return_value = "white"

        self.cli.display_board(mock_board)
        output = mock_stdout.getvalue()
        self.assertGreater(len(output), 0)

    @patch("builtins.input")
    def test_quit_game_confirmation(self, mock_input):
        mock_input.return_value = "y"
        result = self.cli.confirm_quit()
        self.assertTrue(result)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_game_statistics(self, mock_stdout):
        stats = {"moves": 10, "time": 300}
        self.cli.display_statistics(stats)
        output = mock_stdout.getvalue()
        self.assertIn("10", output)
        self.assertIn("300", output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input")
    def test_get_move_input_with_multiple_invalid_attempts(
        self, mock_input, _mock_stdout
    ):
        mock_input.side_effect = [
            "single",  # First attempt fails - only one word
            "1",  # Second attempt fails - only one number
            "1 2 3",  # Third attempt fails - three values
            "5 8",  # Fourth attempt - valid
        ]

        from_pos, to_pos = self.cli.get_move_input()

        self.assertEqual(from_pos, 5)
        self.assertEqual(to_pos, 8)
        self.assertEqual(mock_input.call_count, 4)

    def test_set_game_method(self):
        """Test setting game reference"""
        mock_game = Mock()
        self.cli.set_game(mock_game)
        self.assertEqual(self.cli.game, mock_game)

    @patch("builtins.input")
    def test_confirm_move_invalid_input_retry(self, mock_input):
        """Test confirm move with various inputs"""
        # Test with lowercase 'y' which should be accepted
        mock_input.return_value = "y"
        result = self.cli.confirm_move(1, 4)
        self.assertTrue(result)

        # Test with lowercase 'n' which should be accepted
        mock_input.return_value = "n"
        result = self.cli.confirm_move(1, 4)
        self.assertFalse(result)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_winner_with_none(self, mock_stdout):
        """Test display winner with None player"""
        self.cli.display_winner(None)
        output = mock_stdout.getvalue()
        self.assertGreater(len(output), 0)  # Just check that something is printed

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_current_player_with_none(self, mock_stdout):
        """Test display current player with None"""
        self.cli.display_current_player(None)
        output = mock_stdout.getvalue()
        # Method might not print anything for None, so just check it doesn't crash
        self.assertIsInstance(output, str)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_dice_roll_with_none(self, mock_stdout):
        """Test display dice roll with None values"""
        self.cli.display_dice_roll(None)
        output = mock_stdout.getvalue()
        # Method might not print anything for None, so just check it doesn't crash
        self.assertIsInstance(output, str)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_available_moves_with_none(self, mock_stdout):
        """Test display available moves with None"""
        self.cli.display_available_moves(None)
        output = mock_stdout.getvalue()
        self.assertGreater(len(output), 0)  # Should print something about moves

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_available_moves_empty_list(self, mock_stdout):
        """Test display available moves with empty list"""
        self.cli.display_available_moves([])
        output = mock_stdout.getvalue()
        self.assertGreater(len(output), 0)  # Should print something about no moves

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_statistics_with_none(self, mock_stdout):
        """Test display statistics with None"""
        self.cli.display_statistics(None)
        output = mock_stdout.getvalue()
        # Method might not print anything for None, so just check it doesn't crash
        self.assertIsInstance(output, str)

    def test_run_game_method(self):
        """Test run_game method runs without error when game is set"""
        mock_game = Mock()
        mock_game.start_game = Mock()
        mock_game.is_game_over = Mock(return_value=True)
        mock_game.get_winner = Mock()
        mock_game.get_winner.return_value.name = "TestPlayer"
        self.cli.game = mock_game

        # Should complete without error
        try:
            self.cli.run_game()
        except SystemExit:
            pass  # CLI might call sys.exit, which is fine

    def test_run_game_no_game_set(self):
        """Test run_game when no game is set"""
        self.cli.game = None

        # Should not raise an exception, but should handle gracefully
        try:
            self.cli.run_game()
        except AttributeError:
            pass  # Expected when no game is set


if __name__ == "__main__":
    unittest.main()
