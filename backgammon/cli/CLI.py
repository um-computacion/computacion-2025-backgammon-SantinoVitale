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
        Display the current board state in ASCII format with proper alignment.

        Args:
            board: Board object containing game state (optional, uses game.board if not provided)
        """
        if board is None and self.game:
            board = self.game.board

        if not board:
            print("No hay tablero disponible para mostrar")
            return

        # Get bar and off information
        bar_white = len(board.bar.get("white", [])) if hasattr(board, "bar") else 0
        bar_black = len(board.bar.get("black", [])) if hasattr(board, "bar") else 0
        off_white = len(board.off.get("white", [])) if hasattr(board, "off") else 0
        off_black = len(board.off.get("black", [])) if hasattr(board, "off") else 0

        # Helper function to get single checker character
        def get_checker(point_index, row):
            """Get single checker character"""
            if not hasattr(board, "points") or point_index < 0 or point_index >= 24:
                return " "
            checkers = board.points[point_index]
            if len(checkers) > row:
                if hasattr(checkers[row], "color"):
                    return "●" if checkers[row].color == "white" else "○"
            return " "

        # Header
        print("\n╔═══════════════════════════════════════════════════════════╗")
        print("║                    TABLERO DE BACKGAMMON                  ║")
        print("║  ◄── BLANCAS (●) hacia 0  |  NEGRAS (○) hacia 25 ──►      ║")
        print("╠═══════════════════════════════════════════════════════════╣")

        # Top row: point numbers - cada punto ocupa 4 caracteres
        print("║ 13  14  15  16  17  18 ║BAR║ 19  20  21  22  23  24 ║ OFF ║")
        print("║ ──  ──  ──  ──  ──  ── ╠═══╣ ──  ──  ──  ──  ──  ── ╠═════╣")

        # Top checkers (5 rows) - cada ficha centrada en 4 caracteres
        for row in range(5):
            # Points 13-18 (indices 12-17)
            left_checkers = []
            for i in range(12, 18):
                ch = get_checker(i, row)
                left_checkers.append(f" {ch}  ")

            # Bar display
            if row == 0:
                bar_display = f"W:{bar_white}"
            elif row == 1:
                bar_display = f"B:{bar_black}"
            else:
                bar_display = "   "

            # Points 19-24 (indices 18-23)
            right_checkers = []
            for i in range(18, 24):
                ch = get_checker(i, row)
                right_checkers.append(f" {ch}  ")

            # OFF display
            if row == 0:
                off_display = f"W:{off_white:2d}"
            elif row == 1:
                off_display = f"B:{off_black:2d}"
            else:
                off_display = "    "

            print(
                f"║{''.join(left_checkers)}║{bar_display}║{''.join(right_checkers)}║{off_display} ║"
            )

        # Middle separator
        print("╠════════════════════════╬═══╬════════════════════════╬═════╣")

        # Bottom checkers (5 rows, reversed) - cada ficha centrada en 4 caracteres
        for row in range(4, -1, -1):
            # Points 12-7 (indices 11-6, descending)
            left_checkers = []
            for i in range(11, 5, -1):
                ch = get_checker(i, row)
                left_checkers.append(f" {ch}  ")

            # Points 6-1 (indices 5-0, descending)
            right_checkers = []
            for i in range(5, -1, -1):
                ch = get_checker(i, row)
                right_checkers.append(f" {ch}  ")

            print(
                f"║{''.join(left_checkers)}║   ║{''.join(right_checkers)}║     ║"
            )

        # Bottom row: point numbers
        print("║ ──  ──  ──  ──  ──  ── ╠═══╣ ──  ──  ──  ──  ──  ── ╚═════╝")
        print("║ 12  11  10  09  08  07 ║BAR║ 06  05  04  03  02  01         ")
        print("╚════════════════════════╩═══╩════════════════════════╝        ")

        # Legend and game state
        print("\n┌────────────────────────────────────────────────────┐")
        print("│ ● = Blancas  |  ○ = Negras                         │")
        print("├────────────────────────────────────────────────────┤")
        print(f"│ BARRA → Blancas: {bar_white:2d}  |  Negras: {bar_black:2d}                 │")
        print(f"│ FUERA → Blancas: {off_white:2d}  |  Negras: {off_black:2d}                 │")

        # Show current player if available
        if self.game and hasattr(self.game, "get_current_player") and self.game.players:
            try:
                current_player = self.game.get_current_player()
                if current_player:
                    player_color = (
                        "Blancas (●)"
                        if current_player.color == "white"
                        else "Negras (○)"
                    )
                    # Box width is 52 chars inside (54 - 2 for borders)
                    # "│ TURNO → " is 9 chars
                    turno_text = f"{current_player.name} - {player_color}"
                    padding = max(0, 51 - 9 - len(turno_text))
                    print(f"│ TURNO → {turno_text}{' ' * padding} │")
            except (IndexError, AttributeError):
                # No players set up yet
                pass

        print("└────────────────────────────────────────────────────┘")

    def get_move_input(self) -> Tuple[Union[int, str], Union[int, str]]:
        """
        Get move input from user.

        Returns:
            Tuple of (from_position, to_position)
            Positions can be integers (1-24), 'bar', or 'off'
        """
        while True:
            try:
                # Show some example moves based on current player
                if self.game and hasattr(self.game, "get_current_player"):
                    current_player = self.game.get_current_player()
                    if current_player.color == "white":
                        examples = "'12 8', '1 fuera'"
                    else:
                        examples = "'8 12', '24 fuera'"
                else:
                    examples = "'12 8', 'barra 20', '1 fuera'"

                print("\n" + "─" * 60)
                prompt = (
                    f"Movimiento DESDE-HASTA (ej: {examples})\n"
                    "o 'ayuda', 'movimientos', 'reglas', 'salir': "
                )
                move_input = input(prompt).strip()
                print("─" * 60)

                # Handle special commands
                if move_input.lower() in [
                    "ayuda",
                    "reglas",
                    "salir",
                    "movimientos",
                    "help",
                    "rules",
                    "quit",
                    "moves",
                ]:
                    return move_input.lower(), None

                parts = move_input.split()

                if len(parts) != 2:
                    print(
                        "\nFormato inválido. Necesita especificar posición DESDE y posición HASTA."
                    )
                    print("   Ejemplo: '12 8' = mover del punto 12 al punto 8")
                    print("   Use 'barra' para la barra y 'fuera' para sacar fichas")
                    continue

                from_pos, to_pos = parts

                # Convert to Spanish alternatives
                if from_pos.lower() == "barra":
                    from_pos = "bar"
                if to_pos.lower() == "fuera":
                    to_pos = "off"

                # Convert numeric positions
                if isinstance(from_pos, str) and from_pos.isdigit():
                    from_pos = int(from_pos)
                if isinstance(to_pos, str) and to_pos.isdigit():
                    to_pos = int(to_pos)

                return from_pos, to_pos

            except (ValueError, KeyboardInterrupt):
                print("\n Entrada inválida. Por favor intente nuevamente.")
                continue

    def display_message(self, message: str) -> None:
        """
        Display a general message to the user.

        Args:
            message: Message text to display
        """
        print(f"\n {message}")

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
        color_spanish = "Blancas (●)" if color == "white" else "Negras (○)"
        default_name = "Jugador Blanco" if color == "white" else "Jugador Negro"
        print(f"\n┌{'─' * 50}┐")
        name = input(f"│ Nombre para {color_spanish}: ").strip()
        print(f"└{'─' * 50}┘")
        if not name:
            return default_name
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
            input(f"¿Confirmar movimiento de {from_pos} a {to_pos}? (s/n): ")
            .strip()
            .lower()
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
            color = getattr(player, "color", "desconocido")
            color_symbol = "●" if color == "white" else "○"
            print("\n")
            print("╔" + "═" * 58 + "╗")
            print("║" + " " * 58 + "║")
            print("║" + " " * 18 + "¡FELICITACIONES!" + " " * 24 + "║")
            print("║" + " " * 58 + "║")
            print(
                f"║  {name} {color_symbol} ha ganado el juego!"
                + " " * (36 - len(name) - 2)
                + "║"
            )
            print("║" + " " * 58 + "║")
            print("╚" + "═" * 58 + "╝")
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
            color_spanish = (
                "Blancas (●)"
                if color == "white"
                else "Negras (○)" if color == "black" else color
            )
            print("\n" + "╔" + "═" * 58 + "╗")
            print(
                f"║  TURNO: {name} - {color_spanish}"
                + " " * (46 - len(name) - len(color_spanish))
                + "║"
            )
            print("╚" + "═" * 58 + "╝")

    def display_dice_roll(self, dice_values: Optional[List[int]] = None) -> None:
        """
        Display the result of a dice roll.

        Args:
            dice_values: List of dice values [die1, die2] (optional, uses game dice if not provided)
        """
        if dice_values is None and self.game:
            if hasattr(self.game, "dice") and hasattr(self.game.dice, "last_roll"):
                dice_values = self.game.dice.last_roll

        if dice_values and len(dice_values) >= 2:
            print("\n┌─────────────────────────────┐")
            if dice_values[0] == dice_values[1]:
                print(
                    f"│ DADOS: [ {dice_values[0]} ] [ {dice_values[1]} ] ¡DOBLE! │"
                )
            else:
                print(f"│ DADOS: [ {dice_values[0]} ] [ {dice_values[1]} ]          │")
            print("└─────────────────────────────┘")

    def display_available_moves(self, moves: Optional[List[int]] = None) -> None:
        """
        Display available moves to the player.

        Args:
            moves: List of available move distances (optional, gets from game if not provided)
        """
        if moves is None and self.game:
            if hasattr(self.game, "dice") and hasattr(
                self.game.dice, "get_available_moves"
            ):
                moves = self.game.dice.get_available_moves()

        if moves:
            moves_str = ", ".join(map(str, moves))
            print(f"\nMovimientos disponibles: [ {moves_str} ]")
        else:
            print("\nNo hay movimientos disponibles")

    def display_possible_moves(self) -> None:
        """
        Display all possible moves for the current player.
        Shows specific from-to position pairs that are valid.
        """
        if not self.game:
            print("\nNo hay juego disponible")
            return

        if hasattr(self.game, "get_possible_moves"):
            possible_moves = self.game.get_possible_moves()

            if not possible_moves:
                print("\nNo hay movimientos válidos disponibles")
                return

            print("\n╔═══════════════════════════════════════════════════════╗")
            print("║           MOVIMIENTOS POSIBLES                        ║")
            print("╠═══════════════════════════════════════════════════════╣")

            # Group moves by from position for better readability
            moves_dict = {}
            for from_pos, to_pos in possible_moves:
                from_str = self.format_position(from_pos)
                to_str = self.format_position(to_pos)
                if from_str not in moves_dict:
                    moves_dict[from_str] = []
                moves_dict[from_str].append(to_str)

            # Display grouped moves
            for from_pos in sorted(
                moves_dict.keys(), key=lambda x: (isinstance(x, str), x)
            ):
                to_positions = ", ".join(moves_dict[from_pos])
                move_text = f"  {from_pos} → {to_positions}"
                # Pad to 55 characters (accounting for border)
                padding = max(0, 53 - len(move_text))
                print(f"║{move_text}{' ' * padding}  ║")

            print("╠═══════════════════════════════════════════════════════╣")
            total_text = (
                f"  Total: {len(possible_moves)} movimiento(s) válido(s)"
            )
            padding = max(0, 53 - len(total_text))
            print(f"║{total_text}{' ' * padding}  ║")
            print("╚═══════════════════════════════════════════════════════╝")
        else:
            print("\nFunción no disponible")

    def display_help(self) -> None:
        """Display help information."""
        print("\n╔" + "═" * 68 + "╗")
        print("║" + " " * 24 + "AYUDA DE BACKGAMMON" + " " * 25 + "║")
        print("╠" + "═" * 68 + "╣")
        print("║  COMANDOS BÁSICOS:" + " " * 49 + "║")
        print("║  • 'desde hasta' - Realizar movimiento (ej: '12 8', '1 fuera')     ║")
        print("║  • 'movimientos' - Ver todos los movimientos posibles" + " " * 14 + "║")
        print("║  • 'ayuda' - Mostrar esta ayuda" + " " * 36 + "║")
        print("║  • 'reglas' - Mostrar reglas del juego" + " " * 29 + "║")
        print("║  • 'salir' - Salir del juego" + " " * 39 + "║")
        print("╠" + "═" * 68 + "╣")
        print("║  FORMATO DE MOVIMIENTO:" + " " * 44 + "║")
        print("║  • Números 1-24 para posiciones del tablero" + " " * 24 + "║")
        print("║  • 'barra' para fichas en la barra" + " " * 33 + "║")
        print("║  • 'fuera' para sacar fichas del tablero" + " " * 27 + "║")
        print("╠" + "═" * 68 + "╣")
        print("║  EJEMPLOS:" + " " * 57 + "║")
        print("║  • '8 12' - Mover del punto 8 al punto 12" + " " * 26 + "║")
        print("║  • 'barra 20' - Mover de la barra al punto 20" + " " * 22 + "║")
        print("║  • '6 fuera' - Sacar ficha del punto 6" + " " * 29 + "║")
        print("╚" + "═" * 68 + "╝")

    def display_game_rules(self) -> None:
        """Display the rules of backgammon."""
        print("\n╔" + "═" * 78 + "╗")
        print("║" + " " * 28 + "REGLAS DE BACKGAMMON" + " " * 30 + "║")
        print("╠" + "═" * 78 + "╣")
        print("║  OBJETIVO:" + " " * 67 + "║")
        print(
            "║  Mover todas tus fichas a tu tablero casa y sacarlas del juego."
            + " " * 14
            + "║"
        )
        print(
            "║  • Blancas (●): puntos 1-6  |  Negras (○): puntos 19-24"
            + " " * 22
            + "║"
        )
        print("╠" + "═" * 78 + "╣")
        print("║  MOVIMIENTO:" + " " * 65 + "║")
        print(
            "║  • Lanza dos dados para determinar tus movimientos"
            + " " * 27
            + "║"
        )
        print(
            "║  • Mueve fichas el número de puntos mostrado en los dados"
            + " " * 20
            + "║"
        )
        print(
            "║  • Si sacas dobles, obtienes cuatro movimientos de ese número"
            + " " * 16
            + "║"
        )
        print("║  • Debes usar ambos dados si es posible" + " " * 38 + "║")
        print("╠" + "═" * 78 + "╣")
        print("║  REGLAS ESPECIALES:" + " " * 58 + "║")
        print(
            "║  • Golpea fichas del oponente para enviarlas a la barra"
            + " " * 22
            + "║"
        )
        print(
            "║  • Debes ingresar fichas de la barra antes de otros movimientos"
            + " " * 14
            + "║"
        )
        print(
            "║  • Solo puedes sacar cuando todas estén en el tablero casa"
            + " " * 19
            + "║"
        )
        print(
            "║  • No puedes mover a puntos con 2+ fichas del oponente"
            + " " * 23
            + "║"
        )
        print("╠" + "═" * 78 + "╣")
        print("║  GANADOR:" + " " * 68 + "║")
        print(
            "║  ¡El primer jugador en sacar todas sus fichas gana!"
            + " " * 26
            + "║"
        )
        print("╚" + "═" * 78 + "╝")

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
        if position in ("bar", "barra"):
            return "BARRA"
        if position in ("off", "fuera"):
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

        # Welcome banner
        print("\n")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + " " * 25 + "BACKGAMMON" + " " * 43 + "║")
        print("║" + " " * 78 + "║")
        print("║" + " " * 20 + "Juego local para dos jugadores" + " " * 28 + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")

        # Get player names
        player1_name = self.get_player_name("white")
        player2_name = self.get_player_name("black")

        # Setup and start game
        if hasattr(self.game, "setup_players"):
            self.game.setup_players(player1_name, player2_name)

        if hasattr(self.game, "start_game"):
            self.game.start_game()

        print("\n¡Juego iniciado! Que comience la partida...\n")

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
                    self.display_message(
                        "No hay movimientos válidos disponibles. Turno omitido."
                    )
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
                    if from_pos in ["moves", "movimientos"]:
                        self.display_possible_moves()
                        continue
                    if from_pos in ["rules", "reglas"]:
                        self.display_game_rules()
                        continue
                    if from_pos in ["quit", "salir"]:
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
                                # Show more helpful error message
                                if hasattr(self.game, "get_possible_moves"):
                                    possible_moves = self.game.get_possible_moves()
                                    if possible_moves:
                                        self.display_error(
                                            f"Movimiento inválido: {from_pos} a {to_pos}."
                                        )
                                        print("Movimientos válidos disponibles:")
                                        for fp, tp in possible_moves[:5]:
                                            print(f"  {fp} {tp}")
                                        if len(possible_moves) > 5:
                                            print(
                                                f"  ... y {len(possible_moves) - 5} más"
                                            )
                                    else:
                                        self.display_error(
                                            "No hay movimientos válidos disponibles."
                                        )
                                else:
                                    self.display_error(
                                        "Movimiento inválido. Intente nuevamente."
                                    )
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
