"""
Unit tests for BoardDimensions class.
Tests board dimension calculations and layout for the Backgammon board.
"""

import unittest
from backgammon.pygame_ui.board_dimensions import BoardDimensions


class TestBoardDimensionsInitialization(unittest.TestCase):
    """Test BoardDimensions initialization."""

    def test_init_default_screen_size(self):
        """Test initialization with default screen size."""
        dimensions = BoardDimensions(1600, 900)

        self.assertEqual(dimensions.screen_width, 1600)
        self.assertEqual(dimensions.screen_height, 900)
        self.assertEqual(dimensions.border_thickness, 20)
        self.assertEqual(dimensions.board_x, 40)
        self.assertEqual(dimensions.board_y, 40)

    def test_init_custom_screen_size(self):
        """Test initialization with custom screen size."""
        dimensions = BoardDimensions(1920, 1080)

        self.assertEqual(dimensions.screen_width, 1920)
        self.assertEqual(dimensions.screen_height, 1080)

    def test_board_dimensions_calculated_correctly(self):
        """Test that board dimensions are calculated from screen size."""
        dimensions = BoardDimensions(1600, 900)

        expected_board_width = 1600 - (2 * 40)
        expected_board_height = 900 - (2 * 40)

        self.assertEqual(dimensions.board_width, expected_board_width)
        self.assertEqual(dimensions.board_height, expected_board_height)

    def test_bar_and_panel_widths(self):
        """Test bar and side panel width constants."""
        dimensions = BoardDimensions(1600, 900)

        self.assertEqual(dimensions.bar_width, 50)
        self.assertEqual(dimensions.side_panel_width, 80)

    def test_playable_width_calculation(self):
        """Test playable area width calculation."""
        dimensions = BoardDimensions(1600, 900)

        expected_playable = (
            dimensions.board_width
            - dimensions.bar_width
            - dimensions.side_panel_width
            - (2 * dimensions.border_thickness)
        )

        self.assertEqual(dimensions.playable_width, expected_playable)

    def test_half_width_calculation(self):
        """Test half width calculation for each side of board."""
        dimensions = BoardDimensions(1600, 900)

        expected_half_width = dimensions.playable_width // 2
        self.assertEqual(dimensions.half_width, expected_half_width)

    def test_point_dimensions_calculated(self):
        """Test that point width and height are calculated."""
        dimensions = BoardDimensions(1600, 900)

        expected_point_width = dimensions.half_width // 6
        self.assertEqual(dimensions.point_width, expected_point_width)

        expected_point_height = (
            dimensions.board_height - (2 * dimensions.border_thickness)
        ) // 2 - 10
        self.assertEqual(dimensions.point_height, expected_point_height)


class TestBoardDimensionsRectangles(unittest.TestCase):
    """Test board rectangle calculations."""

    def setUp(self):
        """Set up test fixtures."""
        self.dimensions = BoardDimensions(1600, 900)

    def test_get_board_rect(self):
        """Test get_board_rect method."""
        rect = self.dimensions.get_board_rect()

        self.assertIsInstance(rect, tuple)
        self.assertEqual(len(rect), 4)
        self.assertEqual(rect[0], self.dimensions.board_x)
        self.assertEqual(rect[1], self.dimensions.board_y)
        self.assertEqual(rect[2], self.dimensions.board_width)
        self.assertEqual(rect[3], self.dimensions.board_height)

    def test_get_inner_board_rect(self):
        """Test get_inner_board_rect method."""
        rect = self.dimensions.get_inner_board_rect()

        self.assertIsInstance(rect, tuple)
        self.assertEqual(len(rect), 4)

        expected_x = self.dimensions.board_x + self.dimensions.border_thickness
        expected_y = self.dimensions.board_y + self.dimensions.border_thickness
        expected_width = self.dimensions.board_width - (
            2 * self.dimensions.border_thickness
        )
        expected_height = self.dimensions.board_height - (
            2 * self.dimensions.border_thickness
        )

        self.assertEqual(rect[0], expected_x)
        self.assertEqual(rect[1], expected_y)
        self.assertEqual(rect[2], expected_width)
        self.assertEqual(rect[3], expected_height)

    def test_get_bar_rect(self):
        """Test get_bar_rect method."""
        rect = self.dimensions.get_bar_rect()

        self.assertIsInstance(rect, tuple)
        self.assertEqual(len(rect), 4)

        expected_x = (
            self.dimensions.board_x
            + self.dimensions.border_thickness
            + self.dimensions.half_width
        )
        expected_y = self.dimensions.board_y + self.dimensions.border_thickness
        expected_width = self.dimensions.bar_width
        expected_height = self.dimensions.board_height - (
            2 * self.dimensions.border_thickness
        )

        self.assertEqual(rect[0], expected_x)
        self.assertEqual(rect[1], expected_y)
        self.assertEqual(rect[2], expected_width)
        self.assertEqual(rect[3], expected_height)

    def test_get_side_panel_rect(self):
        """Test get_side_panel_rect method."""
        rect = self.dimensions.get_side_panel_rect()

        self.assertIsInstance(rect, tuple)
        self.assertEqual(len(rect), 4)

        expected_x = (
            self.dimensions.board_x
            + self.dimensions.board_width
            - self.dimensions.border_thickness
            - self.dimensions.side_panel_width
        )
        expected_y = self.dimensions.board_y + self.dimensions.border_thickness
        expected_width = self.dimensions.side_panel_width
        expected_height = self.dimensions.board_height - (
            2 * self.dimensions.border_thickness
        )

        self.assertEqual(rect[0], expected_x)
        self.assertEqual(rect[1], expected_y)
        self.assertEqual(rect[2], expected_width)
        self.assertEqual(rect[3], expected_height)


class TestBoardDimensionsPointPositions(unittest.TestCase):
    """Test point position calculations."""

    def setUp(self):
        """Set up test fixtures."""
        self.dimensions = BoardDimensions(1600, 900)

    def test_get_point_base_y_top(self):
        """Test get_point_base_y for top points."""
        base_y = self.dimensions.get_point_base_y(is_top=True)

        expected_y = self.dimensions.board_y + self.dimensions.border_thickness
        self.assertEqual(base_y, expected_y)

    def test_get_point_base_y_bottom(self):
        """Test get_point_base_y for bottom points."""
        base_y = self.dimensions.get_point_base_y(is_top=False)

        expected_y = (
            self.dimensions.board_y
            + self.dimensions.border_thickness
            + self.dimensions.board_height
            - (2 * self.dimensions.border_thickness)
        )
        self.assertEqual(base_y, expected_y)

    def test_get_point_x_top_right_quadrant(self):
        """Test get_point_x for top right quadrant (points 0-5)."""
        for point in range(6):
            x = self.dimensions.get_point_x(point)
            self.assertIsInstance(x, int)
            self.assertGreaterEqual(x, 0)

    def test_get_point_x_top_left_quadrant(self):
        """Test get_point_x for top left quadrant (points 6-11)."""
        for point in range(6, 12):
            x = self.dimensions.get_point_x(point)
            self.assertIsInstance(x, int)
            self.assertGreaterEqual(x, 0)

    def test_get_point_x_bottom_left_quadrant(self):
        """Test get_point_x for bottom left quadrant (points 12-17)."""
        for point in range(12, 18):
            x = self.dimensions.get_point_x(point)
            self.assertIsInstance(x, int)
            self.assertGreaterEqual(x, 0)

    def test_get_point_x_bottom_right_quadrant(self):
        """Test get_point_x for bottom right quadrant (points 18-23)."""
        for point in range(18, 24):
            x = self.dimensions.get_point_x(point)
            self.assertIsInstance(x, int)
            self.assertGreaterEqual(x, 0)

    def test_get_point_x_all_points_valid(self):
        """Test that all 24 points return valid x coordinates."""
        for point in range(24):
            x = self.dimensions.get_point_x(point)
            self.assertIsInstance(x, int)
            self.assertGreater(x, 0)

    def test_get_point_x_points_are_spaced_correctly(self):
        """Test that points are spaced by point_width."""
        # Points in same quadrant should be spaced by point_width
        x0 = self.dimensions.get_point_x(0)
        x1 = self.dimensions.get_point_x(1)

        self.assertEqual(abs(x1 - x0), self.dimensions.point_width)


class TestBoardDimensionsDifferentScreenSizes(unittest.TestCase):
    """Test BoardDimensions with different screen sizes."""

    def test_small_screen(self):
        """Test with small screen size."""
        dimensions = BoardDimensions(800, 600)

        self.assertEqual(dimensions.screen_width, 800)
        self.assertEqual(dimensions.screen_height, 600)
        self.assertGreater(dimensions.point_width, 0)
        self.assertGreater(dimensions.point_height, 0)

    def test_large_screen(self):
        """Test with large screen size."""
        dimensions = BoardDimensions(1920, 1080)

        self.assertEqual(dimensions.screen_width, 1920)
        self.assertEqual(dimensions.screen_height, 1080)
        self.assertGreater(dimensions.point_width, 0)
        self.assertGreater(dimensions.point_height, 0)

    def test_ultrawide_screen(self):
        """Test with ultrawide screen size."""
        dimensions = BoardDimensions(2560, 1440)

        self.assertEqual(dimensions.screen_width, 2560)
        self.assertEqual(dimensions.screen_height, 1440)
        self.assertGreater(dimensions.point_width, 0)
        self.assertGreater(dimensions.point_height, 0)


if __name__ == "__main__":
    unittest.main()
