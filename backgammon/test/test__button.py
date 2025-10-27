"""
Unit tests for Button class.
Tests button component including rendering, hover, and click detection.
"""

import unittest
from unittest.mock import Mock, patch
import pygame
from backgammon.pygame_ui.button import Button
from backgammon.pygame_ui.color_scheme import ColorScheme
from backgammon.pygame_ui.board_dimensions import BoardDimensions


class TestButtonInitialization(unittest.TestCase):
    """Test Button initialization."""

    @patch("backgammon.pygame_ui.button.pygame.Rect")
    def test_init_default_font_size(self, mock_rect_class):
        """Test initialization with default font size."""
        colors = ColorScheme()
        dimensions = BoardDimensions(1600, 900)
        rect = pygame.Rect(100, 100, 150, 50)

        button = Button(colors, dimensions, "Test Button", rect)

        self.assertEqual(button.colors, colors)
        self.assertEqual(button.dimensions, dimensions)
        self.assertEqual(button.text, "Test Button")
        self.assertEqual(button.button_rect, rect)
        self.assertEqual(button.font_size, 32)
        self.assertFalse(button.is_hovered)
        self.assertTrue(button.is_enabled)

    @patch("backgammon.pygame_ui.button.pygame.Rect")
    def test_init_custom_font_size(self, mock_rect_class):
        """Test initialization with custom font size."""
        colors = ColorScheme()
        dimensions = BoardDimensions(1600, 900)
        rect = pygame.Rect(100, 100, 150, 50)

        button = Button(colors, dimensions, "Test", rect, font_size=24)

        self.assertEqual(button.font_size, 24)


class TestButtonHoverState(unittest.TestCase):
    """Test Button hover state management."""

    @patch("backgammon.pygame_ui.button.pygame.Rect")
    def test_update_hover_state_inside(self, mock_rect_class):
        """Test update_hover_state when mouse is inside button."""
        colors = ColorScheme()
        dimensions = BoardDimensions(1600, 900)
        rect = Mock()
        rect.collidepoint.return_value = True

        button = Button(colors, dimensions, "Test", rect)
        button.update_hover_state((150, 125))

        self.assertTrue(button.is_hovered)
        rect.collidepoint.assert_called_once_with((150, 125))

    @patch("backgammon.pygame_ui.button.pygame.Rect")
    def test_update_hover_state_outside(self, mock_rect_class):
        """Test update_hover_state when mouse is outside button."""
        colors = ColorScheme()
        dimensions = BoardDimensions(1600, 900)
        rect = Mock()
        rect.collidepoint.return_value = False

        button = Button(colors, dimensions, "Test", rect)
        button.update_hover_state((50, 50))

        self.assertFalse(button.is_hovered)
        rect.collidepoint.assert_called_once_with((50, 50))


class TestButtonClickDetection(unittest.TestCase):
    """Test Button click detection."""

    @patch("backgammon.pygame_ui.button.pygame.Rect")
    def test_is_clicked_enabled_and_inside(self, mock_rect_class):
        """Test is_clicked returns True when enabled and inside."""
        colors = ColorScheme()
        dimensions = BoardDimensions(1600, 900)
        rect = Mock()
        rect.collidepoint.return_value = True

        button = Button(colors, dimensions, "Test", rect)
        button.is_enabled = True

        result = button.is_clicked((150, 125))

        self.assertTrue(result)
        rect.collidepoint.assert_called_once_with((150, 125))

    @patch("backgammon.pygame_ui.button.pygame.Rect")
    def test_is_clicked_disabled(self, mock_rect_class):
        """Test is_clicked returns False when disabled."""
        colors = ColorScheme()
        dimensions = BoardDimensions(1600, 900)
        rect = Mock()
        rect.collidepoint.return_value = True

        button = Button(colors, dimensions, "Test", rect)
        button.is_enabled = False

        result = button.is_clicked((150, 125))

        self.assertFalse(result)

    @patch("backgammon.pygame_ui.button.pygame.Rect")
    def test_is_clicked_outside(self, mock_rect_class):
        """Test is_clicked returns False when outside."""
        colors = ColorScheme()
        dimensions = BoardDimensions(1600, 900)
        rect = Mock()
        rect.collidepoint.return_value = False

        button = Button(colors, dimensions, "Test", rect)
        button.is_enabled = True

        result = button.is_clicked((50, 50))

        self.assertFalse(result)


class TestButtonEnableDisable(unittest.TestCase):
    """Test Button enable/disable functionality."""

    @patch("backgammon.pygame_ui.button.pygame.Rect")
    def test_set_enabled_true(self, mock_rect_class):
        """Test set_enabled with True."""
        colors = ColorScheme()
        dimensions = BoardDimensions(1600, 900)
        rect = pygame.Rect(100, 100, 150, 50)

        button = Button(colors, dimensions, "Test", rect)
        button.is_enabled = False

        button.set_enabled(True)

        self.assertTrue(button.is_enabled)

    @patch("backgammon.pygame_ui.button.pygame.Rect")
    def test_set_enabled_false(self, mock_rect_class):
        """Test set_enabled with False."""
        colors = ColorScheme()
        dimensions = BoardDimensions(1600, 900)
        rect = pygame.Rect(100, 100, 150, 50)

        button = Button(colors, dimensions, "Test", rect)
        button.is_enabled = True

        button.set_enabled(False)

        self.assertFalse(button.is_enabled)


class TestButtonRendering(unittest.TestCase):
    """Test Button rendering."""

    @patch("backgammon.pygame_ui.button.pygame.font.Font")
    @patch("backgammon.pygame_ui.button.pygame.draw.rect")
    @patch("backgammon.pygame_ui.button.pygame.Rect")
    def test_render_enabled_not_hovered(
        self, mock_rect_class, mock_draw_rect, mock_font
    ):
        """Test render when enabled and not hovered."""
        colors = ColorScheme()
        dimensions = BoardDimensions(1600, 900)
        rect = Mock()
        rect.center = (100, 100)

        mock_text_surface = Mock()
        mock_text_rect = Mock()
        mock_text_surface.get_rect.return_value = mock_text_rect
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = mock_text_surface
        mock_font.return_value = mock_font_instance

        button = Button(colors, dimensions, "Test", rect)
        button.is_enabled = True
        button.is_hovered = False

        mock_surface = Mock()
        button.render(mock_surface)

        # Should call draw.rect twice (fill and border)
        self.assertEqual(mock_draw_rect.call_count, 2)
        # Should render text
        mock_font_instance.render.assert_called_once_with("Test", True, (255, 255, 255))

    @patch("backgammon.pygame_ui.button.pygame.font.Font")
    @patch("backgammon.pygame_ui.button.pygame.draw.rect")
    @patch("backgammon.pygame_ui.button.pygame.Rect")
    def test_render_enabled_hovered(self, mock_rect_class, mock_draw_rect, mock_font):
        """Test render when enabled and hovered."""
        colors = ColorScheme()
        dimensions = BoardDimensions(1600, 900)
        rect = Mock()
        rect.center = (100, 100)

        mock_text_surface = Mock()
        mock_text_rect = Mock()
        mock_text_surface.get_rect.return_value = mock_text_rect
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = mock_text_surface
        mock_font.return_value = mock_font_instance

        button = Button(colors, dimensions, "Test", rect)
        button.is_enabled = True
        button.is_hovered = True

        mock_surface = Mock()
        button.render(mock_surface)

        # Should use hover colors
        self.assertEqual(mock_draw_rect.call_count, 2)

    @patch("backgammon.pygame_ui.button.pygame.font.Font")
    @patch("backgammon.pygame_ui.button.pygame.draw.rect")
    @patch("backgammon.pygame_ui.button.pygame.Rect")
    def test_render_disabled(self, mock_rect_class, mock_draw_rect, mock_font):
        """Test render when disabled."""
        colors = ColorScheme()
        dimensions = BoardDimensions(1600, 900)
        rect = Mock()
        rect.center = (100, 100)

        mock_text_surface = Mock()
        mock_text_rect = Mock()
        mock_text_surface.get_rect.return_value = mock_text_rect
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = mock_text_surface
        mock_font.return_value = mock_font_instance

        button = Button(colors, dimensions, "Test", rect)
        button.is_enabled = False

        mock_surface = Mock()
        button.render(mock_surface)

        # Should use disabled colors
        self.assertEqual(mock_draw_rect.call_count, 2)


if __name__ == "__main__":
    unittest.main()
