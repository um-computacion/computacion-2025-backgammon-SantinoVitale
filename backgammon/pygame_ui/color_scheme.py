"""
Color scheme for Backgammon board.
Defines all colors used in the board rendering.
"""

from typing import Tuple


class ColorScheme:
    """
    Manages color definitions for the Backgammon board.

    Attributes:
        WOOD_ORANGE: Main board wood texture color (orange/beige tone)
        DARK_BROWN: Dark brown border color
        LIGHT_BEIGE: Light beige color for alternating points
        DARK_BROWN_POINT: Dark brown color for alternating points
        GREEN_BAR: Green color for central bar
        BRASS: Brass/gold color for hinges
        GREEN_STRIPE: Green color for diagonal stripes
        YELLOW_STRIPE: Yellow color for diagonal stripes
        BLACK: Black color for borders and details
    """

    # Main board colors
    WOOD_ORANGE: Tuple[int, int, int] = (210, 150, 90)  # Orange/beige wood
    DARK_BROWN: Tuple[int, int, int] = (60, 40, 20)  # Dark brown border

    # Point colors (triangles)
    LIGHT_BEIGE: Tuple[int, int, int] = (220, 200, 170)  # Light beige point
    DARK_BROWN_POINT: Tuple[int, int, int] = (100, 70, 40)  # Dark brown point

    # Bar colors
    GREEN_BAR: Tuple[int, int, int] = (40, 100, 60)  # Green central bar
    BRASS: Tuple[int, int, int] = (180, 150, 80)  # Brass hinges

    # Side panel colors
    GREEN_STRIPE: Tuple[int, int, int] = (50, 120, 70)  # Green diagonal stripe
    YELLOW_STRIPE: Tuple[int, int, int] = (200, 180, 60)  # Yellow diagonal stripe

    # Utility colors
    BLACK: Tuple[int, int, int] = (0, 0, 0)  # Black
