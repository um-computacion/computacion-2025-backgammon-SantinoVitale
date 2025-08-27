import unittest
from backgammon.core import Player

class TestPlayer(unittest.TestCase):

  def setUp(self):
    self.player = Player()