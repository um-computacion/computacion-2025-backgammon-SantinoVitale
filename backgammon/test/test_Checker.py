"""
Test module for Checker class.

This module contains unit tests for the Checker class which represents
individual checker pieces in the backgammon game.
"""

import unittest
from backgammon.core import Checker

# pylint: disable=C0116  # many simple test methods without individual docstrings
# pylint: disable=C0103  # module name follows test naming convention
# pylint: disable=R0904  # many public methods needed for comprehensive testing


class TestChecker(unittest.TestCase):
    """Test cases for the Checker class."""

    def setUp(self):
        self.white_checker = Checker("white")
        self.black_checker = Checker("black")

    def test_checker_initialization_with_color(self):
        self.assertEqual(self.white_checker.color, "white")
        self.assertEqual(self.black_checker.color, "black")
        self.assertIsNone(self.white_checker.position)
        self.assertIsNone(self.black_checker.position)

    def test_checker_initialization_without_color(self):
        checker = Checker()
        self.assertIsNone(checker.color)
        self.assertIsNone(checker.position)

    def test_invalid_color_initialization(self):
        with self.assertRaises(ValueError):
            Checker("red")
        with self.assertRaises(ValueError):
            Checker("blue")

    def test_set_position_valid(self):
        self.white_checker.set_position(5)
        self.assertEqual(self.white_checker.position, 5)
        self.white_checker.set_position(1)
        self.assertEqual(self.white_checker.position, 1)
        self.white_checker.set_position(24)
        self.assertEqual(self.white_checker.position, 24)

    def test_set_position_invalid(self):
        with self.assertRaises(ValueError):
            self.white_checker.set_position(0)

        with self.assertRaises(ValueError):
            self.white_checker.set_position(25)

        with self.assertRaises(ValueError):
            self.white_checker.set_position(-1)

    def test_set_position_special_locations(self):
        self.white_checker.set_position("bar")
        self.assertEqual(self.white_checker.position, "bar")
        self.white_checker.set_position("off")
        self.assertEqual(self.white_checker.position, "off")

    def test_get_position(self):
        self.assertIsNone(self.white_checker.get_position())
        self.white_checker.set_position(10)
        self.assertEqual(self.white_checker.get_position(), 10)

    def test_is_on_board(self):
        self.assertFalse(self.white_checker.is_on_board())
        self.white_checker.set_position(5)
        self.assertTrue(self.white_checker.is_on_board())
        self.white_checker.set_position("bar")
        self.assertFalse(self.white_checker.is_on_board())
        self.white_checker.set_position("off")
        self.assertFalse(self.white_checker.is_on_board())

    def test_is_on_bar(self):
        self.assertFalse(self.white_checker.is_on_bar())
        self.white_checker.set_position("bar")
        self.assertTrue(self.white_checker.is_on_bar())
        self.white_checker.set_position(5)
        self.assertFalse(self.white_checker.is_on_bar())

    def test_is_off_board(self):
        self.assertFalse(self.white_checker.is_off_board())
        self.white_checker.set_position("off")
        self.assertTrue(self.white_checker.is_off_board())
        self.white_checker.set_position(5)
        self.assertFalse(self.white_checker.is_off_board())

    def test_move_to_bar(self):
        self.white_checker.set_position(5)
        self.white_checker.move_to_bar()
        self.assertEqual(self.white_checker.position, "bar")
        self.assertTrue(self.white_checker.is_on_bar())

    def test_move_off_board(self):
        self.white_checker.set_position(1)
        self.white_checker.move_off_board()
        self.assertEqual(self.white_checker.position, "off")
        self.assertTrue(self.white_checker.is_off_board())

    def test_checker_equality(self):
        checker1 = Checker("white")
        checker2 = Checker("white")
        checker3 = Checker("black")
        self.assertEqual(checker1.color, checker2.color)
        self.assertNotEqual(checker1.color, checker3.color)

    def test_checker_inequality(self):
        self.assertNotEqual(self.white_checker.color, self.black_checker.color)

    def test_checker_str_representation(self):
        white_str = str(self.white_checker)
        self.assertIn("white", white_str.lower())
        black_str = str(self.black_checker)
        self.assertIn("black", black_str.lower())
        self.white_checker.set_position(5)
        positioned_str = str(self.white_checker)
        self.assertIn("5", positioned_str)

    def test_checker_repr_representation(self):
        repr_str = repr(self.white_checker)
        self.assertIn("Checker", repr_str)
        self.assertIn("white", repr_str)

    def test_copy_checker(self):
        self.white_checker.set_position(10)
        copied_checker = self.white_checker.copy()
        self.assertEqual(copied_checker.color, self.white_checker.color)
        self.assertEqual(copied_checker.position, self.white_checker.position)
        self.assertIsNot(copied_checker, self.white_checker)

    def test_reset_position(self):
        self.white_checker.set_position(15)
        self.white_checker.reset_position()
        self.assertIsNone(self.white_checker.position)

    def test_get_direction(self):
        self.assertEqual(self.white_checker.get_direction(), -1)
        self.assertEqual(self.black_checker.get_direction(), 1)

    def test_can_bear_off(self):
        for pos in range(1, 7):
            self.white_checker.set_position(pos)
            self.assertTrue(self.white_checker.can_bear_off())

        for pos in range(7, 25):
            self.white_checker.set_position(pos)
            self.assertFalse(self.white_checker.can_bear_off())

        for pos in range(19, 25):
            self.black_checker.set_position(pos)
            self.assertTrue(self.black_checker.can_bear_off())

        for pos in range(1, 19):
            self.black_checker.set_position(pos)
            self.assertFalse(self.black_checker.can_bear_off())

    def test_get_home_board_positions(self):
        white_home = Checker.get_home_board_positions("white")
        self.assertEqual(white_home, list(range(1, 7)))

        black_home = Checker.get_home_board_positions("black")
        self.assertEqual(black_home, list(range(19, 25)))

    def test_is_in_home_board(self):
        self.white_checker.set_position(3)
        self.assertTrue(self.white_checker.is_in_home_board())
        self.white_checker.set_position(10)
        self.assertFalse(self.white_checker.is_in_home_board())
        self.black_checker.set_position(22)
        self.assertTrue(self.black_checker.is_in_home_board())
        self.black_checker.set_position(10)
        self.assertFalse(self.black_checker.is_in_home_board())

    def test_opposite_color(self):
        self.assertEqual(Checker.get_opposite_color("white"), "black")
        self.assertEqual(Checker.get_opposite_color("black"), "white")

        with self.assertRaises(ValueError):
            Checker.get_opposite_color("red")

    def test_validate_position_type(self):
        self.white_checker.set_position(1)
        self.white_checker.set_position("bar")
        self.white_checker.set_position("off")

        with self.assertRaises(TypeError):
            self.white_checker.set_position(1.5)

        with self.assertRaises(TypeError):
            self.white_checker.set_position([1])

    def test_set_position_invalid_string(self):
        """Test setting invalid string position"""
        with self.assertRaises(ValueError):
            self.white_checker.set_position("invalid")

        with self.assertRaises(ValueError):
            self.white_checker.set_position("middle")

    def test_static_methods_comprehensive(self):
        """Test static methods with comprehensive scenarios"""
        # Test get_home_board_positions with both colors
        white_positions = Checker.get_home_board_positions("white")
        black_positions = Checker.get_home_board_positions("black")

        self.assertEqual(white_positions, [1, 2, 3, 4, 5, 6])
        self.assertEqual(black_positions, [19, 20, 21, 22, 23, 24])

        # Test get_opposite_color
        self.assertEqual(Checker.get_opposite_color("white"), "black")
        self.assertEqual(Checker.get_opposite_color("black"), "white")

        # Test invalid color for get_opposite_color
        with self.assertRaises(ValueError):
            Checker.get_opposite_color("invalid")

    def test_checker_state_transitions(self):
        """Test checker state transitions"""
        # Test initial state
        self.assertIsNone(self.white_checker.position)
        self.assertFalse(self.white_checker.is_on_board())
        self.assertFalse(self.white_checker.is_on_bar())
        self.assertFalse(self.white_checker.is_off_board())

        # Test move to board
        self.white_checker.set_position(10)
        self.assertTrue(self.white_checker.is_on_board())
        self.assertFalse(self.white_checker.is_on_bar())
        self.assertFalse(self.white_checker.is_off_board())

        # Test move to bar
        self.white_checker.move_to_bar()
        self.assertFalse(self.white_checker.is_on_board())
        self.assertTrue(self.white_checker.is_on_bar())
        self.assertFalse(self.white_checker.is_off_board())

        # Test move off board
        self.white_checker.move_off_board()
        self.assertFalse(self.white_checker.is_on_board())
        self.assertFalse(self.white_checker.is_on_bar())
        self.assertTrue(self.white_checker.is_off_board())

    def test_home_board_validation_comprehensive(self):
        """Test comprehensive home board validation"""
        # Test all white home board positions
        for pos in range(1, 7):
            self.white_checker.set_position(pos)
            self.assertTrue(self.white_checker.is_in_home_board())
            self.assertTrue(self.white_checker.can_bear_off())

        # Test all black home board positions
        for pos in range(19, 25):
            self.black_checker.set_position(pos)
            self.assertTrue(self.black_checker.is_in_home_board())
            self.assertTrue(self.black_checker.can_bear_off())

        # Test positions outside home board
        for pos in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]:
            self.white_checker.set_position(pos)
            self.assertFalse(self.white_checker.is_in_home_board())
            self.assertFalse(self.white_checker.can_bear_off())

            self.black_checker.set_position(pos)
            self.assertFalse(self.black_checker.is_in_home_board())
            self.assertFalse(self.black_checker.can_bear_off())

    def test_type_validation_comprehensive(self):
        """Test type validation for various inputs"""
        # Test valid types
        valid_positions = [1, 24, "bar", "off"]
        for pos in valid_positions:
            self.white_checker.set_position(pos)
            self.assertEqual(self.white_checker.position, pos)

        # Test invalid types
        invalid_positions = [1.5, [1], {"pos": 1}, None]
        for pos in invalid_positions:
            with self.assertRaises(TypeError):
                self.white_checker.set_position(pos)


if __name__ == "__main__":
    unittest.main()
