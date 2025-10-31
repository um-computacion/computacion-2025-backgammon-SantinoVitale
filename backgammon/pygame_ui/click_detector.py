"""
Click detector for Backgammon board.
Responsible for converting mouse coordinates to board positions.
"""

from typing import Optional, Tuple
from backgammon.pygame_ui.board_dimensions import BoardDimensions


class ClickDetector:
    """
    Detects which board element was clicked based on mouse coordinates.

    This class converts screen coordinates (x, y) into game board positions
    such as point numbers (0-23), bar, or off areas.

    Attributes:
        dimensions: BoardDimensions instance for layout calculations
    """

    def __init__(self, dimensions: BoardDimensions) -> None:
        """
        Initialize the ClickDetector.

        Args:
            dimensions: BoardDimensions instance
        """
        self.dimensions: BoardDimensions = dimensions

    def get_clicked_point(self, mouse_pos: Tuple[int, int]) -> Optional[int]:
        """
        Determine which point (0-23) was clicked, if any.

        Args:
            mouse_pos: Tuple of (x, y) mouse coordinates

        Returns:
            Point number (0-23) if a point was clicked, None otherwise
        """
        mouse_x, mouse_y = mouse_pos

        # Get board boundaries
        board_x = self.dimensions.board_x
        board_y = self.dimensions.board_y
        border = self.dimensions.border_thickness

        # Check if click is within the board
        inner_x = board_x + border
        inner_y = board_y + border
        inner_width = self.dimensions.board_width - (2 * border)
        inner_height = self.dimensions.board_height - (2 * border)

        if not inner_x <= mouse_x <= inner_x + inner_width:
            return None
        if not inner_y <= mouse_y <= inner_y + inner_height:
            return None

        # Check if click is in the bar area (exclude it)
        bar_rect = self.dimensions.get_bar_rect()
        if bar_rect[0] <= mouse_x <= bar_rect[0] + bar_rect[2]:
            return None

        # Check if click is in the side panel (exclude it)
        panel_rect = self.dimensions.get_side_panel_rect()
        if panel_rect[0] <= mouse_x <= panel_rect[0] + panel_rect[2]:
            return None

        # Determine which half of the board (left or right of bar)
        bar_left = bar_rect[0]
        bar_right = bar_rect[0] + bar_rect[2]

        # Determine if click is in top or bottom half
        mid_y = board_y + (self.dimensions.board_height // 2)
        is_top = mouse_y < mid_y

        # Calculate which point was clicked
        if mouse_x < bar_left:
            # Left side of board
            # Points 6-11 (top) or 18-12 (bottom)
            relative_x = mouse_x - inner_x
            point_index_in_half = int(relative_x // self.dimensions.point_width)

            if is_top:
                # Top left: points 11, 10, 9, 8, 7, 6 (right to left)
                point = 11 - point_index_in_half
            else:
                # Bottom left: points 12, 13, 14, 15, 16, 17 (left to right)
                point = 12 + point_index_in_half

        else:
            # Right side of board
            # Points 0-5 (top) or 23-18 (bottom)
            relative_x = mouse_x - bar_right
            point_index_in_half = int(relative_x // self.dimensions.point_width)

            if is_top:
                # Top right: points 5, 4, 3, 2, 1, 0 (right to left)
                point = 5 - point_index_in_half
            else:
                # Bottom right: points 18, 19, 20, 21, 22, 23 (left to right)
                point = 18 + point_index_in_half

        # Validate point is in range
        if 0 <= point <= 23:
            return point

        return None

    def is_bar_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """
        Check if the bar area was clicked.

        Args:
            mouse_pos: Tuple of (x, y) mouse coordinates

        Returns:
            True if bar was clicked, False otherwise
        """
        mouse_x, mouse_y = mouse_pos
        bar_rect = self.dimensions.get_bar_rect()

        return (
            bar_rect[0] <= mouse_x <= bar_rect[0] + bar_rect[2]
            and bar_rect[1] <= mouse_y <= bar_rect[1] + bar_rect[3]
        )

    def is_off_area_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """
        Check if the off area (side panel) was clicked.

        Args:
            mouse_pos: Tuple of (x, y) mouse coordinates

        Returns:
            True if off area was clicked, False otherwise
        """
        mouse_x, mouse_y = mouse_pos
        panel_rect = self.dimensions.get_side_panel_rect()

        # Check if click is in the side panel horizontally
        if not (panel_rect[0] <= mouse_x <= panel_rect[0] + panel_rect[2]):
            return False

        section_height = panel_rect[3] // 3

        # Top section is for white player bearing off
        top_section_start = panel_rect[1]
        top_section_end = panel_rect[1] + section_height

        # Bottom section is for black player bearing off
        bottom_section_start = panel_rect[1] + (2 * section_height)
        bottom_section_end = panel_rect[1] + panel_rect[3]

        # Return True if click is in top section or bottom section
        in_top_section = top_section_start <= mouse_y <= top_section_end
        in_bottom_section = bottom_section_start <= mouse_y <= bottom_section_end

        return in_top_section or in_bottom_section

    def get_clicked_position(
        self, mouse_pos: Tuple[int, int]
    ) -> Optional[Tuple[str, int]]:
        """
        Get the board position that was clicked.

        Args:
            mouse_pos: Tuple of (x, y) mouse coordinates

        Returns:
            Tuple of (position_type, value) where:
            - position_type is 'point', 'bar', or 'off'
            - value is the point number for 'point', or 0 for 'bar'/'off'
            Returns None if no valid position was clicked
        """
        # Check bar first
        if self.is_bar_clicked(mouse_pos):
            return ("bar", 0)

        # Check off area
        if self.is_off_area_clicked(mouse_pos):
            return ("off", 0)

        # Check points
        point = self.get_clicked_point(mouse_pos)
        if point is not None:
            return ("point", point)

        return None

    def get_dice_roll_button_rect(self) -> Tuple[int, int, int, int]:
        """
        Get the rectangle for the dice roll button in the top section of side panel.

        Returns:
            Tuple of (x, y, width, height) for the button
        """
        panel_rect = self.dimensions.get_side_panel_rect()
        section_height = panel_rect[3] // 3

        # Button in top section, centered
        button_width = 60
        button_height = 30
        button_x = panel_rect[0] + (panel_rect[2] - button_width) // 2
        button_y = panel_rect[1] + section_height - 40  # Near bottom of top section

        return (button_x, button_y, button_width, button_height)

    def is_roll_button_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """
        Check if the roll dice button was clicked.

        Args:
            mouse_pos: Tuple of (x, y) mouse coordinates

        Returns:
            True if roll button was clicked, False otherwise
        """
        mouse_x, mouse_y = mouse_pos
        button_rect = self.get_dice_roll_button_rect()

        return (
            button_rect[0] <= mouse_x <= button_rect[0] + button_rect[2]
            and button_rect[1] <= mouse_y <= button_rect[1] + button_rect[3]
        )
