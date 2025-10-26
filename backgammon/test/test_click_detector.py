"""
Unit tests for ClickDetector class.
Tests click detection and coordinate conversion for the Backgammon board.
"""

import unittest
from backgammon.pygame_ui.click_detector import ClickDetector
from backgammon.pygame_ui.board_dimensions import BoardDimensions


class TestClickDetectorInitialization(unittest.TestCase):
    """Test ClickDetector initialization."""

    def test_init_with_dimensions(self):
        """Test initialization with BoardDimensions instance."""
        dimensions = BoardDimensions(1600, 900)
        detector = ClickDetector(dimensions)

        self.assertEqual(detector.dimensions, dimensions)


class TestClickDetectorPointDetection(unittest.TestCase):
    """Test point click detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.dimensions = BoardDimensions(1600, 900)
        self.detector = ClickDetector(self.dimensions)

    def test_get_clicked_point_outside_board(self):
        """Test clicking outside board returns None."""
        result = self.detector.get_clicked_point((0, 0))
        self.assertIsNone(result)

    def test_get_clicked_point_in_bar_area(self):
        """Test clicking in bar area returns None."""
        bar_rect = self.dimensions.get_bar_rect()
        bar_center_x = bar_rect[0] + (bar_rect[2] // 2)
        bar_center_y = bar_rect[1] + (bar_rect[3] // 2)

        result = self.detector.get_clicked_point((bar_center_x, bar_center_y))
        self.assertIsNone(result)

    def test_get_clicked_point_in_side_panel(self):
        """Test clicking in side panel returns None."""
        panel_rect = self.dimensions.get_side_panel_rect()
        panel_center_x = panel_rect[0] + (panel_rect[2] // 2)
        panel_center_y = panel_rect[1] + (panel_rect[3] // 2)

        result = self.detector.get_clicked_point((panel_center_x, panel_center_y))
        self.assertIsNone(result)

    def test_get_clicked_point_valid_top_left_point(self):
        """Test clicking on a valid top left point."""
        point_x = self.dimensions.get_point_x(11)
        point_y = self.dimensions.get_point_base_y(is_top=True) + 50

        result = self.detector.get_clicked_point((point_x + 10, point_y))

        self.assertIsNotNone(result)
        self.assertIn(result, range(24))

    def test_get_clicked_point_valid_top_right_point(self):
        """Test clicking on a valid top right point."""
        point_x = self.dimensions.get_point_x(0)
        point_y = self.dimensions.get_point_base_y(is_top=True) + 50

        result = self.detector.get_clicked_point((point_x + 10, point_y))

        self.assertIsNotNone(result)
        self.assertIn(result, range(24))

    def test_get_clicked_point_valid_bottom_left_point(self):
        """Test clicking on a valid bottom left point."""
        point_x = self.dimensions.get_point_x(12)
        point_y = self.dimensions.get_point_base_y(is_top=False) - 50

        result = self.detector.get_clicked_point((point_x + 10, point_y))

        self.assertIsNotNone(result)
        self.assertIn(result, range(24))

    def test_get_clicked_point_valid_bottom_right_point(self):
        """Test clicking on a valid bottom right point."""
        point_x = self.dimensions.get_point_x(18)
        point_y = self.dimensions.get_point_base_y(is_top=False) - 50

        result = self.detector.get_clicked_point((point_x + 10, point_y))

        self.assertIsNotNone(result)
        self.assertIn(result, range(24))


class TestClickDetectorBarDetection(unittest.TestCase):
    """Test bar click detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.dimensions = BoardDimensions(1600, 900)
        self.detector = ClickDetector(self.dimensions)

    def test_is_bar_clicked_true(self):
        """Test is_bar_clicked returns True when bar is clicked."""
        bar_rect = self.dimensions.get_bar_rect()
        bar_center_x = bar_rect[0] + (bar_rect[2] // 2)
        bar_center_y = bar_rect[1] + (bar_rect[3] // 2)

        result = self.detector.is_bar_clicked((bar_center_x, bar_center_y))
        self.assertTrue(result)

    def test_is_bar_clicked_false_outside(self):
        """Test is_bar_clicked returns False when outside bar."""
        result = self.detector.is_bar_clicked((0, 0))
        self.assertFalse(result)

    def test_is_bar_clicked_at_edges(self):
        """Test is_bar_clicked at bar edges."""
        bar_rect = self.dimensions.get_bar_rect()

        # Left edge
        result = self.detector.is_bar_clicked((bar_rect[0], bar_rect[1] + 50))
        self.assertTrue(result)

        # Right edge
        result = self.detector.is_bar_clicked(
            (bar_rect[0] + bar_rect[2], bar_rect[1] + 50)
        )
        self.assertTrue(result)


class TestClickDetectorOffAreaDetection(unittest.TestCase):
    """Test off area click detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.dimensions = BoardDimensions(1600, 900)
        self.detector = ClickDetector(self.dimensions)

    def test_is_off_area_clicked_true_middle_section(self):
        """Test is_off_area_clicked returns True for middle section."""
        panel_rect = self.dimensions.get_side_panel_rect()
        section_height = panel_rect[3] // 3
        middle_y = panel_rect[1] + section_height + (section_height // 2)
        center_x = panel_rect[0] + (panel_rect[2] // 2)

        result = self.detector.is_off_area_clicked((center_x, middle_y))
        self.assertTrue(result)

    def test_is_off_area_clicked_false_outside(self):
        """Test is_off_area_clicked returns False outside off area."""
        result = self.detector.is_off_area_clicked((0, 0))
        self.assertFalse(result)

    def test_is_off_area_clicked_false_top_section(self):
        """Test is_off_area_clicked returns False for top section."""
        panel_rect = self.dimensions.get_side_panel_rect()
        top_y = panel_rect[1] + 20
        center_x = panel_rect[0] + (panel_rect[2] // 2)

        result = self.detector.is_off_area_clicked((center_x, top_y))
        self.assertFalse(result)

    def test_is_off_area_clicked_false_bottom_section(self):
        """Test is_off_area_clicked returns False for bottom section."""
        panel_rect = self.dimensions.get_side_panel_rect()
        section_height = panel_rect[3] // 3
        bottom_y = panel_rect[1] + (2 * section_height) + 20
        center_x = panel_rect[0] + (panel_rect[2] // 2)

        result = self.detector.is_off_area_clicked((center_x, bottom_y))
        self.assertFalse(result)


class TestClickDetectorGetClickedPosition(unittest.TestCase):
    """Test get_clicked_position composite method."""

    def setUp(self):
        """Set up test fixtures."""
        self.dimensions = BoardDimensions(1600, 900)
        self.detector = ClickDetector(self.dimensions)

    def test_get_clicked_position_bar(self):
        """Test get_clicked_position returns bar position."""
        bar_rect = self.dimensions.get_bar_rect()
        bar_center = (bar_rect[0] + bar_rect[2] // 2, bar_rect[1] + bar_rect[3] // 2)

        result = self.detector.get_clicked_position(bar_center)

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "bar")
        self.assertEqual(result[1], 0)

    def test_get_clicked_position_off(self):
        """Test get_clicked_position returns off position."""
        panel_rect = self.dimensions.get_side_panel_rect()
        section_height = panel_rect[3] // 3
        middle_y = panel_rect[1] + section_height + (section_height // 2)
        center_x = panel_rect[0] + (panel_rect[2] // 2)

        result = self.detector.get_clicked_position((center_x, middle_y))

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "off")
        self.assertEqual(result[1], 0)

    def test_get_clicked_position_point(self):
        """Test get_clicked_position returns point position."""
        point_x = self.dimensions.get_point_x(12)
        point_y = self.dimensions.get_point_base_y(is_top=False) - 50

        result = self.detector.get_clicked_position((point_x + 10, point_y))

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "point")
        self.assertIsInstance(result[1], int)
        self.assertIn(result[1], range(24))

    def test_get_clicked_position_none(self):
        """Test get_clicked_position returns None for invalid position."""
        result = self.detector.get_clicked_position((0, 0))
        self.assertIsNone(result)


class TestClickDetectorButtonDetection(unittest.TestCase):
    """Test button click detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.dimensions = BoardDimensions(1600, 900)
        self.detector = ClickDetector(self.dimensions)

    def test_get_dice_roll_button_rect(self):
        """Test get_dice_roll_button_rect returns valid rectangle."""
        button_rect = self.detector.get_dice_roll_button_rect()

        self.assertIsInstance(button_rect, tuple)
        self.assertEqual(len(button_rect), 4)
        self.assertEqual(button_rect[2], 60)  # width
        self.assertEqual(button_rect[3], 30)  # height

    def test_is_roll_button_clicked_true(self):
        """Test is_roll_button_clicked returns True when button clicked."""
        button_rect = self.detector.get_dice_roll_button_rect()
        button_center = (
            button_rect[0] + button_rect[2] // 2,
            button_rect[1] + button_rect[3] // 2,
        )

        result = self.detector.is_roll_button_clicked(button_center)
        self.assertTrue(result)

    def test_is_roll_button_clicked_false_outside(self):
        """Test is_roll_button_clicked returns False when outside button."""
        result = self.detector.is_roll_button_clicked((0, 0))
        self.assertFalse(result)

    def test_is_roll_button_clicked_at_edges(self):
        """Test is_roll_button_clicked at button edges."""
        button_rect = self.detector.get_dice_roll_button_rect()

        # Inside button
        result = self.detector.is_roll_button_clicked(
            (button_rect[0] + 1, button_rect[1] + 1)
        )
        self.assertTrue(result)


class TestClickDetectorEdgeCases(unittest.TestCase):
    """Test edge cases for ClickDetector."""

    def setUp(self):
        """Set up test fixtures."""
        self.dimensions = BoardDimensions(1600, 900)
        self.detector = ClickDetector(self.dimensions)

    def test_negative_coordinates(self):
        """Test handling of negative coordinates."""
        result = self.detector.get_clicked_point((-10, -10))
        self.assertIsNone(result)

    def test_very_large_coordinates(self):
        """Test handling of very large coordinates."""
        result = self.detector.get_clicked_point((10000, 10000))
        self.assertIsNone(result)

    def test_exact_border_coordinates(self):
        """Test clicking exactly on board border."""
        inner_rect = self.dimensions.get_inner_board_rect()
        result = self.detector.get_clicked_point((inner_rect[0], inner_rect[1]))
        # Should be inside board area
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
