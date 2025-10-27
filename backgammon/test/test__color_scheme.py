"""
Unit tests for ColorScheme class.
Tests color definitions and attributes for the Backgammon board.
"""

import unittest
from backgammon.pygame_ui.color_scheme import ColorScheme


class TestColorSchemeAttributes(unittest.TestCase):
    """Test ColorScheme color attribute definitions."""

    def setUp(self):
        """Set up test fixtures."""
        self.colors = ColorScheme()

    def test_wood_orange_color(self):
        """Test WOOD_ORANGE color definition."""
        self.assertEqual(self.colors.WOOD_ORANGE, (210, 150, 90))
        self.assertIsInstance(self.colors.WOOD_ORANGE, tuple)
        self.assertEqual(len(self.colors.WOOD_ORANGE), 3)

    def test_dark_brown_color(self):
        """Test DARK_BROWN color definition."""
        self.assertEqual(self.colors.DARK_BROWN, (60, 40, 20))
        self.assertIsInstance(self.colors.DARK_BROWN, tuple)
        self.assertEqual(len(self.colors.DARK_BROWN), 3)

    def test_light_beige_color(self):
        """Test LIGHT_BEIGE color definition."""
        self.assertEqual(self.colors.LIGHT_BEIGE, (220, 200, 170))
        self.assertIsInstance(self.colors.LIGHT_BEIGE, tuple)
        self.assertEqual(len(self.colors.LIGHT_BEIGE), 3)

    def test_dark_brown_point_color(self):
        """Test DARK_BROWN_POINT color definition."""
        self.assertEqual(self.colors.DARK_BROWN_POINT, (100, 70, 40))
        self.assertIsInstance(self.colors.DARK_BROWN_POINT, tuple)
        self.assertEqual(len(self.colors.DARK_BROWN_POINT), 3)

    def test_green_bar_color(self):
        """Test GREEN_BAR color definition."""
        self.assertEqual(self.colors.GREEN_BAR, (40, 100, 60))
        self.assertIsInstance(self.colors.GREEN_BAR, tuple)
        self.assertEqual(len(self.colors.GREEN_BAR), 3)

    def test_brass_color(self):
        """Test BRASS color definition."""
        self.assertEqual(self.colors.BRASS, (180, 150, 80))
        self.assertIsInstance(self.colors.BRASS, tuple)
        self.assertEqual(len(self.colors.BRASS), 3)

    def test_green_stripe_color(self):
        """Test GREEN_STRIPE color definition."""
        self.assertEqual(self.colors.GREEN_STRIPE, (50, 120, 70))
        self.assertIsInstance(self.colors.GREEN_STRIPE, tuple)
        self.assertEqual(len(self.colors.GREEN_STRIPE), 3)

    def test_yellow_stripe_color(self):
        """Test YELLOW_STRIPE color definition."""
        self.assertEqual(self.colors.YELLOW_STRIPE, (200, 180, 60))
        self.assertIsInstance(self.colors.YELLOW_STRIPE, tuple)
        self.assertEqual(len(self.colors.YELLOW_STRIPE), 3)

    def test_black_color(self):
        """Test BLACK color definition."""
        self.assertEqual(self.colors.BLACK, (0, 0, 0))
        self.assertIsInstance(self.colors.BLACK, tuple)
        self.assertEqual(len(self.colors.BLACK), 3)


class TestColorSchemeRGBValues(unittest.TestCase):
    """Test that color values are valid RGB tuples."""

    def setUp(self):
        """Set up test fixtures."""
        self.colors = ColorScheme()

    def test_all_colors_have_valid_rgb_ranges(self):
        """Test that all color values are in valid RGB range (0-255)."""
        color_attributes = [
            "WOOD_ORANGE",
            "DARK_BROWN",
            "LIGHT_BEIGE",
            "DARK_BROWN_POINT",
            "GREEN_BAR",
            "BRASS",
            "GREEN_STRIPE",
            "YELLOW_STRIPE",
            "BLACK",
        ]

        for attr_name in color_attributes:
            color = getattr(self.colors, attr_name)
            for component in color:
                self.assertGreaterEqual(
                    component, 0, f"{attr_name} has component less than 0: {component}"
                )
                self.assertLessEqual(
                    component,
                    255,
                    f"{attr_name} has component greater than 255: {component}",
                )

    def test_all_colors_are_tuples_of_three_integers(self):
        """Test that all colors are tuples of exactly three integers."""
        color_attributes = [
            "WOOD_ORANGE",
            "DARK_BROWN",
            "LIGHT_BEIGE",
            "DARK_BROWN_POINT",
            "GREEN_BAR",
            "BRASS",
            "GREEN_STRIPE",
            "YELLOW_STRIPE",
            "BLACK",
        ]

        for attr_name in color_attributes:
            color = getattr(self.colors, attr_name)
            self.assertIsInstance(color, tuple, f"{attr_name} is not a tuple")
            self.assertEqual(len(color), 3, f"{attr_name} does not have 3 components")
            for component in color:
                self.assertIsInstance(
                    component,
                    int,
                    f"{attr_name} has non-integer component: {component}",
                )


class TestColorSchemeColorDistinctness(unittest.TestCase):
    """Test that colors are distinct from each other."""

    def setUp(self):
        """Set up test fixtures."""
        self.colors = ColorScheme()

    def test_point_colors_are_different(self):
        """Test that point colors (LIGHT_BEIGE and DARK_BROWN_POINT) are different."""
        self.assertNotEqual(self.colors.LIGHT_BEIGE, self.colors.DARK_BROWN_POINT)

    def test_stripe_colors_are_different(self):
        """Test that stripe colors (GREEN_STRIPE and YELLOW_STRIPE) are different."""
        self.assertNotEqual(self.colors.GREEN_STRIPE, self.colors.YELLOW_STRIPE)

    def test_brown_colors_are_different(self):
        """Test that different brown colors are distinct."""
        self.assertNotEqual(self.colors.DARK_BROWN, self.colors.DARK_BROWN_POINT)
        self.assertNotEqual(self.colors.DARK_BROWN, self.colors.WOOD_ORANGE)
        self.assertNotEqual(self.colors.DARK_BROWN_POINT, self.colors.WOOD_ORANGE)

    def test_black_is_pure_black(self):
        """Test that BLACK is exactly (0, 0, 0)."""
        self.assertEqual(self.colors.BLACK, (0, 0, 0))


if __name__ == "__main__":
    unittest.main()
