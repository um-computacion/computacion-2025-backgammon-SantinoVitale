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
            print("No hay tablero disponible para mostrar")
            return

        print("\n" + "=" * 50)
        print("TABLERO DE BACKGAMMON")
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
        print(f"\nFUERA: Blancas: {off_white}, Negras: {off_black}")
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
                    "Ingrese movimiento (ej: '1 4', 'barra 20', '1 fuera'): "
                ).strip()

                # Handle special commands
                if move_input.lower() in ["ayuda", "reglas", "salir", "help", "rules", "quit"]:
                    return move_input.lower(), None

                parts = move_input.split()

                if len(parts) != 2:
                    print(
                        "Formato inválido. Por favor ingrese dos posiciones separadas por espacio."
                    )
                    continue

                from_pos, to_pos = parts

                # Convert to Spanish alternatives
                if from_pos == "barra":
                    from_pos = "bar"
                if to_pos == "fuera":
                    to_pos = "off"

                # Convert numeric positions
                if from_pos.isdigit():
                    from_pos = int(from_pos)
                if to_pos.isdigit():
                    to_pos = int(to_pos)

                return from_pos, to_pos

            except (ValueError, KeyboardInterrupt):
                print("Entrada inválida. Por favor intente nuevamente.")
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
        color_spanish = "blanco" if color == "white" else "negro"
        name = input(f"Ingrese nombre para el jugador {color_spanish}: ").strip()
        if not name:
            return f"Jugador {color_spanish.title()}"
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
            input(f"¿Confirmar movimiento de {from_pos} a {to_pos}? (s/n): ").strip().lower()
        )
        return response in ["s", "sí", "si", "y", "yes"]

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
            name = getattr(player, "name", "Desconocido")
            print("\n🎉 ¡FELICITACIONES! 🎉")
            print(f"¡{name} gana el juego!")
            print("=" * 30)
        else:
            print("\n¡Juego terminado!")

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
            name = getattr(player, "name", "Desconocido")
            color = getattr(player, "color", "desconocido")
            color_spanish = "blanco" if color == "white" else "negro" if color == "black" else color
            print(f"\n{name} ({color_spanish}) - ¡Es tu turno!")

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
                print(f"\n🎲 Lanzamiento de dados: {dice_values[0]}, {dice_values[1]} - ¡DOBLE!")
            else:
                print(f"\n🎲 Lanzamiento de dados: {dice_values[0]}, {dice_values[1]}")

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
            print(f"Movimientos disponibles: {', '.join(map(str, moves))}")
        else:
            print("No hay movimientos disponibles")

    def display_help(self) -> None:
        """Display help information."""
        help_text = """
AYUDA DE BACKGAMMON
===================

Comandos Básicos:
- Ingrese movimientos como 'desde hasta' (ej: '1 4', 'barra 20', '6 fuera')
- 'ayuda' - Mostrar esta ayuda
- 'reglas' - Mostrar reglas del juego
- 'salir' - Salir del juego

Formato de Movimiento:
- Use números de punto 1-24
- Use 'barra' para fichas en la barra
- Use 'fuera' para sacar fichas

Ejemplos de movimientos:
- '8 12' - Mover del punto 8 al punto 12
- 'barra 20' - Mover de la barra al punto 20
- '6 fuera' - Sacar ficha del punto 6
"""
        print(help_text)

    def display_game_rules(self) -> None:
        """Display the rules of backgammon."""
        rules_text = """
REGLAS DE BACKGAMMON
====================

Objetivo: Mover todas tus fichas a tu tablero casa (puntos 1-6 para blancas, 19-24 para negras) y sacarlas.

Configuración: Cada jugador comienza con 15 fichas dispuestas en el tablero.

Movimiento:
- Lanza dos dados para determinar movimientos
- Mueve fichas el número de puntos mostrado en los dados
- Si sacas dobles, obtienes cuatro movimientos de ese número
- Debes usar ambos dados si es posible

Reglas Especiales:
- Golpea fichas del oponente para enviarlas a la barra
- Debes ingresar fichas de la barra antes de hacer otros movimientos
- Solo puedes sacar fichas cuando todas estén en el tablero casa
- No puedes mover a puntos ocupados por 2+ fichas del oponente

¡Ganador: El primer jugador en sacar todas las fichas gana!
"""
        print(rules_text)

    def pause_game(self) -> None:
        """Pause the game and wait for user input."""
        input("\nPresione Enter para continuar...")

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
        if position == "bar" or position == "barra":
            return "BARRA"
        if position == "off" or position == "fuera":
            return "FUERA"
        return str(position)

    def get_valid_position(self) -> int:
        """
        Get a valid position (1-24) from user input.

        Returns:
            Valid position number
        """
        while True:
            try:
                position = int(input("Ingrese posición (1-24): ").strip())
                if 1 <= position <= 24:
                    return position
                print("La posición debe estar entre 1 y 24.")
            except ValueError:
                print("Por favor ingrese un número válido.")

    def confirm_quit(self) -> bool:
        """
        Confirm if user wants to quit the game.

        Returns:
            True if confirmed, False otherwise
        """
        response = input("¿Está seguro que desea salir? (s/n): ").strip().lower()
        return response in ["s", "sí", "si", "y", "yes"]

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
            print("\nEstadísticas del Juego:")
            print("=" * 22)
            for key, value in stats.items():
                print(f"{key.title()}: {value}")
            print("=" * 22)

    def run_game(self) -> None:
        """
        Main game loop for CLI interface.

        Simple local two-player Backgammon game.
        """
        if not self.game:
            print("Error: No hay instancia de juego disponible")
            return

        self.display_message("¡Bienvenido al Backgammon!")
        self.display_message("Juego local de dos jugadores")

        # Get player names
        player1_name = self.get_player_name("white")
        player2_name = self.get_player_name("black")

        # Setup and start game
        if hasattr(self.game, "setup_players"):
            self.game.setup_players(player1_name, player2_name)

        if hasattr(self.game, "start_game"):
            self.game.start_game()

        # Main game loop
        while True:
            try:
                # Check if game is over
                if hasattr(self.game, "is_game_over") and self.game.is_game_over():
                    self.display_winner()
                    break

                # Display current state
                self.clear_screen()
                self.display_board()
                self.display_current_player()

                # Roll dice if no moves available (start of turn)
                if (
                    hasattr(self.game, "dice")
                    and hasattr(self.game.dice, "get_available_moves")
                    and not self.game.dice.get_available_moves()
                ):
                    if hasattr(self.game, "roll_dice"):
                        dice_values = self.game.roll_dice()
                        self.display_dice_roll(dice_values)

                # Display available moves
                if hasattr(self.game, "dice") and hasattr(
                    self.game.dice, "get_available_moves"
                ):
                    moves = self.game.dice.get_available_moves()
                    self.display_available_moves(moves)

                # Check if player has valid moves
                if (
                    hasattr(self.game, "has_valid_moves")
                    and not self.game.has_valid_moves()
                ):
                    self.display_message("No hay movimientos válidos disponibles. Turno omitido.")
                    if hasattr(self.game, "switch_turns"):
                        self.game.switch_turns()
                    continue

                # Human player turn - get moves until all dice used
                while (
                    hasattr(self.game, "dice")
                    and hasattr(self.game.dice, "has_moves")
                    and self.game.dice.has_moves()
                    and hasattr(self.game, "has_valid_moves")
                    and self.game.has_valid_moves()
                ):

                    from_pos, to_pos = self.get_move_input()

                    # Handle special commands
                    if from_pos in ["help", "ayuda"]:
                        self.display_help()
                        continue
                    elif from_pos in ["rules", "reglas"]:
                        self.display_game_rules()
                        continue
                    elif from_pos in ["quit", "salir"]:
                        if self.confirm_quit():
                            return
                        continue

                    # Try to make the move
                    if hasattr(self.game, "make_move"):
                        try:
                            if self.game.make_move(from_pos, to_pos):
                                self.display_message(
                                    f"Movimiento realizado: {from_pos} a {to_pos}"
                                )

                                # Consume the dice move
                                if hasattr(self.game, "calculate_move_distance"):
                                    distance = self.game.calculate_move_distance(
                                        from_pos, to_pos
                                    )
                                    if distance > 0 and hasattr(
                                        self.game.dice, "use_move"
                                    ):
                                        self.game.dice.use_move(distance)

                                # Update display after successful move
                                self.display_board()
                                if hasattr(self.game, "dice"):
                                    remaining_moves = (
                                        self.game.dice.get_available_moves()
                                    )
                                    if remaining_moves:
                                        self.display_available_moves(remaining_moves)
                                    else:
                                        self.display_message("¡Todos los dados usados!")
                                        break
                            else:
                                self.display_error("Movimiento inválido. Intente nuevamente.")
                        except (ValueError, TypeError, AttributeError) as e:
                            self.display_error(f"Movimiento falló: {str(e)}")

                # Complete turn and switch players if dice are used up or no valid moves
                if hasattr(self.game, "can_continue_turn"):
                    if not self.game.can_continue_turn():
                        if hasattr(self.game, "complete_turn"):
                            self.game.complete_turn()
                        else:
                            # Fallback to direct turn switching
                            if hasattr(self.game, "switch_turns"):
                                self.game.switch_turns()
                else:
                    # Fallback behavior
                    if hasattr(self.game, "switch_turns"):
                        self.game.switch_turns()

            except KeyboardInterrupt:
                if self.confirm_quit():
                    break
            except (ValueError, TypeError, AttributeError) as e:
                self.display_error(f"Error del juego: {str(e)}")
                break

        self.display_message("¡Gracias por jugar!")
