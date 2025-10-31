"""
UserInterface class for Backgammon game.
Responsible only for user input/output operations.
"""

import os
from typing import List, Union, Dict, Any


class UserInterface:
    """
    Handles user input and output for Backgammon CLI.

    Single Responsibility: Only handles user I/O operations.
    """

    def __init__(self) -> None:
        """Initialize the UserInterface."""

    def display(self, message: str) -> None:
        """
        Display a message to the user.

        Args:
            message: Message to display
        """
        print(message)

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

    def get_input(self, prompt: str) -> str:
        """
        Get user input with a prompt.

        Args:
            prompt: Prompt to display

        Returns:
            User input string
        """
        return input(prompt).strip()

    def get_move_input(self, examples: str) -> str:
        """
        Get move input from user.

        Args:
            examples: Example moves to show

        Returns:
            User input string
        """
        print("\n" + "─" * 60)
        prompt = (
            f"Movimiento DESDE-HASTA (ej: {examples})\n"
            "o 'ayuda', 'movimientos', 'reglas', 'salir': "
        )
        move_input = input(prompt).strip()
        print("─" * 60)
        return move_input

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

    def confirm_action(self, prompt: str) -> bool:
        """
        Ask user to confirm an action.

        Args:
            prompt: Confirmation prompt

        Returns:
            True if confirmed, False otherwise
        """
        response = input(prompt).strip().lower()
        return response in ["s", "sí", "si", "y", "yes"]

    def display_welcome(self) -> None:
        """Display welcome banner."""
        print("\n")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + " " * 25 + "BACKGAMMON" + " " * 43 + "║")
        print("║" + " " * 78 + "║")
        print("║" + " " * 20 + "Juego local para dos jugadores" + " " * 28 + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")

    def display_winner(self, player) -> None:
        """
        Display the winner of the game.

        Args:
            player: Player object who won
        """
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

    def display_current_player(self, player) -> None:
        """
        Display whose turn it is.

        Args:
            player: Current player object
        """
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

    def display_dice_roll(self, dice_values: List[int]) -> None:
        """
        Display the result of a dice roll.

        Args:
            dice_values: List of dice values [die1, die2]
        """
        if dice_values and len(dice_values) >= 2:
            print("\n┌─────────────────────────────┐")
            if dice_values[0] == dice_values[1]:
                print(f"│ DADOS: [ {dice_values[0]} ] [ {dice_values[1]} ] ¡DOBLE! │")
            else:
                print(f"│ DADOS: [ {dice_values[0]} ] [ {dice_values[1]} ]          │")
            print("└─────────────────────────────┘")

    def display_available_moves(self, moves: List[int]) -> None:
        """
        Display available moves to the player.

        Args:
            moves: List of available move distances
        """
        if moves:
            moves_str = ", ".join(map(str, moves))
            print(f"\nMovimientos disponibles: [ {moves_str} ]")
        else:
            print("\nNo hay movimientos disponibles")

    def display_help(self) -> None:
        """Display help information."""
        print("\n╔" + "═" * 68 + "╗")
        print("║" + " " * 24 + "AYUDA DE BACKGAMMON" + " " * 25 + "║")
        print("╠" + "═" * 68 + "╣")
        print("║  COMANDOS BÁSICOS:" + " " * 49 + "║")
        print("║  • 'desde hasta' - Realizar movimiento (ej: '12 8', '1 fuera')     ║")
        print(
            "║  • 'movimientos' - Ver todos los movimientos posibles" + " " * 14 + "║"
        )
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
            "║  • Blancas (●): puntos 1-6  |  Negras (○): puntos 19-24" + " " * 22 + "║"
        )
        print("╠" + "═" * 78 + "╣")
        print("║  MOVIMIENTO:" + " " * 65 + "║")
        print("║  • Lanza dos dados para determinar tus movimientos" + " " * 27 + "║")
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
            "║  • Golpea fichas del oponente para enviarlas a la barra" + " " * 22 + "║"
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
            "║  • No puedes mover a puntos con 2+ fichas del oponente" + " " * 23 + "║"
        )
        print("╠" + "═" * 78 + "╣")
        print("║  GANADOR:" + " " * 68 + "║")
        print("║  ¡El primer jugador en sacar todas sus fichas gana!" + " " * 26 + "║")
        print("╚" + "═" * 78 + "╝")

    def display_statistics(self, stats: Dict[str, Any]) -> None:
        """
        Display game statistics.

        Args:
            stats: Dictionary containing game statistics
        """
        if stats:
            print("\nEstadísticas del Juego:")
            print("=" * 22)
            for key, value in stats.items():
                print(f"{key.title()}: {value}")
            print("=" * 22)

    def pause(self) -> None:
        """Pause and wait for user input."""
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
