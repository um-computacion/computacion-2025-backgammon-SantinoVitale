"""
Unit tests for UserInterface class.
Tests user I/O functionality following SOLID principles.
"""

import unittest
from unittest.mock import Mock, patch
from backgammon.cli.user_interface import UserInterface


class TestUserInterface(unittest.TestCase):
    """Test cases for UserInterface class."""

    def setUp(self):
        """Set up test fixtures."""
        self.ui = UserInterface()

    def test_init(self):
        """Test UserInterface initialization."""
        ui = UserInterface()
        self.assertIsInstance(ui, UserInterface)

    def test_format_position_bar(self):
        """Test formatting 'bar' position."""
        result = self.ui.format_position("bar")
        self.assertEqual(result, "BARRA")

    def test_format_position_barra(self):
        """Test formatting 'barra' position."""
        result = self.ui.format_position("barra")
        self.assertEqual(result, "BARRA")

    def test_format_position_off(self):
        """Test formatting 'off' position."""
        result = self.ui.format_position("off")
        self.assertEqual(result, "FUERA")

    def test_format_position_fuera(self):
        """Test formatting 'fuera' position."""
        result = self.ui.format_position("fuera")
        self.assertEqual(result, "FUERA")

    def test_format_position_numeric(self):
        """Test formatting numeric position."""
        result = self.ui.format_position(12)
        self.assertEqual(result, "12")

    def test_format_position_numeric_string(self):
        """Test formatting numeric string position."""
        result = self.ui.format_position("24")
        self.assertEqual(result, "24")

    @patch("builtins.print")
    def test_display(self, mock_print):
        """Test display method."""
        self.ui.display("Test message")
        mock_print.assert_called_once_with("Test message")

    @patch("builtins.print")
    def test_display_message(self, mock_print):
        """Test display_message method."""
        self.ui.display_message("Test message")
        mock_print.assert_called_once_with("\n Test message")

    @patch("builtins.print")
    def test_display_error(self, mock_print):
        """Test display_error method."""
        self.ui.display_error("Test error")
        mock_print.assert_called_once_with("\nError: Test error")

    @patch("builtins.input", return_value="test input")
    def test_get_input(self, mock_input):
        """Test get_input method."""
        result = self.ui.get_input("Enter something: ")
        self.assertEqual(result, "test input")
        mock_input.assert_called_once_with("Enter something: ")

    @patch("builtins.input", return_value="  test input  ")
    def test_get_input_strips_whitespace(self, mock_input):
        """Test get_input strips whitespace."""
        result = self.ui.get_input("Prompt: ")
        self.assertEqual(result, "test input")

    @patch("builtins.input", return_value="12 8")
    @patch("builtins.print")
    def test_get_move_input(self, mock_print, mock_input):
        """Test get_move_input method."""
        result = self.ui.get_move_input("'12 8'")
        self.assertEqual(result, "12 8")

    @patch("builtins.input", return_value="TestPlayer")
    @patch("builtins.print")
    def test_get_player_name_white(self, mock_print, mock_input):
        """Test getting white player name."""
        result = self.ui.get_player_name("white")
        self.assertEqual(result, "TestPlayer")

    @patch("builtins.input", return_value="TestPlayer")
    @patch("builtins.print")
    def test_get_player_name_black(self, mock_print, mock_input):
        """Test getting black player name."""
        result = self.ui.get_player_name("black")
        self.assertEqual(result, "TestPlayer")

    @patch("builtins.input", return_value="")
    @patch("builtins.print")
    def test_get_player_name_default_white(self, mock_print, mock_input):
        """Test getting default white player name."""
        result = self.ui.get_player_name("white")
        self.assertEqual(result, "Jugador Blanco")

    @patch("builtins.input", return_value="")
    @patch("builtins.print")
    def test_get_player_name_default_black(self, mock_print, mock_input):
        """Test getting default black player name."""
        result = self.ui.get_player_name("black")
        self.assertEqual(result, "Jugador Negro")

    @patch("builtins.input", return_value="s")
    def test_confirm_action_affirmative(self, mock_input):
        """Test confirm_action with affirmative response."""
        result = self.ui.confirm_action("Confirm? ")
        self.assertTrue(result)

    @patch("builtins.input", return_value="n")
    def test_confirm_action_negative(self, mock_input):
        """Test confirm_action with negative response."""
        result = self.ui.confirm_action("Confirm? ")
        self.assertFalse(result)

    @patch("builtins.print")
    def test_display_welcome(self, mock_print):
        """Test display_welcome method."""
        self.ui.display_welcome()
        self.assertGreater(mock_print.call_count, 0)

    @patch("builtins.print")
    def test_display_winner_with_player(self, mock_print):
        """Test display_winner with player."""
        mock_player = Mock()
        mock_player.name = "TestPlayer"
        mock_player.color = "white"

        self.ui.display_winner(mock_player)
        self.assertGreater(mock_print.call_count, 0)

    @patch("builtins.print")
    def test_display_winner_without_player(self, mock_print):
        """Test display_winner without player."""
        self.ui.display_winner(None)
        mock_print.assert_called_once_with("\n¡Juego terminado!")

    @patch("builtins.print")
    def test_display_current_player(self, mock_print):
        """Test display_current_player method."""
        mock_player = Mock()
        mock_player.name = "TestPlayer"
        mock_player.color = "white"

        self.ui.display_current_player(mock_player)
        self.assertGreater(mock_print.call_count, 0)

    @patch("builtins.print")
    def test_display_dice_roll(self, mock_print):
        """Test display_dice_roll method."""
        self.ui.display_dice_roll([3, 5])
        self.assertGreater(mock_print.call_count, 0)

    @patch("builtins.print")
    def test_display_dice_roll_doubles(self, mock_print):
        """Test display_dice_roll with doubles."""
        self.ui.display_dice_roll([4, 4])
        self.assertGreater(mock_print.call_count, 0)

    @patch("builtins.print")
    def test_display_available_moves(self, mock_print):
        """Test display_available_moves method."""
        self.ui.display_available_moves([3, 5])
        mock_print.assert_called_once_with("\nMovimientos disponibles: [ 3, 5 ]")

    @patch("builtins.print")
    def test_display_available_moves_empty(self, mock_print):
        """Test display_available_moves with empty list."""
        self.ui.display_available_moves([])
        mock_print.assert_called_once_with("\nNo hay movimientos disponibles")

    @patch("builtins.print")
    def test_display_help(self, mock_print):
        """Test display_help method."""
        self.ui.display_help()
        self.assertGreater(mock_print.call_count, 0)

    @patch("builtins.print")
    def test_display_game_rules(self, mock_print):
        """Test display_game_rules method."""
        self.ui.display_game_rules()
        self.assertGreater(mock_print.call_count, 0)

    @patch("builtins.print")
    def test_display_statistics(self, mock_print):
        """Test display_statistics method."""
        stats = {"moves": 10, "captures": 2}
        self.ui.display_statistics(stats)
        self.assertGreater(mock_print.call_count, 0)

    @patch("builtins.input", return_value="")
    def test_pause(self, mock_input):
        """Test pause method."""
        self.ui.pause()
        mock_input.assert_called_once_with("\nPresione Enter para continuar...")

    @patch("os.system")
    def test_clear_screen_windows(self, mock_system):
        """Test clear_screen on Windows."""
        with patch("os.name", "nt"):
            self.ui.clear_screen()
            mock_system.assert_called_once_with("cls")

    @patch("os.system")
    def test_clear_screen_unix(self, mock_system):
        """Test clear_screen on Unix."""
        with patch("os.name", "posix"):
            self.ui.clear_screen()
            mock_system.assert_called_once_with("clear")


if __name__ == "__main__":
    unittest.main()
