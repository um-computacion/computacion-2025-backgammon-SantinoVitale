"""
Board dimensions and layout calculations for Backgammon board.
Manages all measurements and spacing for board components.
"""

from typing import Tuple


class BoardDimensions:
    """
    Calculates and stores dimensions for the Backgammon board layout.

    Attributes:
        screen_width: Total screen width
        screen_height: Total screen height
        border_thickness: Thickness of the outer border
        bar_width: Width of the central bar
        side_panel_width: Width of the right side panel
        board_x: X coordinate of board start
        board_y: Y coordinate of board start
        board_width: Total width of the board
        board_height: Total height of the board
        playable_width: Width of playable area (excluding bar and side panel)
        half_width: Width of each half of the board
        point_width: Width of each triangular point
        point_height: Height of each triangular point
    """

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """
        Initialize board dimensions.

        Args:
            screen_width: Total screen width in pixels
            screen_height: Total screen height in pixels
        """
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height

        # Border and spacing
        self.border_thickness: int = 20

        # Board position and size
        self.board_x: int = 40
        self.board_y: int = 40
        self.board_width: int = screen_width - (2 * self.board_x)
        self.board_height: int = screen_height - (2 * self.board_y)

        # Component widths
        self.bar_width: int = 50
        self.side_panel_width: int = 80

        # Calculate playable area
        self.playable_width: int = (
            self.board_width
            - self.bar_width
            - self.side_panel_width
            - (2 * self.border_thickness)
        )
        self.half_width: int = self.playable_width // 2

        # Point dimensions
        self.point_width: int = self.half_width // 6
        self.point_height: int = (
            self.board_height - (2 * self.border_thickness)
        ) // 2 - 10

    def get_board_rect(self) -> Tuple[int, int, int, int]:
        """
        Get the main board rectangle coordinates.

        Returns:
            Tuple of (x, y, width, height)
        """
        return (self.board_x, self.board_y, self.board_width, self.board_height)

    def get_inner_board_rect(self) -> Tuple[int, int, int, int]:
        """
        Get the inner board rectangle (inside the border).

        Returns:
            Tuple of (x, y, width, height)
        """
        return (
            self.board_x + self.border_thickness,
            self.board_y + self.border_thickness,
            self.board_width - (2 * self.border_thickness),
            self.board_height - (2 * self.border_thickness),
        )

    def get_point_base_y(self, is_top: bool) -> int:
        """
        Get the Y coordinate for the base of a point.

        Args:
            is_top: True for top points, False for bottom points

        Returns:
            Y coordinate of the point base
        """
        inner_y = self.board_y + self.border_thickness
        if is_top:
            return inner_y
        else:
            return inner_y + self.board_height - (2 * self.border_thickness)

    def get_point_x(self, point_number: int) -> int:
        """
        Get the X coordinate for a point (0-23).

        Args:
            point_number: Point number (0-23, starting from top-right going counterclockwise)

        Returns:
            X coordinate of the point's left edge
        """
        start_x = self.board_x + self.border_thickness

        # Points 0-5: top right (right to left)
        # Points 6-11: top left (right to left)
        # Points 12-17: bottom left (left to right)
        # Points 18-23: bottom right (left to right)

        if 0 <= point_number <= 5:
            # Top right quadrant
            offset = (5 - point_number) * self.point_width
            return start_x + self.half_width + self.bar_width + offset
        elif 6 <= point_number <= 11:
            # Top left quadrant
            offset = (11 - point_number) * self.point_width
            return start_x + offset
        elif 12 <= point_number <= 17:
            # Bottom left quadrant
            offset = (point_number - 12) * self.point_width
            return start_x + offset
        else:  # 18 <= point_number <= 23
            # Bottom right quadrant
            offset = (point_number - 18) * self.point_width
            return start_x + self.half_width + self.bar_width + offset

    def get_bar_rect(self) -> Tuple[int, int, int, int]:
        """
        Get the central bar rectangle coordinates.

        Returns:
            Tuple of (x, y, width, height)
        """
        x = self.board_x + self.border_thickness + self.half_width
        y = self.board_y + self.border_thickness
        height = self.board_height - (2 * self.border_thickness)
        return (x, y, self.bar_width, height)

    def get_side_panel_rect(self) -> Tuple[int, int, int, int]:
        """
        Get the right side panel rectangle coordinates.

        Returns:
            Tuple of (x, y, width, height)
        """
        x = (
            self.board_x
            + self.board_width
            - self.border_thickness
            - self.side_panel_width
        )
        y = self.board_y + self.border_thickness
        height = self.board_height - (2 * self.border_thickness)
        return (x, y, self.side_panel_width, height)
