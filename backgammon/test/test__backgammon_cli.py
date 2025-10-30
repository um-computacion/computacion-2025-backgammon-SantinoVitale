"""
Unit tests for BackgammonCLI class.
Tests CLI coordinator functionality following SOLID principles.
"""

import unittest
from unittest.mock import Mock, patch
from backgammon.cli.BackgammonCLI import BackgammonCLI


class TestBackgammonCLIInitialization(unittest.TestCase):
    """Test BackgammonCLI initialization."""

    def test_init_without_game(self):
        """Test initialization without game."""
        cli = BackgammonCLI()
        self.assertIsNotNone(cli.board_renderer)
        self.assertIsNotNone(cli.command_parser)
        self.assertIsNotNone(cli.input_validator)
        self.assertIsNotNone(cli.game_controller)
        self.assertIsNotNone(cli.ui)

    def test_init_with_game(self):
        """Test initialization with game."""
        mock_game = Mock()
        cli = BackgammonCLI(mock_game)
        self.assertIsNotNone(cli.game_controller)

    def test_set_game(self):
        """Test setting game instance."""
        cli = BackgammonCLI()
        mock_game = Mock()
        cli.set_game(mock_game)
        self.assertIsNotNone(cli.game_controller)


class TestBackgammonCLIDisplayBoard(unittest.TestCase):
    """Test BackgammonCLI display board functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.cli = BackgammonCLI()
        self.mock_board = Mock()
        self.mock_player = Mock()

    @patch("backgammon.cli.BackgammonCLI.UserInterface.display")
    def test_display_board_with_board_parameter(self, mock_display):
        """Test displaying board with board parameter."""
        self.cli.board_renderer.render_board = Mock(return_value="Board Display")
        self.cli.board_renderer.render_legend = Mock(return_value="Legend")
        self.cli.game_controller.get_current_player = Mock(
            return_value=self.mock_player
        )

        self.cli.display_board(self.mock_board)

        self.cli.board_renderer.render_board.assert_called_once_with(self.mock_board)
        mock_display.assert_called()

    @patch("backgammon.cli.BackgammonCLI.UserInterface.display")
    def test_display_board_without_board_parameter(self, mock_display):
        """Test displaying board without board parameter."""
        self.cli.game_controller.get_board = Mock(return_value=self.mock_board)
        self.cli.board_renderer.render_board = Mock(return_value="Board Display")
        self.cli.board_renderer.render_legend = Mock(return_value="Legend")
        self.cli.game_controller.get_current_player = Mock(
            return_value=self.mock_player
        )

        self.cli.display_board()

        self.cli.game_controller.get_board.assert_called_once()
        mock_display.assert_called()

    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_message")
    def test_display_board_no_board_available(self, mock_display_message):
        """Test displaying board when no board is available."""
        self.cli.game_controller.get_board = Mock(return_value=None)

        self.cli.display_board()

        mock_display_message.assert_called_once_with(
            "No hay tablero disponible para mostrar"
        )


class TestBackgammonCLIDisplayPossibleMoves(unittest.TestCase):
    """Test BackgammonCLI display possible moves functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.cli = BackgammonCLI()

    @patch("backgammon.cli.BackgammonCLI.UserInterface.display")
    def test_display_possible_moves_with_moves(self, mock_display):
        """Test displaying possible moves when moves are available."""
        moves = [(1, 4), (6, 9)]
        self.cli.game_controller.get_possible_moves = Mock(return_value=moves)
        self.cli.board_renderer.render_possible_moves = Mock(
            return_value="Moves Display"
        )

        self.cli.display_possible_moves()

        self.cli.game_controller.get_possible_moves.assert_called_once()
        mock_display.assert_called_once_with("Moves Display")

    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_message")
    def test_display_possible_moves_no_moves(self, mock_display_message):
        """Test displaying possible moves when no moves are available."""
        self.cli.game_controller.get_possible_moves = Mock(return_value=[])

        self.cli.display_possible_moves()

        mock_display_message.assert_called_once_with(
            "No hay movimientos válidos disponibles"
        )


class TestBackgammonCLIGetMoveInput(unittest.TestCase):
    """Test BackgammonCLI get move input functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.cli = BackgammonCLI()
        self.mock_player = Mock()

    @patch(
        "backgammon.cli.BackgammonCLI.UserInterface.get_move_input", return_value="12 8"
    )
    def test_get_move_input_valid(self, _mock_get_input):
        """Test getting valid move input."""
        self.cli.game_controller.get_current_player = Mock(
            return_value=self.mock_player
        )
        self.mock_player.color = "white"
        self.cli.command_parser.parse_move_input = Mock(return_value=(12, 8))

        from_pos, to_pos = self.cli.get_move_input()

        self.assertEqual(from_pos, 12)
        self.assertEqual(to_pos, 8)

    @patch(
        "backgammon.cli.BackgammonCLI.UserInterface.get_move_input", return_value="8 12"
    )
    def test_get_move_input_black_player(self, _mock_get_input):
        """Test getting move input for black player."""
        self.cli.game_controller.get_current_player = Mock(
            return_value=self.mock_player
        )
        self.mock_player.color = "black"
        self.cli.command_parser.parse_move_input = Mock(return_value=(8, 12))

        from_pos, to_pos = self.cli.get_move_input()

        self.assertEqual(from_pos, 8)
        self.assertEqual(to_pos, 12)

    @patch(
        "backgammon.cli.BackgammonCLI.UserInterface.get_move_input", return_value="12 8"
    )
    def test_get_move_input_no_color_attribute(self, _mock_get_input):
        """Test getting move input when player has no color attribute."""
        mock_player_no_color = Mock(spec=[])
        self.cli.game_controller.get_current_player = Mock(
            return_value=mock_player_no_color
        )
        self.cli.command_parser.parse_move_input = Mock(return_value=(12, 8))

        from_pos, to_pos = self.cli.get_move_input()

        self.assertEqual(from_pos, 12)
        self.assertEqual(to_pos, 8)

    @patch(
        "backgammon.cli.BackgammonCLI.UserInterface.get_move_input", return_value="12 8"
    )
    def test_get_move_input_no_player(self, _mock_get_input):
        """Test getting move input when no current player."""
        self.cli.game_controller.get_current_player = Mock(return_value=None)
        self.cli.command_parser.parse_move_input = Mock(return_value=(12, 8))

        from_pos, to_pos = self.cli.get_move_input()

        self.assertEqual(from_pos, 12)
        self.assertEqual(to_pos, 8)

    @patch(
        "backgammon.cli.BackgammonCLI.UserInterface.get_move_input",
        side_effect=["invalid", "12 8"],
    )
    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_error")
    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_message")
    def test_get_move_input_invalid_then_valid(
        self, _mock_display_msg, mock_display_error, _mock_get_input
    ):
        """Test getting move input with invalid then valid input."""
        self.cli.game_controller.get_current_player = Mock(
            return_value=self.mock_player
        )
        self.mock_player.color = "white"
        self.cli.command_parser.parse_move_input = Mock(
            side_effect=[ValueError("Invalid"), (12, 8)]
        )

        from_pos, to_pos = self.cli.get_move_input()

        self.assertEqual(from_pos, 12)
        self.assertEqual(to_pos, 8)
        mock_display_error.assert_called_once()

    @patch(
        "backgammon.cli.BackgammonCLI.UserInterface.get_move_input",
        side_effect=[KeyboardInterrupt(), "12 8"],
    )
    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_message")
    def test_get_move_input_keyboard_interrupt(
        self, _mock_display_msg, _mock_get_input
    ):
        """Test getting move input with keyboard interrupt."""
        self.cli.game_controller.get_current_player = Mock(
            return_value=self.mock_player
        )
        self.mock_player.color = "white"
        self.cli.command_parser.parse_move_input = Mock(return_value=(12, 8))

        from_pos, to_pos = self.cli.get_move_input()

        self.assertEqual(from_pos, 12)
        self.assertEqual(to_pos, 8)

    @patch(
        "backgammon.cli.BackgammonCLI.UserInterface.get_move_input",
        side_effect=[ValueError("Bad input"), "12 8"],
    )
    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_message")
    def test_get_move_input_value_error_exception(
        self, _mock_display_msg, _mock_get_input
    ):
        """Test getting move input with ValueError exception."""
        self.cli.game_controller.get_current_player = Mock(
            return_value=self.mock_player
        )
        self.mock_player.color = "white"
        self.cli.command_parser.parse_move_input = Mock(return_value=(12, 8))

        from_pos, to_pos = self.cli.get_move_input()

        self.assertEqual(from_pos, 12)
        self.assertEqual(to_pos, 8)


class TestBackgammonCLIDisplayMoveError(unittest.TestCase):
    """Test BackgammonCLI display move error functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.cli = BackgammonCLI()

    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_error")
    @patch("backgammon.cli.BackgammonCLI.UserInterface.display")
    def test_display_move_error_with_possible_moves(
        self, mock_display, mock_display_error
    ):
        """Test displaying move error with possible moves."""
        moves = [(1, 4), (6, 9), (8, 12)]
        self.cli.game_controller.get_possible_moves = Mock(return_value=moves)

        # pylint: disable=W0212
        self.cli._display_move_error(1, 10)

        mock_display_error.assert_called_once()
        self.assertGreater(mock_display.call_count, 0)

    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_error")
    @patch("backgammon.cli.BackgammonCLI.UserInterface.display")
    def test_display_move_error_with_many_moves(self, mock_display, mock_display_error):
        """Test displaying move error with many possible moves."""
        moves = [(i, i + 1) for i in range(10)]
        self.cli.game_controller.get_possible_moves = Mock(return_value=moves)

        # pylint: disable=W0212
        self.cli._display_move_error(1, 10)

        mock_display_error.assert_called_once()
        self.assertGreater(mock_display.call_count, 5)

    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_error")
    def test_display_move_error_no_possible_moves(self, mock_display_error):
        """Test displaying move error with no possible moves."""
        self.cli.game_controller.get_possible_moves = Mock(return_value=[])

        # pylint: disable=W0212
        self.cli._display_move_error(1, 10)

        self.assertEqual(mock_display_error.call_count, 1)


class TestBackgammonCLIRunGame(unittest.TestCase):
    """Test BackgammonCLI run game functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.cli = BackgammonCLI()

    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_welcome")
    @patch(
        "backgammon.cli.BackgammonCLI.UserInterface.get_player_name",
        side_effect=["Player1", "Player2"],
    )
    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_message")
    def test_run_game_game_over_immediately(
        self, _mock_display_msg, _mock_get_name, mock_display_welcome
    ):
        """Test running game that ends immediately."""
        self.cli.game_controller.setup_game = Mock()
        self.cli.game_controller.is_game_over = Mock(return_value=True)
        self.cli.game_controller.get_winner = Mock(return_value=Mock(name="Player1"))
        self.cli.ui.display_winner = Mock()

        self.cli.run_game()

        mock_display_welcome.assert_called_once()
        self.cli.game_controller.setup_game.assert_called_once_with(
            "Player1", "Player2"
        )
        self.cli.ui.display_winner.assert_called_once()

    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_welcome")
    @patch(
        "backgammon.cli.BackgammonCLI.UserInterface.get_player_name",
        side_effect=["Player1", "Player2"],
    )
    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_message")
    @patch("backgammon.cli.BackgammonCLI.UserInterface.clear_screen")
    @patch("backgammon.cli.BackgammonCLI.UserInterface.display_current_player")
    def test_run_game_keyboard_interrupt(
        self,
        _mock_display_player,
        _mock_clear,
        _mock_display_msg,
        _mock_get_name,
        mock_display_welcome,
    ):
        """Test running game with keyboard interrupt."""
        self.cli.game_controller.setup_game = Mock()
        self.cli.game_controller.is_game_over = Mock(return_value=False)
        self.cli.display_board = Mock(side_effect=KeyboardInterrupt())
        self.cli.ui.confirm_action = Mock(return_value=True)

        self.cli.run_game()

        mock_display_welcome.assert_called_once()
        self.cli.ui.confirm_action.assert_called_once()


if __name__ == "__main__":
    unittest.main()
