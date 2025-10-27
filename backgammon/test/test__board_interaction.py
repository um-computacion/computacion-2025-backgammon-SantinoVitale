"""
Unit tests for BoardInteraction class.
Tests board interaction handling including clicks, moves, and validation.
"""

import unittest
from unittest.mock import Mock, patch
from backgammon.pygame_ui.board_interaction import BoardInteraction
from backgammon.pygame_ui.click_detector import ClickDetector
from backgammon.pygame_ui.board_dimensions import BoardDimensions


class TestBoardInteractionInitialization(unittest.TestCase):
    """Test BoardInteraction initialization."""

    def test_init_with_click_detector(self):
        """Test initialization with ClickDetector instance."""
        dimensions = BoardDimensions(1600, 900)
        detector = ClickDetector(dimensions)
        interaction = BoardInteraction(detector)

        self.assertEqual(interaction.click_detector, detector)
        self.assertIsNone(interaction.game)
        self.assertIsNone(interaction.selected_point)
        self.assertFalse(interaction.selected_bar)
        self.assertEqual(interaction.valid_move_destinations, [])
        self.assertFalse(interaction.dice_rolled)

    def test_set_game(self):
        """Test set_game method."""
        dimensions = BoardDimensions(1600, 900)
        detector = ClickDetector(dimensions)
        interaction = BoardInteraction(detector)

        mock_game = Mock()
        interaction.set_game(mock_game)

        self.assertEqual(interaction.game, mock_game)


class TestBoardInteractionStateManagement(unittest.TestCase):
    """Test BoardInteraction state management."""

    def setUp(self):
        """Set up test fixtures."""
        dimensions = BoardDimensions(1600, 900)
        detector = ClickDetector(dimensions)
        self.interaction = BoardInteraction(detector)

    def test_clear_selection(self):
        """Test clear_selection method."""
        self.interaction.selected_point = 5
        self.interaction.selected_bar = True
        self.interaction.valid_move_destinations = [3, 4, 5]

        self.interaction.clear_selection()

        self.assertIsNone(self.interaction.selected_point)
        self.assertFalse(self.interaction.selected_bar)
        self.assertEqual(self.interaction.valid_move_destinations, [])

    def test_reset_turn_state(self):
        """Test reset_turn_state method."""
        self.interaction.dice_rolled = True
        self.interaction.selected_point = 10
        self.interaction.valid_move_destinations = [7, 8]

        self.interaction.reset_turn_state()

        self.assertFalse(self.interaction.dice_rolled)
        self.assertIsNone(self.interaction.selected_point)
        self.assertEqual(self.interaction.valid_move_destinations, [])


class TestBoardInteractionPointClicks(unittest.TestCase):
    """Test BoardInteraction point click handling."""

    def setUp(self):
        """Set up test fixtures."""
        dimensions = BoardDimensions(1600, 900)
        detector = ClickDetector(dimensions)
        self.interaction = BoardInteraction(detector)

    @patch("builtins.print")
    def test_handle_point_click_no_game(self, mock_print):
        """Test handle_point_click with no game set."""
        self.interaction.handle_point_click(5)

        # Should not crash, just return
        self.assertIsNone(self.interaction.selected_point)

    @patch("builtins.print")
    def test_handle_point_click_select_point(self, mock_print):
        """Test handle_point_click to select a point."""
        mock_game = Mock()
        mock_board = Mock()
        mock_player = Mock()
        mock_player.color = "white"
        mock_checker = Mock()
        mock_checker.color = "white"

        mock_board.points = {5: [mock_checker]}
        mock_board.bar = {"white": [], "black": []}
        mock_game.board = mock_board
        mock_game.dice = Mock()
        mock_game.dice.last_roll = [3, 4]
        mock_game.dice.get_available_moves.return_value = []
        mock_game.get_current_player.return_value = mock_player

        self.interaction.set_game(mock_game)
        self.interaction.handle_point_click(5)

        self.assertEqual(self.interaction.selected_point, 5)

    @patch("builtins.print")
    def test_handle_point_click_deselect_same_point(self, mock_print):
        """Test handle_point_click to deselect the same point."""
        self.interaction.selected_point = 5
        self.interaction.selected_bar = False

        self.interaction.handle_point_click(5)

        self.assertIsNone(self.interaction.selected_point)

    @patch("builtins.print")
    def test_handle_point_click_execute_move(self, mock_print):
        """Test handle_point_click to execute a move."""
        mock_game = Mock()
        mock_game.make_move.return_value = True
        mock_game.dice = Mock()
        mock_game.dice.get_available_moves.return_value = []

        self.interaction.set_game(mock_game)
        self.interaction.selected_point = 5
        self.interaction.valid_move_destinations = [8]

        self.interaction.handle_point_click(8)

        mock_game.make_move.assert_called_once_with(6, 9)
        self.assertIsNone(self.interaction.selected_point)


class TestBoardInteractionBarClicks(unittest.TestCase):
    """Test BoardInteraction bar click handling."""

    def setUp(self):
        """Set up test fixtures."""
        dimensions = BoardDimensions(1600, 900)
        detector = ClickDetector(dimensions)
        self.interaction = BoardInteraction(detector)

    @patch("builtins.print")
    def test_handle_bar_click_no_game(self, mock_print):
        """Test handle_bar_click with no game set."""
        self.interaction.handle_bar_click()

        # Should not crash
        self.assertFalse(self.interaction.selected_bar)

    @patch("builtins.print")
    def test_handle_bar_click_no_checkers_on_bar(self, mock_print):
        """Test handle_bar_click with no checkers on bar."""
        mock_game = Mock()
        mock_board = Mock()
        mock_player = Mock()
        mock_player.color = "white"

        mock_board.bar = {"white": [], "black": []}
        mock_game.board = mock_board
        mock_game.get_current_player.return_value = mock_player

        self.interaction.set_game(mock_game)
        self.interaction.handle_bar_click()

        self.assertFalse(self.interaction.selected_bar)

    @patch("builtins.print")
    def test_handle_bar_click_with_checkers(self, mock_print):
        """Test handle_bar_click with checkers on bar."""
        mock_game = Mock()
        mock_board = Mock()
        mock_player = Mock()
        mock_player.color = "white"
        mock_checker = Mock()

        mock_board.bar = {"white": [mock_checker], "black": []}
        mock_game.board = mock_board
        mock_game.dice = Mock()
        mock_game.dice.last_roll = [3, 4]
        mock_game.dice.get_available_moves.return_value = []
        mock_game.get_current_player.return_value = mock_player

        self.interaction.set_game(mock_game)
        self.interaction.handle_bar_click()

        self.assertTrue(self.interaction.selected_bar)
        self.assertIsNone(self.interaction.selected_point)


class TestBoardInteractionOffAreaClicks(unittest.TestCase):
    """Test BoardInteraction off area click handling."""

    def setUp(self):
        """Set up test fixtures."""
        dimensions = BoardDimensions(1600, 900)
        detector = ClickDetector(dimensions)
        self.interaction = BoardInteraction(detector)

    @patch("builtins.print")
    def test_handle_off_area_click_no_selection(self, mock_print):
        """Test handle_off_area_click with no checker selected."""
        self.interaction.handle_off_area_click()

        mock_print.assert_called()

    @patch("builtins.print")
    def test_handle_off_area_click_from_bar(self, mock_print):
        """Test handle_off_area_click from bar (invalid)."""
        self.interaction.selected_bar = True

        self.interaction.handle_off_area_click()

        # Should deselect and print message
        self.assertFalse(self.interaction.selected_bar)

    @patch("builtins.print")
    def test_handle_off_area_click_valid_bearing_off(self, mock_print):
        """Test handle_off_area_click with valid bearing off."""
        mock_game = Mock()
        mock_game.make_move.return_value = True
        mock_game.dice = Mock()
        mock_game.dice.get_available_moves.return_value = []

        self.interaction.set_game(mock_game)
        self.interaction.selected_point = 23
        self.interaction.valid_move_destinations = ["off"]

        self.interaction.handle_off_area_click()

        mock_game.make_move.assert_called_once_with(24, "off")

    @patch("builtins.print")
    def test_handle_off_area_click_invalid_bearing_off(self, mock_print):
        """Test handle_off_area_click with invalid bearing off."""
        self.interaction.selected_point = 10
        self.interaction.valid_move_destinations = [7, 8]

        self.interaction.handle_off_area_click()

        # Should deselect
        self.assertIsNone(self.interaction.selected_point)


class TestBoardInteractionMoveValidation(unittest.TestCase):
    """Test BoardInteraction move validation."""

    def setUp(self):
        """Set up test fixtures."""
        dimensions = BoardDimensions(1600, 900)
        detector = ClickDetector(dimensions)
        self.interaction = BoardInteraction(detector)

    def test_calculate_valid_destinations_no_game(self):
        """Test _calculate_valid_destinations with no game."""
        result = self.interaction._calculate_valid_destinations(5)

        self.assertEqual(result, [])

    def test_calculate_valid_destinations_no_dice(self):
        """Test _calculate_valid_destinations with no dice rolled."""
        mock_game = Mock()
        mock_game.dice = Mock()
        mock_game.dice.last_roll = None

        self.interaction.set_game(mock_game)
        result = self.interaction._calculate_valid_destinations(5)

        self.assertEqual(result, [])

    def test_calculate_valid_destinations_with_valid_moves(self):
        """Test _calculate_valid_destinations with valid moves."""
        mock_game = Mock()
        mock_board = Mock()
        mock_player = Mock()
        mock_player.color = "white"
        mock_checker = Mock()
        mock_checker.color = "white"

        mock_board.points = {5: [mock_checker]}
        mock_game.board = mock_board
        mock_game.dice = Mock()
        mock_game.dice.last_roll = [3, 4]
        mock_game.dice.get_available_moves.return_value = [3, 4]
        mock_game.get_current_player.return_value = mock_player
        mock_game.is_valid_move.return_value = True

        self.interaction.set_game(mock_game)
        result = self.interaction._calculate_valid_destinations(5)

        # White moves backwards, so 5-3=2 and 5-4=1
        self.assertIsInstance(result, list)

    def test_calculate_valid_destinations_from_bar_no_game(self):
        """Test _calculate_valid_destinations_from_bar with no game."""
        result = self.interaction._calculate_valid_destinations_from_bar()

        self.assertEqual(result, [])


class TestBoardInteractionMoveExecution(unittest.TestCase):
    """Test BoardInteraction move execution."""

    def setUp(self):
        """Set up test fixtures."""
        dimensions = BoardDimensions(1600, 900)
        detector = ClickDetector(dimensions)
        self.interaction = BoardInteraction(detector)

    @patch("builtins.print")
    def test_execute_move_no_selection(self, mock_print):
        """Test _execute_move with no selection."""
        self.interaction.selected_point = None
        self.interaction._execute_move(5)

        # Should just return
        mock_print.assert_not_called()

    @patch("builtins.print")
    def test_execute_move_success(self, mock_print):
        """Test _execute_move with successful move."""
        mock_game = Mock()
        mock_game.make_move.return_value = True
        mock_game.dice = Mock()
        mock_game.dice.get_available_moves.return_value = []

        self.interaction.set_game(mock_game)
        self.interaction.selected_point = 5

        self.interaction._execute_move(8)

        mock_game.make_move.assert_called_once_with(6, 9)
        self.assertIsNone(self.interaction.selected_point)

    @patch("builtins.print")
    def test_execute_move_failure(self, mock_print):
        """Test _execute_move with failed move."""
        mock_game = Mock()
        mock_game.make_move.return_value = False

        self.interaction.set_game(mock_game)
        self.interaction.selected_point = 5

        self.interaction._execute_move(8)

        mock_print.assert_called()

    @patch("builtins.print")
    def test_execute_move_from_bar_success(self, mock_print):
        """Test _execute_move_from_bar with successful move."""
        mock_game = Mock()
        mock_game.make_move.return_value = True
        mock_game.dice = Mock()
        mock_game.dice.get_available_moves.return_value = []

        self.interaction.set_game(mock_game)

        self.interaction._execute_move_from_bar(5)

        mock_game.make_move.assert_called_once_with("bar", 6)

    @patch("builtins.print")
    def test_execute_move_to_off_no_selection(self, mock_print):
        """Test _execute_move_to_off with no selection."""
        self.interaction.selected_point = None
        self.interaction._execute_move_to_off()

        # Should just return
        self.assertIsNone(self.interaction.selected_point)

    @patch("builtins.print")
    def test_execute_move_to_off_success(self, mock_print):
        """Test _execute_move_to_off with successful bearing off."""
        mock_game = Mock()
        mock_game.make_move.return_value = True
        mock_game.dice = Mock()
        mock_game.dice.get_available_moves.return_value = []

        self.interaction.set_game(mock_game)
        self.interaction.selected_point = 23

        self.interaction._execute_move_to_off()

        mock_game.make_move.assert_called_once_with(24, "off")


class TestBoardInteractionTurnCompletion(unittest.TestCase):
    """Test BoardInteraction turn completion logic."""

    def setUp(self):
        """Set up test fixtures."""
        dimensions = BoardDimensions(1600, 900)
        detector = ClickDetector(dimensions)
        self.interaction = BoardInteraction(detector)

    @patch("builtins.print")
    def test_check_turn_completion_no_game(self, mock_print):
        """Test _check_turn_completion with no game."""
        self.interaction._check_turn_completion()

        # Should not crash

    @patch("builtins.print")
    def test_check_turn_completion_all_dice_consumed(self, mock_print):
        """Test _check_turn_completion when all dice consumed."""
        mock_game = Mock()
        mock_game.dice = Mock()
        mock_game.dice.get_available_moves.return_value = []

        self.interaction.set_game(mock_game)
        self.interaction._check_turn_completion()

        mock_game.complete_turn.assert_called_once()

    @patch("builtins.print")
    def test_check_turn_completion_no_valid_moves(self, mock_print):
        """Test _check_turn_completion when no valid moves available."""
        mock_game = Mock()
        mock_game.dice = Mock()
        mock_game.dice.get_available_moves.return_value = [3]
        mock_game.has_valid_moves.return_value = False

        self.interaction.set_game(mock_game)
        self.interaction._check_turn_completion()

        mock_game.complete_turn.assert_called_once()

    @patch("builtins.print")
    def test_check_turn_completion_turn_continues(self, mock_print):
        """Test _check_turn_completion when turn continues."""
        mock_game = Mock()
        mock_game.dice = Mock()
        mock_game.dice.get_available_moves.return_value = [3, 4]
        mock_game.has_valid_moves.return_value = True

        self.interaction.set_game(mock_game)
        self.interaction._check_turn_completion()

        mock_game.complete_turn.assert_not_called()


class TestBoardInteractionTrySelectPoint(unittest.TestCase):
    """Test BoardInteraction point selection logic."""

    def setUp(self):
        """Set up test fixtures."""
        dimensions = BoardDimensions(1600, 900)
        detector = ClickDetector(dimensions)
        self.interaction = BoardInteraction(detector)

    @patch("builtins.print")
    def test_try_select_point_with_bar_checkers(self, mock_print):
        """Test _try_select_point when checkers on bar."""
        mock_game = Mock()
        mock_board = Mock()
        mock_player = Mock()
        mock_player.color = "white"
        mock_checker = Mock()

        mock_board.bar = {"white": [mock_checker], "black": []}
        mock_game.board = mock_board
        mock_game.get_current_player.return_value = mock_player

        self.interaction.set_game(mock_game)
        self.interaction._try_select_point(5)

        # Should not select point
        self.assertIsNone(self.interaction.selected_point)

    @patch("builtins.print")
    def test_try_select_point_no_checkers(self, mock_print):
        """Test _try_select_point on empty point."""
        mock_game = Mock()
        mock_board = Mock()
        mock_player = Mock()
        mock_player.color = "white"

        mock_board.points = {5: []}
        mock_board.bar = {"white": [], "black": []}
        mock_game.board = mock_board
        mock_game.get_current_player.return_value = mock_player

        self.interaction.set_game(mock_game)
        self.interaction._try_select_point(5)

        self.assertIsNone(self.interaction.selected_point)

    @patch("builtins.print")
    def test_try_select_point_wrong_color(self, mock_print):
        """Test _try_select_point on opponent's checker."""
        mock_game = Mock()
        mock_board = Mock()
        mock_player = Mock()
        mock_player.color = "white"
        mock_checker = Mock()
        mock_checker.color = "black"

        mock_board.points = {5: [mock_checker]}
        mock_board.bar = {"white": [], "black": []}
        mock_game.board = mock_board
        mock_game.get_current_player.return_value = mock_player

        self.interaction.set_game(mock_game)
        self.interaction._try_select_point(5)

        self.assertIsNone(self.interaction.selected_point)


if __name__ == "__main__":
    unittest.main()
