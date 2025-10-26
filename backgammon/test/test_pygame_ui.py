"""
Unit tests for PygameUI class.
Tests the main pygame UI coordinator including initialization, event handling, and rendering.
"""

import unittest
from unittest.mock import Mock, patch
import pygame
from backgammon.pygame_ui.pygame_ui import PygameUI


class TestPygameUIInitialization(unittest.TestCase):
    """Test PygameUI initialization."""

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    def test_init_default_dimensions(self, mock_board_class, mock_pygame):
        """Test initialization with default dimensions."""
        mock_display = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = Mock()

        ui = PygameUI()

        self.assertEqual(ui.width, 1600)
        self.assertEqual(ui.height, 900)
        self.assertFalse(ui.running)
        self.assertIsNone(ui.game)
        mock_pygame.init.assert_called_once()
        mock_display.set_mode.assert_called_once_with((1600, 900))
        mock_display.set_caption.assert_called_once_with("Backgammon Game")

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    def test_init_custom_dimensions(self, mock_board_class, mock_pygame):
        """Test initialization with custom dimensions."""
        mock_display = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = Mock()

        ui = PygameUI(width=1920, height=1080)

        self.assertEqual(ui.width, 1920)
        self.assertEqual(ui.height, 1080)
        mock_display.set_mode.assert_called_once_with((1920, 1080))

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    def test_init_creates_board(self, mock_board_class, mock_pygame):
        """Test that initialization creates a BackgammonBoard instance."""
        mock_display = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = Mock()

        ui = PygameUI(width=1600, height=900)

        mock_board_class.assert_called_once_with(1600, 900)
        self.assertIsNotNone(ui.board)


class TestPygameUIGameSetup(unittest.TestCase):
    """Test PygameUI game setup methods."""

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    def test_set_game(self, mock_board_class, mock_pygame):
        """Test setting the game instance."""
        mock_display = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = Mock()

        ui = PygameUI()
        mock_board = Mock()
        ui.board = mock_board

        mock_game = Mock()
        ui.set_game(mock_game)

        self.assertEqual(ui.game, mock_game)
        mock_board.set_game.assert_called_once_with(mock_game)


class TestPygameUIDisplayMethods(unittest.TestCase):
    """Test PygameUI display methods."""

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    @patch("builtins.print")
    def test_display_message(self, mock_print, mock_board_class, mock_pygame):
        """Test display_message method."""
        mock_display = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = Mock()

        ui = PygameUI()
        ui.display_message("Test message")

        mock_print.assert_called_once_with("Pygame UI: Test message")

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    def test_display_board(self, mock_board_class, mock_pygame):
        """Test display_board method."""
        mock_display = Mock()
        mock_screen = Mock()
        mock_pygame.display = mock_display
        mock_pygame.display.flip = Mock()
        mock_pygame.time.Clock.return_value = Mock()

        ui = PygameUI()
        ui.screen = mock_screen
        mock_board = Mock()
        ui.board = mock_board

        ui.display_board()

        mock_screen.fill.assert_called_once_with(ui.background_color)
        mock_board.render.assert_called_once_with(mock_screen)
        mock_pygame.display.flip.assert_called_once()

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    @patch("builtins.print")
    def test_display_winner(self, mock_print, mock_board_class, mock_pygame):
        """Test display_winner method."""
        mock_display = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = Mock()

        ui = PygameUI()
        ui.display_winner("Player 1")

        mock_print.assert_called_once_with("Winner: Player 1")


class TestPygameUIEventHandling(unittest.TestCase):
    """Test PygameUI event handling."""

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    def test_handle_events_quit(self, mock_board_class, mock_pygame):
        """Test handling QUIT event."""
        mock_display = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = Mock()
        mock_pygame.QUIT = pygame.QUIT

        ui = PygameUI()
        mock_board = Mock()
        ui.board = mock_board

        mock_event = Mock()
        mock_event.type = pygame.QUIT
        mock_pygame.event.get.return_value = [mock_event]
        mock_pygame.mouse.get_pos.return_value = (0, 0)

        result = ui.handle_events()

        self.assertFalse(result)

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    def test_handle_events_escape_key(self, mock_board_class, mock_pygame):
        """Test handling ESC key press."""
        mock_display = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = Mock()
        mock_pygame.KEYDOWN = pygame.KEYDOWN
        mock_pygame.K_ESCAPE = pygame.K_ESCAPE

        ui = PygameUI()
        mock_board = Mock()
        ui.board = mock_board

        mock_event = Mock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_ESCAPE
        mock_pygame.event.get.return_value = [mock_event]
        mock_pygame.mouse.get_pos.return_value = (0, 0)

        result = ui.handle_events()

        self.assertFalse(result)

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    def test_handle_events_mouse_click(self, mock_board_class, mock_pygame):
        """Test handling mouse button click."""
        mock_display = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = Mock()
        mock_pygame.MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN

        ui = PygameUI()
        mock_board = Mock()
        ui.board = mock_board

        mock_event = Mock()
        mock_event.type = pygame.MOUSEBUTTONDOWN
        mock_event.button = 1
        mock_event.pos = (100, 200)
        mock_pygame.event.get.return_value = [mock_event]
        mock_pygame.mouse.get_pos.return_value = (100, 200)

        result = ui.handle_events()

        self.assertTrue(result)
        mock_board.handle_mouse_click.assert_called_once_with((100, 200))

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    def test_handle_events_updates_hover(self, mock_board_class, mock_pygame):
        """Test that handle_events updates hover state."""
        mock_display = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = Mock()

        ui = PygameUI()
        mock_board = Mock()
        ui.board = mock_board

        mock_pygame.event.get.return_value = []
        mock_pygame.mouse.get_pos.return_value = (150, 250)

        result = ui.handle_events()

        self.assertTrue(result)
        mock_board.update_hover_state.assert_called_once_with((150, 250))

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    def test_handle_events_no_events(self, mock_board_class, mock_pygame):
        """Test handle_events with no events."""
        mock_display = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = Mock()

        ui = PygameUI()
        mock_board = Mock()
        ui.board = mock_board

        mock_pygame.event.get.return_value = []
        mock_pygame.mouse.get_pos.return_value = (0, 0)

        result = ui.handle_events()

        self.assertTrue(result)


class TestPygameUIGameLoop(unittest.TestCase):
    """Test PygameUI game loop."""

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    @patch("builtins.print")
    def test_run_game_loop(self, mock_print, mock_board_class, mock_pygame):
        """Test main game loop execution."""
        mock_display = Mock()
        mock_screen = Mock()
        mock_clock = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = mock_clock
        mock_pygame.QUIT = pygame.QUIT

        ui = PygameUI()
        ui.screen = mock_screen
        mock_board = Mock()
        ui.board = mock_board

        # Simulate one iteration then quit
        mock_event = Mock()
        mock_event.type = pygame.QUIT
        mock_pygame.event.get.side_effect = [[mock_event]]
        mock_pygame.mouse.get_pos.return_value = (0, 0)

        ui.run_game()

        # Check that loop was entered
        self.assertFalse(ui.running)
        mock_pygame.quit.assert_called_once()
        mock_clock.tick.assert_called()

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    @patch("builtins.print")
    def test_run_game_prints_messages(self, mock_print, mock_board_class, mock_pygame):
        """Test that run_game prints startup and exit messages."""
        mock_display = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = Mock()
        mock_pygame.QUIT = pygame.QUIT

        ui = PygameUI()

        mock_event = Mock()
        mock_event.type = pygame.QUIT
        mock_pygame.event.get.side_effect = [[mock_event]]
        mock_pygame.mouse.get_pos.return_value = (0, 0)

        ui.run_game()

        # Check for startup and exit messages
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("Starting Backgammon" in str(call) for call in print_calls))
        self.assertTrue(any("Thanks for playing" in str(call) for call in print_calls))


class TestPygameUIPlayerMove(unittest.TestCase):
    """Test PygameUI player move method."""

    @patch("backgammon.pygame_ui.pygame_ui.pygame")
    @patch("backgammon.pygame_ui.pygame_ui.BackgammonBoard")
    def test_get_player_move_returns_none(self, mock_board_class, mock_pygame):
        """Test get_player_move returns None (placeholder)."""
        mock_display = Mock()
        mock_pygame.display = mock_display
        mock_pygame.time.Clock.return_value = Mock()

        ui = PygameUI()
        result = ui.get_player_move()

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
