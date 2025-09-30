"""
Package entry point for Backgammon game.
Allows running the game using 'python -m backgammon' command.
"""

import sys
import os

# Add the parent directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main

if __name__ == "__main__":
    main()