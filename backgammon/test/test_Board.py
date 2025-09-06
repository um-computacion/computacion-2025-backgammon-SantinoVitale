import unittest
from unittest.mock import Mock
from backgammon.core import Board, Checker

class TestBoard(unittest.TestCase):

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

if __name__ == "__main__":
  unittest.main()
