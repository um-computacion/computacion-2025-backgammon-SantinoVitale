import unittest
from backgammon.core import Dice

class TestDice(unittest.TestCase):

  def setUp(self):
    self.dice = Dice()