"""
Unit tests for CommandParser class.
Tests command parsing functionality following SOLID principles.
"""

import unittest
from backgammon.cli.command_parser import CommandParser


class TestCommandParser(unittest.TestCase):
    """Test cases for CommandParser class."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = CommandParser()

    def test_init(self):
        """Test CommandParser initialization."""
        parser = CommandParser()
        self.assertIsInstance(parser, CommandParser)

    def test_parse_move_input_valid_numeric(self):
        """Test parsing valid numeric move input."""
        from_pos, to_pos = self.parser.parse_move_input("12 8")
        self.assertEqual(from_pos, 12)
        self.assertEqual(to_pos, 8)

    def test_parse_move_input_with_barra(self):
        """Test parsing move input with 'barra'."""
        from_pos, to_pos = self.parser.parse_move_input("barra 20")
        self.assertEqual(from_pos, "bar")
        self.assertEqual(to_pos, 20)

    def test_parse_move_input_with_fuera(self):
        """Test parsing move input with 'fuera'."""
        from_pos, to_pos = self.parser.parse_move_input("6 fuera")
        self.assertEqual(from_pos, 6)
        self.assertEqual(to_pos, "off")

    def test_parse_move_input_special_command_ayuda(self):
        """Test parsing special command 'ayuda'."""
        from_pos, to_pos = self.parser.parse_move_input("ayuda")
        self.assertEqual(from_pos, "ayuda")
        self.assertIsNone(to_pos)

    def test_parse_move_input_special_command_help(self):
        """Test parsing special command 'help'."""
        from_pos, to_pos = self.parser.parse_move_input("help")
        self.assertEqual(from_pos, "help")
        self.assertIsNone(to_pos)

    def test_parse_move_input_special_command_salir(self):
        """Test parsing special command 'salir'."""
        from_pos, to_pos = self.parser.parse_move_input("salir")
        self.assertEqual(from_pos, "salir")
        self.assertIsNone(to_pos)

    def test_parse_move_input_special_command_movimientos(self):
        """Test parsing special command 'movimientos'."""
        from_pos, to_pos = self.parser.parse_move_input("movimientos")
        self.assertEqual(from_pos, "movimientos")
        self.assertIsNone(to_pos)

    def test_parse_move_input_invalid_format_one_part(self):
        """Test parsing invalid move input with only one part."""
        with self.assertRaises(ValueError) as context:
            self.parser.parse_move_input("12")
        self.assertIn("Formato inválido", str(context.exception))

    def test_parse_move_input_invalid_format_three_parts(self):
        """Test parsing invalid move input with three parts."""
        with self.assertRaises(ValueError) as context:
            self.parser.parse_move_input("12 8 5")
        self.assertIn("Formato inválido", str(context.exception))

    def test_parse_move_input_with_whitespace(self):
        """Test parsing move input with extra whitespace."""
        from_pos, to_pos = self.parser.parse_move_input("  12   8  ")
        self.assertEqual(from_pos, 12)
        self.assertEqual(to_pos, 8)

    def test_is_special_command_true(self):
        """Test is_special_command with special commands."""
        self.assertTrue(self.parser.is_special_command("ayuda"))
        self.assertTrue(self.parser.is_special_command("help"))
        self.assertTrue(self.parser.is_special_command("salir"))
        self.assertTrue(self.parser.is_special_command("quit"))

    def test_is_special_command_false(self):
        """Test is_special_command with non-special commands."""
        self.assertFalse(self.parser.is_special_command("12"))
        self.assertFalse(self.parser.is_special_command("move"))
        self.assertFalse(self.parser.is_special_command("invalid"))

    def test_get_command_type_help(self):
        """Test get_command_type for help commands."""
        self.assertEqual(self.parser.get_command_type("help"), "help")
        self.assertEqual(self.parser.get_command_type("ayuda"), "help")

    def test_get_command_type_rules(self):
        """Test get_command_type for rules commands."""
        self.assertEqual(self.parser.get_command_type("rules"), "rules")
        self.assertEqual(self.parser.get_command_type("reglas"), "rules")

    def test_get_command_type_quit(self):
        """Test get_command_type for quit commands."""
        self.assertEqual(self.parser.get_command_type("quit"), "quit")
        self.assertEqual(self.parser.get_command_type("salir"), "quit")

    def test_get_command_type_moves(self):
        """Test get_command_type for moves commands."""
        self.assertEqual(self.parser.get_command_type("moves"), "moves")
        self.assertEqual(self.parser.get_command_type("movimientos"), "moves")

    def test_get_command_type_unknown(self):
        """Test get_command_type for unknown commands."""
        self.assertEqual(self.parser.get_command_type("invalid"), "unknown")

    def test_get_command_type_case_insensitive(self):
        """Test get_command_type is case insensitive."""
        self.assertEqual(self.parser.get_command_type("HELP"), "help")
        self.assertEqual(self.parser.get_command_type("Help"), "help")


if __name__ == "__main__":
    unittest.main()
