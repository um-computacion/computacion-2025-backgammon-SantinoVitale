"""
Unit tests for InputValidator class.
Tests input validation functionality following SOLID principles.
"""

import unittest
from backgammon.cli.InputValidator import InputValidator


class TestInputValidator(unittest.TestCase):
    """Test cases for InputValidator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = InputValidator()

    def test_init(self):
        """Test InputValidator initialization."""
        validator = InputValidator()
        self.assertIsInstance(validator, InputValidator)

    def test_validate_position_valid_numeric(self):
        """Test validating valid numeric positions."""
        self.assertTrue(self.validator.validate_position(1))
        self.assertTrue(self.validator.validate_position(12))
        self.assertTrue(self.validator.validate_position(24))

    def test_validate_position_invalid_numeric(self):
        """Test validating invalid numeric positions."""
        self.assertFalse(self.validator.validate_position(0))
        self.assertFalse(self.validator.validate_position(25))
        self.assertFalse(self.validator.validate_position(-1))
        self.assertFalse(self.validator.validate_position(100))

    def test_validate_position_valid_string(self):
        """Test validating valid string positions."""
        self.assertTrue(self.validator.validate_position("bar"))
        self.assertTrue(self.validator.validate_position("off"))
        self.assertTrue(self.validator.validate_position("barra"))
        self.assertTrue(self.validator.validate_position("fuera"))

    def test_validate_position_valid_string_case_insensitive(self):
        """Test validating string positions is case insensitive."""
        self.assertTrue(self.validator.validate_position("BAR"))
        self.assertTrue(self.validator.validate_position("OFF"))
        self.assertTrue(self.validator.validate_position("Barra"))
        self.assertTrue(self.validator.validate_position("FUERA"))

    def test_validate_position_invalid_string(self):
        """Test validating invalid string positions."""
        self.assertFalse(self.validator.validate_position("invalid"))
        self.assertFalse(self.validator.validate_position("home"))
        self.assertFalse(self.validator.validate_position(""))

    def test_validate_position_invalid_type(self):
        """Test validating positions with invalid types."""
        self.assertFalse(self.validator.validate_position(None))
        self.assertFalse(self.validator.validate_position([]))
        self.assertFalse(self.validator.validate_position({}))

    def test_validate_numeric_position_valid(self):
        """Test validating valid numeric position strings."""
        self.assertTrue(self.validator.validate_numeric_position("1"))
        self.assertTrue(self.validator.validate_numeric_position("12"))
        self.assertTrue(self.validator.validate_numeric_position("24"))

    def test_validate_numeric_position_invalid_range(self):
        """Test validating numeric positions out of range."""
        self.assertFalse(self.validator.validate_numeric_position("0"))
        self.assertFalse(self.validator.validate_numeric_position("25"))
        self.assertFalse(self.validator.validate_numeric_position("-1"))

    def test_validate_numeric_position_non_numeric(self):
        """Test validating non-numeric strings."""
        self.assertFalse(self.validator.validate_numeric_position("bar"))
        self.assertFalse(self.validator.validate_numeric_position("abc"))
        self.assertFalse(self.validator.validate_numeric_position(""))

    def test_validate_confirmation_affirmative_spanish(self):
        """Test validating affirmative responses in Spanish."""
        self.assertTrue(self.validator.validate_confirmation("s"))
        self.assertTrue(self.validator.validate_confirmation("sí"))
        self.assertTrue(self.validator.validate_confirmation("si"))

    def test_validate_confirmation_affirmative_english(self):
        """Test validating affirmative responses in English."""
        self.assertTrue(self.validator.validate_confirmation("y"))
        self.assertTrue(self.validator.validate_confirmation("yes"))

    def test_validate_confirmation_case_insensitive(self):
        """Test validating confirmation is case insensitive."""
        self.assertTrue(self.validator.validate_confirmation("S"))
        self.assertTrue(self.validator.validate_confirmation("YES"))
        self.assertTrue(self.validator.validate_confirmation("Si"))

    def test_validate_confirmation_with_whitespace(self):
        """Test validating confirmation with whitespace."""
        self.assertTrue(self.validator.validate_confirmation("  s  "))
        self.assertTrue(self.validator.validate_confirmation("  yes  "))

    def test_validate_confirmation_negative(self):
        """Test validating negative responses."""
        self.assertFalse(self.validator.validate_confirmation("n"))
        self.assertFalse(self.validator.validate_confirmation("no"))
        self.assertFalse(self.validator.validate_confirmation("nope"))
        self.assertFalse(self.validator.validate_confirmation(""))

    def test_validate_move_format_valid(self):
        """Test validating valid move formats."""
        self.assertTrue(self.validator.validate_move_format("12 8"))
        self.assertTrue(self.validator.validate_move_format("1 6"))
        self.assertTrue(self.validator.validate_move_format("barra 20"))
        self.assertTrue(self.validator.validate_move_format("5 fuera"))

    def test_validate_move_format_invalid_one_part(self):
        """Test validating move format with one part."""
        self.assertFalse(self.validator.validate_move_format("12"))
        self.assertFalse(self.validator.validate_move_format("bar"))

    def test_validate_move_format_invalid_three_parts(self):
        """Test validating move format with three parts."""
        self.assertFalse(self.validator.validate_move_format("12 8 5"))

    def test_validate_move_format_with_extra_whitespace(self):
        """Test validating move format with extra whitespace."""
        self.assertTrue(self.validator.validate_move_format("  12   8  "))

    def test_validate_move_format_empty(self):
        """Test validating empty move format."""
        self.assertFalse(self.validator.validate_move_format(""))
        self.assertFalse(self.validator.validate_move_format("   "))


if __name__ == "__main__":
    unittest.main()
