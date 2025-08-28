import unittest
from backgammon.core import Board

class TestBoard(unittest.TestCase):

  def setUp(self):
    self.board = Board()
