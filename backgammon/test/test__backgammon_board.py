"""
Unit tests for BackgammonBoard class.
Tests the main board coordinator including rendering and interaction.
"""

import unittest
from unittest.mock import Mock, patch
from backgammon.pygame_ui.backgammon_board import BackgammonBoard


class TestBackgammonBoardInitialization(unittest.TestCase):
    """Test BackgammonBoard initialization."""

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    def test_init_creates_components(self, mock_rect):
        """Test initialization creates all necessary components."""
        board = BackgammonBoard(1600, 900)

        self.assertIsNotNone(board.dimensions)
        self.assertIsNotNone(board.colors)
        self.assertIsNotNone(board.board_renderer)
        self.assertIsNotNone(board.click_detector)
        self.assertIsNotNone(board.interaction)
        self.assertIsNotNone(board.dice_button)
        self.assertIsNone(board.game)
        self.assertEqual(board.last_player_index, -1)

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    def test_init_custom_dimensions(self, mock_rect):
        """Test initialization with custom dimensions."""
        board = BackgammonBoard(1920, 1080)

        self.assertEqual(board.dimensions.screen_width, 1920)
        self.assertEqual(board.dimensions.screen_height, 1080)


class TestBackgammonBoardGameSetup(unittest.TestCase):
    """Test BackgammonBoard game setup."""

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    def test_set_game(self, mock_rect):
        """Test set_game method."""
        board = BackgammonBoard(1600, 900)

        mock_game = Mock()
        mock_game.current_player_index = 0

        board.set_game(mock_game)

        self.assertEqual(board.game, mock_game)
        self.assertEqual(board.last_player_index, 0)

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    def test_set_game_sets_interaction_game(self, mock_rect):
        """Test set_game also sets game for interaction."""
        board = BackgammonBoard(1600, 900)
        mock_interaction = Mock()
        board.interaction = mock_interaction

        mock_game = Mock()
        mock_game.current_player_index = 0

        board.set_game(mock_game)

        mock_interaction.set_game.assert_called_once_with(mock_game)


class TestBackgammonBoardMouseHandling(unittest.TestCase):
    """Test BackgammonBoard mouse event handling."""

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    def test_update_hover_state(self, mock_rect):
        """Test update_hover_state method."""
        board = BackgammonBoard(1600, 900)
        mock_button = Mock()
        board.dice_button = mock_button

        mouse_pos = (100, 200)
        board.update_hover_state(mouse_pos)

        mock_button.update_hover_state.assert_called_once_with(mouse_pos)

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    @patch("builtins.print")
    def test_handle_mouse_click_dice_button(self, mock_print, mock_rect):
        """Test handle_mouse_click on dice button."""
        board = BackgammonBoard(1600, 900)
        mock_button = Mock()
        mock_button.is_clicked.return_value = True
        board.dice_button = mock_button

        mock_game = Mock()
        mock_game.dice = Mock()
        mock_game.dice.last_roll = [3, 5]
        board.game = mock_game
        board.interaction = Mock()
        board.interaction.dice_rolled = False

        board.handle_mouse_click((100, 200))

        mock_game.roll_dice.assert_called_once()
        self.assertTrue(board.interaction.dice_rolled)

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    def test_handle_mouse_click_point(self, mock_rect):
        """Test handle_mouse_click on a point."""
        board = BackgammonBoard(1600, 900)
        mock_button = Mock()
        mock_button.is_clicked.return_value = False
        board.dice_button = mock_button

        mock_click_detector = Mock()
        mock_click_detector.get_clicked_position.return_value = ("point", 5)
        board.click_detector = mock_click_detector

        mock_interaction = Mock()
        board.interaction = mock_interaction

        board.handle_mouse_click((100, 200))

        mock_interaction.handle_point_click.assert_called_once_with(5)

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    def test_handle_mouse_click_bar(self, mock_rect):
        """Test handle_mouse_click on bar."""
        board = BackgammonBoard(1600, 900)
        mock_button = Mock()
        mock_button.is_clicked.return_value = False
        board.dice_button = mock_button

        mock_click_detector = Mock()
        mock_click_detector.get_clicked_position.return_value = ("bar", 0)
        board.click_detector = mock_click_detector

        mock_interaction = Mock()
        board.interaction = mock_interaction

        board.handle_mouse_click((100, 200))

        mock_interaction.handle_bar_click.assert_called_once()

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    def test_handle_mouse_click_off_area(self, mock_rect):
        """Test handle_mouse_click on off area."""
        board = BackgammonBoard(1600, 900)
        mock_button = Mock()
        mock_button.is_clicked.return_value = False
        board.dice_button = mock_button

        mock_click_detector = Mock()
        mock_click_detector.get_clicked_position.return_value = ("off", 0)
        board.click_detector = mock_click_detector

        mock_interaction = Mock()
        board.interaction = mock_interaction

        board.handle_mouse_click((100, 200))

        mock_interaction.handle_off_area_click.assert_called_once()

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    def test_handle_mouse_click_no_position(self, mock_rect):
        """Test handle_mouse_click with no valid position."""
        board = BackgammonBoard(1600, 900)
        mock_button = Mock()
        mock_button.is_clicked.return_value = False
        board.dice_button = mock_button

        mock_click_detector = Mock()
        mock_click_detector.get_clicked_position.return_value = None
        board.click_detector = mock_click_detector

        mock_interaction = Mock()
        board.interaction = mock_interaction

        board.handle_mouse_click((100, 200))

        mock_interaction.clear_selection.assert_called_once()


class TestBackgammonBoardRendering(unittest.TestCase):
    """Test BackgammonBoard rendering."""

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    def test_render_without_game(self, mock_rect):
        """Test render method without game set."""
        board = BackgammonBoard(1600, 900)
        mock_surface = Mock()
        mock_renderer = Mock()
        mock_button = Mock()
        board.board_renderer = mock_renderer
        board.dice_button = mock_button

        board.render(mock_surface)

        mock_renderer.render.assert_called_once()
        mock_button.render.assert_called_once_with(mock_surface)

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    def test_render_with_game(self, mock_rect):
        """Test render method with game set."""
        board = BackgammonBoard(1600, 900)
        mock_surface = Mock()

        mock_game = Mock()
        mock_board_obj = Mock()
        mock_dice = Mock()
        mock_dice.last_roll = [3, 5]
        mock_dice.get_available_moves.return_value = [3, 5]

        mock_player1 = Mock()
        mock_player1.name = "Player 1"
        mock_player1.color = "white"
        mock_player1.checkers_off_board = 5

        mock_player2 = Mock()
        mock_player2.name = "Player 2"
        mock_player2.color = "black"
        mock_player2.checkers_off_board = 3

        mock_game.board = mock_board_obj
        mock_game.dice = mock_dice
        mock_game.players = [mock_player1, mock_player2]
        mock_game.get_current_player.return_value = mock_player1

        board.game = mock_game
        mock_renderer = Mock()
        mock_button = Mock()
        board.board_renderer = mock_renderer
        board.dice_button = mock_button

        board.render(mock_surface)

        mock_renderer.render.assert_called_once()
        call_args = mock_renderer.render.call_args
        self.assertEqual(call_args[0][0], mock_surface)
        self.assertEqual(call_args[1]["board"], mock_board_obj)
        self.assertEqual(call_args[1]["dice_values"], [3, 5])


class TestBackgammonBoardButtonState(unittest.TestCase):
    """Test BackgammonBoard button state management."""

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    @patch("builtins.print")
    def test_update_button_state_turn_change(self, mock_print, mock_rect):
        """Test button state updates on turn change."""
        board = BackgammonBoard(1600, 900)

        mock_game = Mock()
        mock_game.current_player_index = 1
        board.game = mock_game
        board.last_player_index = 0

        mock_button = Mock()
        board.dice_button = mock_button

        mock_interaction = Mock()
        board.interaction = mock_interaction

        board._update_button_state(None)

        self.assertEqual(board.last_player_index, 1)
        mock_button.set_enabled.assert_called_once_with(True)
        mock_interaction.reset_turn_state.assert_called_once()

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    def test_update_button_state_no_moves(self, mock_rect):
        """Test button state with no available moves."""
        board = BackgammonBoard(1600, 900)

        mock_game = Mock()
        mock_game.current_player_index = 0
        board.game = mock_game
        board.last_player_index = 0

        mock_button = Mock()
        board.dice_button = mock_button

        mock_interaction = Mock()
        mock_interaction.dice_rolled = True
        board.interaction = mock_interaction

        board._update_button_state([])

        mock_button.set_enabled.assert_called_once_with(False)

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    def test_update_button_state_no_game(self, mock_rect):
        """Test button state update with no game set."""
        board = BackgammonBoard(1600, 900)
        board.game = None

        # Should not raise exception
        board._update_button_state(None)


class TestBackgammonBoardDiceButton(unittest.TestCase):
    """Test BackgammonBoard dice button handling."""

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    @patch("builtins.print")
    def test_handle_dice_button_click_success(self, mock_print, mock_rect):
        """Test handling dice button click successfully."""
        board = BackgammonBoard(1600, 900)

        mock_game = Mock()
        mock_game.dice = Mock()
        mock_game.dice.last_roll = [4, 2]
        board.game = mock_game

        mock_interaction = Mock()
        mock_interaction.dice_rolled = False
        board.interaction = mock_interaction

        mock_button = Mock()
        board.dice_button = mock_button

        board._handle_dice_button_click()

        mock_game.roll_dice.assert_called_once()
        self.assertTrue(board.interaction.dice_rolled)
        mock_button.set_enabled.assert_called_once_with(False)

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    @patch("builtins.print")
    def test_handle_dice_button_click_already_rolled(self, mock_print, mock_rect):
        """Test handling dice button click when already rolled."""
        board = BackgammonBoard(1600, 900)

        mock_interaction = Mock()
        mock_interaction.dice_rolled = True
        board.interaction = mock_interaction

        board._handle_dice_button_click()

        # Should print message but not roll
        mock_print.assert_called()

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    @patch("builtins.print")
    def test_handle_dice_button_click_no_game(self, mock_print, mock_rect):
        """Test handling dice button click with no game."""
        board = BackgammonBoard(1600, 900)
        board.game = None

        mock_interaction = Mock()
        mock_interaction.dice_rolled = False
        board.interaction = mock_interaction

        board._handle_dice_button_click()

        # Should print error message
        mock_print.assert_called()


class TestBackgammonBoardCreateDiceButton(unittest.TestCase):
    """Test BackgammonBoard dice button creation."""

    @patch("backgammon.pygame_ui.backgammon_board.pygame.Rect")
    @patch("backgammon.pygame_ui.backgammon_board.Button")
    def test_create_dice_button(self, mock_button_class, mock_rect):
        """Test _create_dice_button method."""
        mock_rect_instance = Mock()
        mock_rect.return_value = mock_rect_instance

        board = BackgammonBoard(1600, 900)

        # Button should have been created
        mock_button_class.assert_called_once()
        call_args = mock_button_class.call_args

        # Check button text
        self.assertEqual(call_args[0][2], "ROLL DICE")


if __name__ == "__main__":
    unittest.main()
