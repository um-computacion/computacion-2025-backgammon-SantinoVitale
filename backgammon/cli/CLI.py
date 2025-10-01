"""
CLI interface for the Backgammon game.
Provides command-line interaction methods for displaying the board,
getting user input, and managing game flow using BackgammonGame.
"""

# pylint: disable=invalid-name  # CLI follows PascalCase class naming convention
# pylint: disable=too-many-branches  # Complex user input handling requires branching

import os
from typing import Tuple, List, Union, Dict, Any, Optional


class CLI:
    """
    Command Line Interface for Backgammon game.

    This class uses BackgammonGame to handle game logic and provides
    a console-based interface for:
    - Board display and formatting
    - User input collection and validation
    - Game state communication
    - Help and rules display
    """

    def __init__(self, game=None) -> None:
        """
        Initialize the CLI interface.

        Args:
            game: BackgammonGame instance to interact with
        """
        self.game = game

    def set_game(self, game) -> None:
        """
        Set the BackgammonGame instance for the CLI.

        Args:
            game: BackgammonGame instance
        """
        self.game = game

    def display_board(self, board=None) -> None:  # pylint: disable=too-many-branches
        """
        Display the current board state in ASCII format.

        Args:
            board: Board object containing game state (optional, uses game.board if not provided)
        """
        if board is None and self.game:
            board = self.game.board

        if not board:
            print("No board available to display")
            return

        print("\n" + "=" * 50)
        print("BACKGAMMON BOARD")
        print("=" * 50)

        # Top half of board (points 13-24)
        top_line = "13 14 15 16 17 18   BAR   19 20 21 22 23 24"
        print(f"   {top_line}")

        # Display top checkers
        for row in range(5):
            line = " "
            for point in range(13, 19):
                checkers = board.points[point - 1] if hasattr(board, "points") else []
                if len(checkers) > row:
                    color = (
                        checkers[row].color[0].upper()
                        if hasattr(checkers[row], "color")
                        else "X"
                    )
                    line += f" {color} "
                else:
                    line += "   "

            # Bar display
            bar_white = len(board.bar.get("white", [])) if hasattr(board, "bar") else 0
            bar_black = len(board.bar.get("black", [])) if hasattr(board, "bar") else 0
            if row == 0 and bar_white > 0:
                line += f"  W{bar_white} "
            elif row == 1 and bar_black > 0:
                line += f"  B{bar_black} "
            else:
                line += "     "

            for point in range(19, 25):
                checkers = board.points[point - 1] if hasattr(board, "points") else []
                if len(checkers) > row:
                    color = (
                        checkers[row].color[0].upper()
                        if hasattr(checkers[row], "color")
                        else "X"
                    )
                    line += f" {color} "
                else:
                    line += "   "
            print(line)

        print("   " + "-" * 45)

        # Bottom half of board (points 12-1)
        for row in range(4, -1, -1):
            line = " "
            for point in range(12, 6, -1):
                checkers = board.points[point - 1] if hasattr(board, "points") else []
                if len(checkers) > row:
                    color = (
                        checkers[row].color[0].upper()
                        if hasattr(checkers[row], "color")
                        else "X"
                    )
                    line += f" {color} "
                else:
                    line += "   "

            line += "     "  # Bar space

            for point in range(6, 0, -1):
                checkers = board.points[point - 1] if hasattr(board, "points") else []
                if len(checkers) > row:
                    color = (
                        checkers[row].color[0].upper()
                        if hasattr(checkers[row], "color")
                        else "X"
                    )
                    line += f" {color} "
                else:
                    line += "   "
            print(line)

        bottom_line = "12 11 10  9  8  7         6  5  4  3  2  1"
        print(f"   {bottom_line}")

        # Display off checkers
        off_white = len(board.off.get("white", [])) if hasattr(board, "off") else 0
        off_black = len(board.off.get("black", [])) if hasattr(board, "off") else 0
        print(f"\nOFF: White: {off_white}, Black: {off_black}")
        print("=" * 50)

    def get_move_input(self) -> Tuple[Union[int, str], Union[int, str]]:
        """
        Get move input from user.

        Returns:
            Tuple of (from_position, to_position)
            Positions can be integers (1-24), 'bar', or 'off'
        """
        while True:
            try:
                move_input = input(
                    "Enter move (e.g., '1 4', 'bar 20', '1 off'): "
                ).strip()

                # Handle special commands
                if move_input.lower() in ["help", "rules", "quit"]:
                    return move_input.lower(), None

                parts = move_input.split()

                if len(parts) != 2:
                    print(
                        "Invalid format. Please enter two positions separated by space."
                    )
                    continue

                from_pos, to_pos = parts

                # Convert numeric positions
                if from_pos.isdigit():
                    from_pos = int(from_pos)
                if to_pos.isdigit():
                    to_pos = int(to_pos)

                return from_pos, to_pos

            except (ValueError, KeyboardInterrupt):
                print("Invalid input. Please try again.")
                continue

    def display_message(self, message: str) -> None:
        """
        Display a general message to the user.

        Args:
            message: Message text to display
        """
        print(f"\n{message}")

    def display_error(self, error: str) -> None:
        """
        Display an error message to the user.

        Args:
            error: Error message to display
        """
        print(f"\nError: {error}")

    def get_player_name(self, color: str) -> str:
        """
        Get player name from user input.

        Args:
            color: Player color ('white' or 'black')

        Returns:
            Player name string
        """
        name = input(f"Enter name for {color} player: ").strip()
        if not name:
            return f"{color.title()} Player"
        return name

    def confirm_move(self, from_pos: Union[int, str], to_pos: Union[int, str]) -> bool:
        """
        Ask user to confirm a move.

        Args:
            from_pos: Starting position
            to_pos: Ending position

        Returns:
            True if confirmed, False otherwise
        """
        response = (
            input(f"Confirm move from {from_pos} to {to_pos}? (y/n): ").strip().lower()
        )
        return response in ["y", "yes"]

    def display_winner(self, player=None) -> None:
        """
        Display the winner of the game.

        Args:
            player: Player object who won (optional, uses game winner if not provided)
        """
        if player is None and self.game:
            # Try to get winner from game
            if hasattr(self.game, "get_winner"):
                player = self.game.get_winner()

        if player:
            name = getattr(player, "name", "Unknown")
            print("\n🎉 CONGRATULATIONS! 🎉")
            print(f"{name} wins the game!")
            print("=" * 30)
        else:
            print("\nGame over!")

    def display_current_player(self, player=None) -> None:
        """
        Display whose turn it is.

        Args:
            player: Current player object (optional, uses game current player if not provided)
        """
        if player is None and self.game:
            if hasattr(self.game, "get_current_player"):
                player = self.game.get_current_player()

        if player:
            name = getattr(player, "name", "Unknown")
            color = getattr(player, "color", "unknown")
            print(f"\n{name} ({color}) - Your turn!")

    def display_dice_roll(self, dice_values: Optional[List[int]] = None) -> None:
        """
        Display the result of a dice roll.

        Args:
            dice_values: List of dice values [die1, die2] (optional, uses game dice if not provided)
        """
        if dice_values is None and self.game:
            if hasattr(self.game, "dice") and hasattr(self.game.dice, "values"):
                dice_values = self.game.dice.values

        if dice_values and len(dice_values) >= 2:
            if len(dice_values) == 2 and dice_values[0] == dice_values[1]:
                print(f"\n🎲 Dice roll: {dice_values[0]}, {dice_values[1]} - DOUBLE!")
            else:
                print(f"\n🎲 Dice roll: {dice_values[0]}, {dice_values[1]}")

    def display_available_moves(self, moves: Optional[List[int]] = None) -> None:
        """
        Display available moves to the player.

        Args:
            moves: List of available move distances (optional, gets from game if not provided)
        """
        if moves is None and self.game:
            if hasattr(self.game, "get_available_moves"):
                moves = self.game.get_available_moves()

        if moves:
            print(f"Available moves: {', '.join(map(str, moves))}")
        else:
            print("No moves available")

    def display_help(self) -> None:
        """Display help information."""
        help_text = """
BACKGAMMON HELP
===============

Basic Commands:
- Enter moves as 'from to' (e.g., '1 4', 'bar 20', '6 off')
- 'help' - Show this help
- 'rules' - Show game rules
- 'quit' - Exit the game

Move Format:
- Use point numbers 1-24
- Use 'bar' for pieces on the bar
- Use 'off' to bear off pieces

Example moves:
- '8 12' - Move from point 8 to point 12
- 'bar 20' - Move from bar to point 20
- '6 off' - Bear off from point 6
"""
        print(help_text)

    def display_game_rules(self) -> None:
        """Display the rules of backgammon."""
        rules_text = """
BACKGAMMON RULES
================

Objective: Move all your checkers to your home board (points 1-6 for white, 19-24 for black) and bear them off.

Setup: Each player starts with 15 checkers arranged on the board.

Movement:
- Roll two dice to determine moves
- Move checkers the number of points shown on dice
- If you roll doubles, you get four moves of that number
- You must use both dice if possible

Special Rules:
- Hit opponent checkers to send them to the bar
- Must enter checkers from bar before making other moves
- Can only bear off when all checkers are in home board
- Cannot move to points occupied by 2+ opponent checkers

Winning: First player to bear off all checkers wins!
"""
        print(rules_text)

    def pause_game(self) -> None:
        """Pause the game and wait for user input."""
        input("\nPress Enter to continue...")

    def clear_screen(self) -> None:
        """Clear the console screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def format_position(self, position: Union[int, str]) -> str:
        """
        Format a position for display.

        Args:
            position: Position to format

        Returns:
            Formatted position string
        """
        if position == "bar":
            return "BAR"
        if position == "off":
            return "OFF"
        return str(position)

    def get_valid_position(self) -> int:
        """
        Get a valid position (1-24) from user input.

        Returns:
            Valid position number
        """
        while True:
            try:
                position = int(input("Enter position (1-24): ").strip())
                if 1 <= position <= 24:
                    return position
                print("Position must be between 1 and 24.")
            except ValueError:
                print("Please enter a valid number.")

    def confirm_quit(self) -> bool:
        """
        Confirm if user wants to quit the game.

        Returns:
            True if confirmed, False otherwise
        """
        response = input("Are you sure you want to quit? (y/n): ").strip().lower()
        return response in ["y", "yes"]

    def display_statistics(self, stats: Optional[Dict[str, Any]] = None) -> None:
        """
        Display game statistics.

        Args:
            stats: Dictionary containing game statistics (optional, gets from game if not provided)
        """
        if stats is None and self.game:
            if hasattr(self.game, "get_statistics"):
                stats = self.game.get_statistics()

        if stats:
            print("\nGame Statistics:")
            print("=" * 20)
            for key, value in stats.items():
                print(f"{key.title()}: {value}")
            print("=" * 20)

    def run_game(self) -> None:
        """
        Main game loop for CLI interface.
        
        Simple local two-player Backgammon game.
        """
        if not self.game:
            print("Error: No game instance available")
            return
        
        self.display_message("Welcome to Backgammon!")
        self.display_message("Local two-player game")
        
        # Get player names
        player1_name = self.get_player_name("white")
        player2_name = self.get_player_name("black")
        
        # Setup and start game
        if hasattr(self.game, 'setup_players'):
            self.game.setup_players(player1_name, player2_name)
        
        if hasattr(self.game, 'start_game'):
            self.game.start_game()
        
        # Main game loop
        while True:
            try:
                # Check if game is over
                if hasattr(self.game, 'is_game_over') and self.game.is_game_over():
                    self.display_winner()
                    break
                
                # Display current state
                self.clear_screen()
                self.display_board()
                self.display_current_player()
                
                # Roll dice
                if hasattr(self.game, 'roll_dice'):
                    dice_values = self.game.roll_dice()
                    self.display_dice_roll(dice_values)
                
                # Display available moves
                if hasattr(self.game, 'dice') and hasattr(self.game.dice, 'get_available_moves'):
                    moves = self.game.dice.get_available_moves()
                    self.display_available_moves(moves)
                
                # Human player turn - get moves until all dice used
                while (hasattr(self.game, 'dice') and 
                       hasattr(self.game.dice, 'has_moves_available') and
                       self.game.dice.has_moves_available()):
                    
                    from_pos, to_pos = self.get_move_input()
                    
                    # Handle special commands
                    if from_pos == 'help':
                        self.display_help()
                        continue
                    elif from_pos == 'rules':
                        self.display_game_rules()
                        continue
                    elif from_pos == 'quit':
                        if self.confirm_quit():
                            return
                        continue
                    
                    # Try to make the move
                    if hasattr(self.game, 'make_move'):
                        try:
                            if self.game.make_move(from_pos, to_pos):
                                self.display_message(f"Move made: {from_pos} to {to_pos}")
                                # Update display after successful move
                                self.display_board()
                                if hasattr(self.game, 'dice'):
                                    remaining_moves = self.game.dice.get_available_moves()
                                    if remaining_moves:
                                        self.display_available_moves(remaining_moves)
                                    else:
                                        self.display_message("All dice used!")
                                        break
                            else:
                                self.display_error("Invalid move. Try again.")
                        except (ValueError, TypeError, AttributeError) as e:
                            self.display_error(f"Move failed: {str(e)}")
                
                # Switch players
                if hasattr(self.game, 'switch_turns'):
                    self.game.switch_turns()
            
            except KeyboardInterrupt:
                if self.confirm_quit():
                    break
            except (ValueError, TypeError, AttributeError) as e:
                self.display_error(f"Game error: {str(e)}")
                break
        
        self.display_message("Thanks for playing!")
