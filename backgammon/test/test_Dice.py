import unittest
from unittest.mock import patch
from backgammon.core import Dice


class TestDice(unittest.TestCase):

  def setUp(self):
    self.dice = Dice()
  
  def test_dice_initialization(self):
    self.assertIsNotNone(self.dice)
    self.assertIsNone(self.dice.last_roll)
    self.assertEqual(self.dice.values, [])

  def test_roll_single_die(self):
    value = self.dice.roll_single()
    self.assertIn(value, [1, 2, 3, 4, 5, 6])
    self.assertIsInstance(value, int)

  def test_roll_both_dice(self):
    values = self.dice.roll()
    self.assertEqual(len(values), 2)
    self.assertTrue(all(1 <= v <= 6 for v in values))
    self.assertTrue(all(isinstance(v, int) for v in values))
    self.assertEqual(self.dice.last_roll, values)

  def test_is_double_true(self):
    self.dice.last_roll = [3, 3]
    self.assertTrue(self.dice.is_double())

  def test_is_double_false(self):
    self.dice.last_roll = [2, 5]
    self.assertFalse(self.dice.is_double())

  def test_is_double_no_roll(self):
    self.dice.last_roll = None
    self.assertFalse(self.dice.is_double())

  def test_get_moves_normal_roll(self):
    moves = self.dice.get_moves([3, 5])
    self.assertEqual(sorted(moves), [3, 5])
    self.assertEqual(len(moves), 2)

  def test_get_moves_double_roll(self):
    moves = self.dice.get_moves([4, 4])
    self.assertEqual(moves, [4, 4, 4, 4])
    self.assertEqual(len(moves), 4)

  def test_get_moves_all_doubles(self):
    for value in range(1, 7):
      moves = self.dice.get_moves([value, value])
      self.assertEqual(moves, [value] * 4)

  def test_get_moves_empty_list(self):
    moves = self.dice.get_moves([])
    self.assertEqual(moves, [])

  def test_get_moves_invalid_input(self):
    moves = self.dice.get_moves(None)
    self.assertEqual(moves, [])

  def test_use_move(self):
    self.dice.values = [2, 4, 6]
    result = self.dice.use_move(4)
    self.assertTrue(result)
    self.assertNotIn(4, self.dice.values)
    self.assertEqual(len(self.dice.values), 2)

  def test_use_move_not_available(self):
    self.dice.values = [2, 4, 6]
    result = self.dice.use_move(3)
    self.assertFalse(result)
    self.assertEqual(len(self.dice.values), 3)

  def test_use_move_empty_values(self):
    self.dice.values = []
    result = self.dice.use_move(3)
    self.assertFalse(result)

  def test_has_moves_available(self):
    self.dice.values = [2, 4]
    self.assertTrue(self.dice.has_moves())

  def test_has_no_moves_available(self):
    self.dice.values = []
    self.assertFalse(self.dice.has_moves())

  def test_can_use_move(self):
    self.dice.values = [2, 4, 6]
    self.assertTrue(self.dice.can_use_move(4))
    self.assertFalse(self.dice.can_use_move(3))

  def test_get_available_moves(self):
    self.dice.values = [2, 4, 6]
    available = self.dice.get_available_moves()
    self.assertEqual(sorted(available), [2, 4, 6])

  def test_reset_dice(self):
    self.dice.last_roll = [3, 5]
    self.dice.values = [3, 5]
    self.dice.reset()
    self.assertIsNone(self.dice.last_roll)
    self.assertEqual(self.dice.values, [])

  def test_roll_updates_values(self):
    values = self.dice.roll()
    expected_values = self.dice.get_moves(values)
    self.assertEqual(self.dice.values, expected_values)

  @patch("random.randint")
  def test_multiple_rolls(self, mock_randint):
    mock_randint.side_effect = [1, 2, 6, 6]
    first_roll = self.dice.roll()
    self.assertEqual(first_roll, [1, 2])
    
    second_roll = self.dice.roll()
    self.assertEqual(second_roll, [6, 6])
    self.assertEqual(self.dice.values, [6, 6, 6, 6])  # Double gives 4 moves

  @patch("random.randint")
  def test_consecutive_different_rolls(self, mock_randint):
    # Test a sequence of different roll types
    mock_randint.side_effect = [1, 6, 3, 3, 2, 5]
    
    # First roll: normal
    first_roll = self.dice.roll()
    self.assertEqual(first_roll, [1, 6])
    self.assertFalse(self.dice.is_double())
    
    # Second roll: double
    second_roll = self.dice.roll()
    self.assertEqual(second_roll, [3, 3])
    self.assertTrue(self.dice.is_double())
    
    # Third roll: normal again
    third_roll = self.dice.roll()
    self.assertEqual(third_roll, [2, 5])
    self.assertFalse(self.dice.is_double())

  def test_str_representation(self):
    self.dice.last_roll = [3, 5]
    dice_str = str(self.dice)
    self.assertIn("3", dice_str)
    self.assertIn("5", dice_str)

  def test_str_no_roll(self):
    dice_str = str(self.dice)
    self.assertIsInstance(dice_str, str)

  def test_equality(self):
    dice2 = Dice()
    dice2.last_roll = self.dice.last_roll
    dice2.values = self.dice.values

  def test_copy_dice_state(self):
    self.dice.last_roll = [4, 6]
    self.dice.values = [4, 6]
    state = self.dice.get_state()
    self.assertEqual(state["last_roll"], [4, 6])
    self.assertEqual(state["values"], [4, 6])

  def test_set_dice_state(self):
    state = {"last_roll": [2, 3], "values": [2, 3]}
    self.dice.set_state(state)
    self.assertEqual(self.dice.last_roll, [2, 3])
    self.assertEqual(self.dice.values, [2, 3])

  @patch("random.randint")
  def test_roll_all_possible_doubles(self, mock_randint):
    # Test all possible double combinations
    for value in range(1, 7):
        mock_randint.side_effect = [value, value]
        result = self.dice.roll()
        self.assertEqual(result, [value, value])
        self.assertTrue(self.dice.is_double())
        self.assertEqual(self.dice.values, [value] * 4)

  @patch("random.randint")
  def test_roll_boundary_values(self, mock_randint):
    # Test minimum values
    mock_randint.side_effect = [1, 1]
    result = self.dice.roll()
    self.assertEqual(result, [1, 1])
    
    # Test maximum values
    mock_randint.side_effect = [6, 6]
    result = self.dice.roll()
    self.assertEqual(result, [6, 6])

  @patch("random.randint")
  def test_move_usage_with_double(self, mock_randint):
    mock_randint.side_effect = [4, 4]
    self.dice.roll()
    
    # Should have 4 moves of value 4
    self.assertEqual(self.dice.values, [4, 4, 4, 4])
    
    # Use moves one by one
    self.assertTrue(self.dice.use_move(4))
    self.assertEqual(len(self.dice.values), 3)
    
    self.assertTrue(self.dice.use_move(4))
    self.assertEqual(len(self.dice.values), 2)

if __name__ == "__main__":
  unittest.main()
