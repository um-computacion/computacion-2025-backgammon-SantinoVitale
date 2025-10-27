"""
BackgammonCLI coordinator for the Backgammon game.
Acts as coordinator, delegating to specialized classes.
"""

from typing import Union
from .BoardRenderer import BoardRenderer
from .CommandParser import CommandParser
from .InputValidator import InputValidator
from .GameController import GameController
from .UserInterface import UserInterface


class BackgammonCLI:
    """
    Main CLI coordinator for Backgammon game.

    Delegates responsibilities to specialized classes following SOLID principles:
    - BoardRenderer: Board visualization
    - CommandParser: Command parsing and routing
    - InputValidator: Input validation
    - GameController: Game state management
    - UserInterface: User I/O operations
    """

    def __init__(self, game=None) -> None:
        """
        Initialize the BackgammonCLI coordinator.

        Args:
            game: BackgammonGame instance to interact with
        """
        self.board_renderer = BoardRenderer()
        self.command_parser = CommandParser()
        self.input_validator = InputValidator()
        self.game_controller = GameController(game)
        self.ui = UserInterface()

    def set_game(self, game) -> None:
        """
        Set the BackgammonGame instance.

        Args:
            game: BackgammonGame instance
        """
        self.game_controller.set_game(game)

    def display_board(self, board=None) -> None:
        """
        Display the current board state.

        Args:
            board: Board object (optional, uses game.board if not provided)
        """
        if board is None:
            board = self.game_controller.get_board()

        if not board:
            self.ui.display_message("No hay tablero disponible para mostrar")
            return

        board_display = self.board_renderer.render_board(board)
        self.ui.display(board_display)

        current_player = self.game_controller.get_current_player()
        legend = self.board_renderer.render_legend(board, current_player)
        self.ui.display(legend)

    def display_possible_moves(self) -> None:
        """Display all possible moves for the current player."""
        possible_moves = self.game_controller.get_possible_moves()

        if not possible_moves:
            self.ui.display_message("No hay movimientos válidos disponibles")
            return

        moves_display = self.board_renderer.render_possible_moves(
            possible_moves, self.ui.format_position
        )
        self.ui.display(moves_display)

    def get_move_input(self) -> tuple:
        """
        Get move input from user.

        Returns:
            Tuple of (from_position, to_position) or (command, None)
        """
        while True:
            try:
                current_player = self.game_controller.get_current_player()

                if current_player and hasattr(current_player, "color"):
                    if current_player.color == "white":
                        examples = "'12 8', '1 fuera'"
                    else:
                        examples = "'8 12', '24 fuera'"
                else:
                    examples = "'12 8', 'barra 20', '1 fuera'"

                move_input = self.ui.get_move_input(examples)

                try:
                    from_pos, to_pos = self.command_parser.parse_move_input(move_input)
                    return from_pos, to_pos
                except ValueError as e:
                    self.ui.display_error(str(e))
                    self.ui.display_message(
                        "Ejemplo: '12 8' = mover del punto 12 al punto 8"
                    )
                    self.ui.display_message(
                        "Use 'barra' para la barra y 'fuera' para sacar fichas"
                    )
                    continue

            except (ValueError, KeyboardInterrupt):
                self.ui.display_message(
                    "Entrada inválida. Por favor intente nuevamente."
                )
                continue

    def run_game(self) -> None:
        """Main game loop for CLI interface."""
        self.ui.display_welcome()

        player1_name = self.ui.get_player_name("white")
        player2_name = self.ui.get_player_name("black")

        self.game_controller.setup_game(player1_name, player2_name)

        self.ui.display_message("¡Juego iniciado! Que comience la partida...")

        while True:
            try:
                if self.game_controller.is_game_over():
                    winner = self.game_controller.get_winner()
                    self.ui.display_winner(winner)
                    break

                self.ui.clear_screen()
                self.display_board()

                current_player = self.game_controller.get_current_player()
                self.ui.display_current_player(current_player)

                if not self.game_controller.get_available_moves():
                    dice_values = self.game_controller.roll_dice()
                    if dice_values:
                        self.ui.display_dice_roll(dice_values)

                moves = self.game_controller.get_available_moves()
                if moves:
                    self.ui.display_available_moves(moves)

                if not self.game_controller.has_valid_moves():
                    self.ui.display_message(
                        "No hay movimientos válidos disponibles. Turno omitido."
                    )
                    self.game_controller.complete_turn()
                    continue

                while (
                    self.game_controller.has_moves_remaining()
                    and self.game_controller.has_valid_moves()
                ):

                    from_pos, to_pos = self.get_move_input()

                    command_type = self.command_parser.get_command_type(str(from_pos))

                    if command_type == "help":
                        self.ui.display_help()
                        continue
                    if command_type == "moves":
                        self.display_possible_moves()
                        continue
                    if command_type == "rules":
                        self.ui.display_game_rules()
                        continue
                    if command_type == "quit":
                        if self.ui.confirm_action(
                            "¿Está seguro que desea salir? (s/n): "
                        ):
                            return
                        continue

                    try:
                        if self.game_controller.make_move(from_pos, to_pos):
                            self.ui.display_message(
                                f"Movimiento realizado: {from_pos} a {to_pos}"
                            )

                            distance = self.game_controller.calculate_move_distance(
                                from_pos, to_pos
                            )
                            if distance > 0:
                                self.game_controller.use_dice_move(distance)

                            self.display_board()
                            remaining_moves = self.game_controller.get_available_moves()
                            if remaining_moves:
                                self.ui.display_available_moves(remaining_moves)
                            else:
                                self.ui.display_message("¡Todos los dados usados!")
                                break
                        else:
                            self._display_move_error(from_pos, to_pos)
                    except (ValueError, TypeError, AttributeError) as e:
                        self.ui.display_error(f"Movimiento falló: {str(e)}")

                if not self.game_controller.can_continue_turn():
                    self.game_controller.complete_turn()

            except KeyboardInterrupt:
                if self.ui.confirm_action("¿Está seguro que desea salir? (s/n): "):
                    break
            except (ValueError, TypeError, AttributeError) as e:
                self.ui.display_error(f"Error del juego: {str(e)}")
                break

        self.ui.display_message("¡Gracias por jugar!")

    def _display_move_error(
        self, from_pos: Union[int, str], to_pos: Union[int, str]
    ) -> None:
        """
        Display helpful error message for invalid move.

        Args:
            from_pos: Starting position
            to_pos: Ending position
        """
        possible_moves = self.game_controller.get_possible_moves()
        if possible_moves:
            self.ui.display_error(f"Movimiento inválido: {from_pos} a {to_pos}.")
            self.ui.display("Movimientos válidos disponibles:")
            for fp, tp in possible_moves[:5]:
                self.ui.display(f"  {fp} {tp}")
            if len(possible_moves) > 5:
                self.ui.display(f"  ... y {len(possible_moves) - 5} más")
        else:
            self.ui.display_error("No hay movimientos válidos disponibles.")
