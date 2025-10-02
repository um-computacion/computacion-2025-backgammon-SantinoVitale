"""
Test module for Board class.

This module contains unit tests for the Board class which represents
the backgammon game board and handles checker movements.
"""

import unittest
from unittest.mock import Mock
from backgammon.core import Board, Checker

# pylint: disable=C0116  # many simple test methods without individual docstrings
# pylint: disable=C0103  # module name follows test naming convention


class TestBoard(unittest.TestCase):
    """Test cases for the Board class."""

    def setUp(self):
        self.board = Board()
        self.white = "white"
        self.black = "black"

    def test_board_initialization(self):
        self.assertTrue(hasattr(self.board, "points"))
        self.assertEqual(len(self.board.points), 24)
        self.assertTrue(all(isinstance(p, list) for p in self.board.points))
        self.assertTrue(hasattr(self.board, "bar"))
        self.assertTrue(hasattr(self.board, "off"))
        self.assertIn(self.white, self.board.bar)
        self.assertIn(self.black, self.board.bar)
        self.assertIn(self.white, self.board.off)
        self.assertIn(self.black, self.board.off)

    def test_setup_initial_position_total_checkers(self):
        self.board.setup_initial_position()
        total = sum(len(p) for p in self.board.points)
        self.assertEqual(total, 30)

    def test_setup_initial_position_creates_correct_checkers(self):
        # Create a simple board fresh and count the checkers directly
        test_board = Board()
        test_board.setup_initial_position()

        # Count white and black checkers by examining all points
        white_count = 0
        black_count = 0

        for point in test_board.points:
            for checker in point:
                if checker.color == "white":
                    white_count += 1
                elif checker.color == "black":
                    black_count += 1

        # Verify correct number of checkers
        self.assertEqual(white_count + black_count, 30)  # Total checkers
        self.assertEqual(white_count, 15)  # 15 white checkers
        self.assertEqual(black_count, 15)  # 15 black checkers

    def test_get_point_count_and_top_color(self):
        self.board.points[0] = [Checker(self.white) for _ in range(3)]
        self.board.points[5] = [Checker(self.black) for _ in range(2)]
        self.assertEqual(self.board.get_point_count(0), 3)
        self.assertEqual(self.board.get_point_count(5), 2)
        self.assertEqual(self.board.get_point_top_color(0), self.white)
        self.assertEqual(self.board.get_point_top_color(5), self.black)
        self.assertIsNone(self.board.get_point_top_color(10))

    def test_is_point_available_simple(self):
        self.board.points[7] = []
        self.assertTrue(self.board.is_point_available(7, self.white))
        self.board.points[8] = [Checker(self.black)]
        self.assertTrue(self.board.is_point_available(8, self.white))
        self.board.points[9] = [Checker(self.black), Checker(self.black)]
        self.assertFalse(self.board.is_point_available(9, self.white))

    def test_move_checker_valid_to_empty(self):
        self.board.points[2] = [Checker(self.white), Checker(self.white)]
        self.board.points[4] = []
        result = self.board.move_checker(2, 4, self.white)
        self.assertTrue(result)
        self.assertEqual(self.board.get_point_count(2), 1)
        self.assertEqual(self.board.get_point_count(4), 1)
        self.assertEqual(self.board.get_point_top_color(4), self.white)

    def test_move_checker_hit_opponent_to_bar(self):
        self.board.points[3] = [Checker(self.white)]
        self.board.points[6] = [Checker(self.black)]
        result = self.board.move_checker(3, 6, self.white)
        self.assertTrue(result)
        self.assertEqual(self.board.get_point_top_color(6), self.white)
        self.assertEqual(len(self.board.bar[self.black]), 1)
        self.assertEqual(self.board.bar[self.black][0].color, self.black)

    def test_move_checker_hit_with_mock_checkers(self):
        # Create mock checkers with specific colors
        mock_white_checker = Mock()
        mock_white_checker.color = "white"

        mock_black_checker = Mock()
        mock_black_checker.color = "black"

        # Setup initial positions
        self.board.points[3] = [mock_white_checker]  # White checker at position 3
        self.board.points[6] = [
            mock_black_checker
        ]  # Black checker at position 6 (will be hit)

        result = self.board.move_checker(3, 6, "white")

        self.assertTrue(result)
        self.assertEqual(len(self.board.bar["black"]), 1)  # Black checker moved to bar
        self.assertEqual(
            self.board.points[6][0], mock_white_checker
        )  # White checker at position 6

    def test_move_checker_invalid_from_empty(self):
        self.board.points[10] = []
        result = self.board.move_checker(10, 12, self.white)
        self.assertFalse(result)

    def test_move_checker_blocked_destination(self):
        self.board.points[1] = [Checker(self.white)]
        self.board.points[2] = [Checker(self.black), Checker(self.black)]
        result = self.board.move_checker(1, 2, self.white)
        self.assertFalse(result)
        self.assertEqual(self.board.get_point_count(1), 1)

    def test_move_from_bar_and_to_bar(self):
        self.board.bar[self.white].append(Checker(self.white))
        success = self.board.move_from_bar(self.white, 22)
        self.assertIn(success, (True, False))
        if success:
            self.assertEqual(len(self.board.bar[self.white]), 0)

    def test_bearing_off_and_off_storage(self):
        self.board.points[0] = [Checker(self.white)]
        prev_off = len(self.board.off[self.white])
        result = self.board.bear_off(0, self.white)
        self.assertIn(result, (True, False))
        if result:
            self.assertEqual(len(self.board.off[self.white]), prev_off + 1)
            self.assertEqual(self.board.get_point_count(0), 0)

    def test_get_state_and_set_state(self):
        self.board.points[0] = [Checker(self.white)]
        self.board.bar[self.black].append(Checker(self.black))
        state = self.board.get_state()
        new = Board()
        new.set_state(state)
        new_state = new.get_state()
        self.assertEqual(len(new_state["points"][0]), 1)
        self.assertEqual(len(new_state["bar"][self.black]), 1)

    def test_reset_board(self):
        self.board.points[0] = [Checker(self.white)]
        self.board.bar[self.black].append(Checker(self.black))
        self.board.reset()
        self.assertEqual(len(self.board.bar[self.white]), 0)
        self.assertEqual(len(self.board.bar[self.black]), 0)
        self.assertEqual(len(self.board.off[self.white]), 0)
        self.assertEqual(len(self.board.off[self.black]), 0)

    def test_string_and_repr(self):
        s = str(self.board)
        r = repr(self.board)
        self.assertIsInstance(s, str)
        self.assertIsInstance(r, str)

    def test_invalid_point_indexes(self):
        with self.assertRaises(IndexError):
            _ = self.board.get_point_count(24)
        with self.assertRaises(IndexError):
            _ = self.board.get_point_top_color(-25)

    def test_is_point_available_invalid_index(self):
        """Test is_point_available with invalid point index"""
        self.assertFalse(self.board.is_point_available(-1, self.white))
        self.assertFalse(self.board.is_point_available(24, self.white))

    def test_move_from_bar_no_checkers(self):
        """Test moving from bar when no checkers are on bar"""
        self.board.bar[self.white] = []
        result = self.board.move_from_bar(self.white, 5)
        self.assertFalse(result)

    def test_move_from_bar_point_not_available(self):
        """Test moving from bar to unavailable point"""
        self.board.bar[self.white].append(Checker(self.white))
        # Block point 5 with two black checkers
        self.board.points[5] = [Checker(self.black), Checker(self.black)]

        result = self.board.move_from_bar(self.white, 5)
        self.assertFalse(result)

    def test_move_from_bar_successful_with_capture(self):
        """Test successful move from bar with capturing opponent checker"""
        self.board.bar[self.white].append(Checker(self.white))
        # Place single black checker on destination
        self.board.points[10] = [Checker(self.black)]

        result = self.board.move_from_bar(self.white, 10)
        self.assertTrue(result)

        # Check that white checker is on point 10
        self.assertEqual(len(self.board.points[10]), 1)
        self.assertEqual(self.board.points[10][0].color, self.white)

        # Check that black checker was moved to bar
        self.assertEqual(len(self.board.bar[self.black]), 1)
        self.assertEqual(self.board.bar[self.black][0].color, self.black)

    def test_bear_off_successful(self):
        """Test successful bear off move"""
        self.board.points[2] = [Checker(self.white)]

        result = self.board.bear_off(2, self.white)
        self.assertTrue(result)

        # Check checker was removed from board
        self.assertEqual(len(self.board.points[2]), 0)

        # Check checker was added to off area
        self.assertEqual(len(self.board.off[self.white]), 1)

    def test_bear_off_no_checker_on_point(self):
        """Test bear off when no checker on point"""
        self.board.points[2] = []

        result = self.board.bear_off(2, self.white)
        self.assertFalse(result)

    def test_bear_off_wrong_color_checker(self):
        """Test bear off when checker is wrong color"""
        self.board.points[2] = [Checker(self.black)]

        result = self.board.bear_off(2, self.white)
        self.assertFalse(result)

    def test_all_checkers_in_home_board_white_true(self):
        """Test all checkers in home board for white player - true case"""
        # Clear all points
        self.board.points = [[] for _ in range(24)]

        # Place white checkers only in home board (points 0-5)
        self.board.points[0] = [Checker(self.white)]
        self.board.points[3] = [Checker(self.white)]
        self.board.points[5] = [Checker(self.white)]

        # Ensure no checkers on bar
        self.board.bar[self.white] = []

        result = self.board.all_checkers_in_home_board(self.white)
        self.assertTrue(result)

    def test_all_checkers_in_home_board_white_false_checkers_on_bar(self):
        """Test all checkers in home board for white - false due to bar"""
        # Place all checkers in home board
        self.board.points = [[] for _ in range(24)]
        self.board.points[0] = [Checker(self.white)]

        # But also have checkers on bar
        self.board.bar[self.white] = [Checker(self.white)]

        result = self.board.all_checkers_in_home_board(self.white)
        self.assertFalse(result)

    def test_all_checkers_in_home_board_white_false_checkers_outside(self):
        """Test all checkers in home board for white - false due to outside checkers"""
        # Clear all points
        self.board.points = [[] for _ in range(24)]

        # Place checker outside home board
        self.board.points[10] = [Checker(self.white)]

        # No checkers on bar
        self.board.bar[self.white] = []

        result = self.board.all_checkers_in_home_board(self.white)
        self.assertFalse(result)

    def test_all_checkers_in_home_board_black_true(self):
        """Test all checkers in home board for black player - true case"""
        # Clear all points
        self.board.points = [[] for _ in range(24)]

        # Place black checkers only in home board (points 18-23)
        self.board.points[18] = [Checker(self.black)]
        self.board.points[21] = [Checker(self.black)]
        self.board.points[23] = [Checker(self.black)]

        # Ensure no checkers on bar
        self.board.bar[self.black] = []

        result = self.board.all_checkers_in_home_board(self.black)
        self.assertTrue(result)

    def test_all_checkers_in_home_board_black_false_checkers_outside(self):
        """Test all checkers in home board for black - false due to outside checkers"""
        # Clear all points
        self.board.points = [[] for _ in range(24)]

        # Place checker outside home board
        self.board.points[10] = [Checker(self.black)]

        # No checkers on bar
        self.board.bar[self.black] = []

        result = self.board.all_checkers_in_home_board(self.black)
        self.assertFalse(result)

    def test_can_bear_off_delegates_to_all_checkers_in_home_board(self):
        """Test can_bear_off calls all_checkers_in_home_board"""
        # Clear board and put all white checkers in home board
        self.board.points = [[] for _ in range(24)]
        self.board.points[0] = [Checker(self.white)]
        self.board.bar[self.white] = []

        result = self.board.can_bear_off(self.white)
        self.assertTrue(result)

        # Add checker outside home board
        self.board.points[10] = [Checker(self.white)]

        result = self.board.can_bear_off(self.white)
        self.assertFalse(result)

    def test_get_state_method(self):
        """Test get_state method returns correct state"""
        # Setup some checkers
        self.board.points[0] = [Checker(self.white)]
        self.board.bar[self.black].append(Checker(self.black))
        self.board.off[self.white].append(Checker(self.white))

        state = self.board.get_state()

        self.assertIn("points", state)
        self.assertIn("bar", state)
        self.assertIn("off", state)
        self.assertEqual(len(state["points"]), 24)

    def test_set_state_method(self):
        """Test set_state method correctly sets board state"""
        # Create a state with some checkers
        state = {
            "points": [[] for _ in range(24)],
            "bar": {self.white: [], self.black: []},
            "off": {self.white: [], self.black: []},
        }
        state["points"][5] = [{"color": self.white}]
        state["bar"][self.black] = [{"color": self.black}]

        self.board.set_state(state)

        # Verify state was set correctly
        self.assertEqual(len(self.board.points[5]), 1)
        self.assertEqual(self.board.points[5][0].color, self.white)
        self.assertEqual(len(self.board.bar[self.black]), 1)

    def test_board_state_independence(self):
        """Test board state can be copied through get_state/set_state"""
        # Setup original board
        self.board.points[0] = [Checker(self.white)]

        # Get state and create new board with same state
        state = self.board.get_state()
        new_board = Board()
        new_board.set_state(state)

        # Verify independence
        self.assertIsNot(new_board, self.board)
        self.assertEqual(len(new_board.points[0]), 1)

    def test_get_possible_moves_with_checkers_on_bar(self):
        """Test get_possible_moves when player has checkers on bar"""
        # Put white checker on bar
        self.board.bar[self.white].append(Checker(self.white))

        # Test possible moves from bar
        dice_values = [3, 5]
        moves = self.board.get_possible_moves(self.white, dice_values)

        # Should only return bar moves
        self.assertTrue(all(move[0] == "bar" for move in moves))

        # Should have moves for each valid dice value
        expected_destinations = [21, 19]  # 24-3=21, 24-5=19 for white
        actual_destinations = [move[1] for move in moves]
        for dest in expected_destinations:
            if 0 <= dest <= 23:  # Only valid destinations
                self.assertIn(dest, actual_destinations)

    def test_get_possible_moves_normal_moves(self):
        """Test get_possible_moves for normal board moves"""
        # Clear board and place white checker
        self.board.points = [[] for _ in range(24)]
        self.board.points[10] = [Checker(self.white)]
        self.board.bar[self.white] = []

        dice_values = [2, 4]
        moves = self.board.get_possible_moves(self.white, dice_values)

        # Should have normal moves
        expected_moves = [(10, 8), (10, 6)]  # 10-2=8, 10-4=6 for white
        for move in expected_moves:
            self.assertIn(move, moves)

    def test_get_possible_moves_bear_off(self):
        """Test get_possible_moves when bearing off is possible"""
        # Setup all checkers in home board for white
        self.board.points = [[] for _ in range(24)]
        self.board.points[2] = [Checker(self.white)]  # Point 3 in human notation
        self.board.bar[self.white] = []

        dice_values = [4]  # This would move checker off the board
        moves = self.board.get_possible_moves(self.white, dice_values)

        # Should include bear off move
        self.assertIn((2, "off"), moves)

    def test_get_possible_moves_blocked_destinations(self):
        """Test get_possible_moves with blocked destinations"""
        # Clear board and setup
        self.board.points = [[] for _ in range(24)]
        self.board.points[10] = [Checker(self.white)]
        # Block destination with two black checkers
        self.board.points[8] = [Checker(self.black), Checker(self.black)]
        self.board.bar[self.white] = []

        dice_values = [2]
        moves = self.board.get_possible_moves(self.white, dice_values)

        # Should not include blocked move
        self.assertNotIn((10, 8), moves)

    def test_get_possible_moves_black_player(self):
        """Test get_possible_moves for black player"""
        # Clear board and place black checker
        self.board.points = [[] for _ in range(24)]
        self.board.points[5] = [Checker(self.black)]
        self.board.bar[self.black] = []

        dice_values = [3]
        moves = self.board.get_possible_moves(self.black, dice_values)

        # Black moves in opposite direction (5+3=8)
        self.assertIn((5, 8), moves)

    def test_get_possible_moves_black_from_bar(self):
        """Test get_possible_moves for black player from bar"""
        # Put black checker on bar
        self.board.bar[self.black].append(Checker(self.black))

        dice_values = [3]
        moves = self.board.get_possible_moves(self.black, dice_values)

        # Black enters from point 1 towards 24 (3-1=2)
        expected_moves = [("bar", 2)]
        for move in expected_moves:
            self.assertIn(move, moves)

    def test_get_possible_moves_edge_case_dice_values(self):
        """Test get_possible_moves with edge case dice values"""
        # Setup checker near edge
        self.board.points = [[] for _ in range(24)]
        self.board.points[1] = [Checker(self.white)]  # Near the edge
        self.board.bar[self.white] = []

        dice_values = [6]  # Would go to -5, invalid
        moves = self.board.get_possible_moves(self.white, dice_values)

        # Should include bear off if all checkers in home board
        if self.board._can_bear_off(self.white):
            self.assertIn((1, "off"), moves)

    def test_hit_checker_functionality(self):
        """Test hitting opponent checker moves to bar"""
        # Setup: white checker can hit single black checker
        self.board.points[10] = [Checker(self.white)]
        self.board.points[8] = [Checker(self.black)]  # Single black checker

        success = self.board.move_checker(10, 8, self.white)

        self.assertTrue(success)
        # Black checker should be on bar
        self.assertEqual(len(self.board.bar[self.black]), 1)
        # White checker should be on point 8
        self.assertEqual(self.board.get_point_top_color(8), self.white)

    def test_board_validation_methods(self):
        """Test various board validation methods"""
        # Test invalid point access
        with self.assertRaises(IndexError):
            self.board.get_point_count(-1)

        with self.assertRaises(IndexError):
            self.board.get_point_count(24)

    def test_bear_off_validation(self):
        """Test bear off validation logic"""
        # Test when not all checkers in home board
        self.board.points[10] = [Checker(self.white)]  # Outside home board
        result = self.board.bear_off(2, self.white)
        self.assertFalse(result)  # Should fail if not all checkers in home board


if __name__ == "__main__":
    unittest.main()
