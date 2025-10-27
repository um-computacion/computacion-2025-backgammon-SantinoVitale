"""
Unit tests for BoardRenderer class.
Tests board visualization functionality following SOLID principles.
"""

import unittest
from unittest.mock import Mock
from backgammon.cli.BoardRenderer import BoardRenderer


class TestBoardRenderer(unittest.TestCase):
    """Test cases for BoardRenderer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.renderer = BoardRenderer()
        self.mock_board = Mock()
        self.mock_board.bar = {"white": [], "black": []}
        self.mock_board.off = {"white": [], "black": []}
        self.mock_board.points = [[] for _ in range(24)]

    def test_init(self):
        """Test BoardRenderer initialization."""
        renderer = BoardRenderer()
        self.assertIsInstance(renderer, BoardRenderer)

    def test_render_board_with_empty_board(self):
        """Test rendering an empty board."""
        result = self.renderer.render_board(self.mock_board)
        self.assertIsInstance(result, str)
        self.assertIn("TABLERO DE BACKGAMMON", result)
        self.assertIn("BLANCAS", result)
        self.assertIn("NEGRAS", result)

    def test_render_board_with_none_board(self):
        """Test rendering with None board."""
        result = self.renderer.render_board(None)
        self.assertEqual(result, "No hay tablero disponible para mostrar")

    def test_render_board_with_checkers(self):
        """Test rendering board with checkers."""
        mock_checker_white = Mock()
        mock_checker_white.color = "white"
        mock_checker_black = Mock()
        mock_checker_black.color = "black"

        self.mock_board.points[0] = [mock_checker_white, mock_checker_white]
        self.mock_board.points[23] = [mock_checker_black, mock_checker_black]

        result = self.renderer.render_board(self.mock_board)
        self.assertIsInstance(result, str)
        self.assertIn("TABLERO DE BACKGAMMON", result)

    def test_render_board_with_bar_checkers(self):
        """Test rendering board with checkers in bar."""
        mock_checker = Mock()
        self.mock_board.bar = {
            "white": [mock_checker],
            "black": [mock_checker, mock_checker],
        }

        result = self.renderer.render_board(self.mock_board)
        self.assertIn("W:1", result)
        self.assertIn("B:2", result)

    def test_render_board_with_off_checkers(self):
        """Test rendering board with checkers off."""
        mock_checker = Mock()
        self.mock_board.off = {"white": [mock_checker] * 3, "black": [mock_checker] * 5}

        result = self.renderer.render_board(self.mock_board)
        self.assertIn("W: 3", result)
        self.assertIn("B: 5", result)

    def test_render_legend_with_empty_board(self):
        """Test rendering legend with empty board."""
        result = self.renderer.render_legend(self.mock_board)
        self.assertIsInstance(result, str)
        self.assertIn("Blancas", result)
        self.assertIn("Negras", result)
        self.assertIn("BARRA", result)
        self.assertIn("FUERA", result)

    def test_render_legend_with_none_board(self):
        """Test rendering legend with None board."""
        result = self.renderer.render_legend(None)
        self.assertEqual(result, "")

    def test_render_legend_with_current_player(self):
        """Test rendering legend with current player."""
        mock_player = Mock()
        mock_player.name = "TestPlayer"
        mock_player.color = "white"

        result = self.renderer.render_legend(self.mock_board, mock_player)
        self.assertIn("TestPlayer", result)
        self.assertIn("TURNO", result)

    def test_render_legend_with_player_no_attributes(self):
        """Test rendering legend with player missing attributes."""
        mock_player = Mock(spec=[])

        result = self.renderer.render_legend(self.mock_board, mock_player)
        self.assertIsInstance(result, str)

    def test_render_possible_moves_empty(self):
        """Test rendering empty possible moves."""
        result = self.renderer.render_possible_moves([], str)
        self.assertEqual(result, "\nNo hay movimientos válidos disponibles")

    def test_render_possible_moves_with_moves(self):
        """Test rendering possible moves with valid moves."""
        moves = [(1, 5), (12, 8), (24, 20)]

        result = self.renderer.render_possible_moves(moves, str)
        self.assertIsInstance(result, str)
        self.assertIn("MOVIMIENTOS POSIBLES", result)
        self.assertIn("Total: 3", result)

    def test_render_possible_moves_grouping(self):
        """Test that possible moves are grouped by from position."""
        moves = [(1, 5), (1, 6), (12, 8)]

        result = self.renderer.render_possible_moves(moves, str)
        self.assertIn("1", result)
        self.assertIn("5", result)
        self.assertIn("6", result)
        self.assertIn("12", result)

    def test_render_possible_moves_with_special_positions(self):
        """Test rendering moves with special positions."""
        moves = [("bar", 20), (5, "off")]

        def format_func(x):
            if x == "bar":
                return "BARRA"
            if x == "off":
                return "FUERA"
            return str(x)

        result = self.renderer.render_possible_moves(moves, format_func)
        self.assertIn("BARRA", result)
        self.assertIn("FUERA", result)

    def test_render_board_without_hasattr(self):
        """Test rendering board without required attributes."""
        mock_board_minimal = Mock(spec=[])

        result = self.renderer.render_board(mock_board_minimal)
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
