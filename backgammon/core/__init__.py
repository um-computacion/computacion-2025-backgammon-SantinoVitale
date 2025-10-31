"""
Core module for Backgammon game.

This package contains all the core classes and functionality for the
Backgammon game including game logic, board management, and player handling.
"""
from .dice import Dice
from .player import Player
from .board import Board
from .checker import Checker
from .backgammon_game import BackgammonGame

__all__ = ['Dice', 'Player', 'Board', 'Checker', 'BackgammonGame']
