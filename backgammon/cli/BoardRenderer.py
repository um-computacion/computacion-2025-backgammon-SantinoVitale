"""
BoardRenderer class for Backgammon game.
Responsible only for board visualization logic.
"""


class BoardRenderer:
    """
    Handles board visualization for Backgammon game.

    Single Responsibility: Only handles visual representation of the board state.
    """

    def __init__(self) -> None:
        """Initialize the BoardRenderer."""

    def render_board(self, board) -> str:
        """
        Render the board state to a string representation.

        Args:
            board: Board object containing game state

        Returns:
            String representation of the board
        """
        if not board:
            return "No hay tablero disponible para mostrar"

        lines = []

        bar_white = len(board.bar.get("white", [])) if hasattr(board, "bar") else 0
        bar_black = len(board.bar.get("black", [])) if hasattr(board, "bar") else 0
        off_white = len(board.off.get("white", [])) if hasattr(board, "off") else 0
        off_black = len(board.off.get("black", [])) if hasattr(board, "off") else 0

        def get_checker(point_index: int, row: int) -> str:
            """Get single checker character at position."""
            if not hasattr(board, "points") or point_index < 0 or point_index >= 24:
                return " "
            checkers = board.points[point_index]
            if len(checkers) > row:
                if hasattr(checkers[row], "color"):
                    return "●" if checkers[row].color == "white" else "○"
            return " "

        lines.append("\n╔═══════════════════════════════════════════════════════════╗")
        lines.append("║                    TABLERO DE BACKGAMMON                  ║")
        lines.append("║  ◄── BLANCAS (●) hacia 0  |  NEGRAS (○) hacia 25 ──►      ║")
        lines.append("╠═══════════════════════════════════════════════════════════╣")

        lines.append("║ 13  14  15  16  17  18 ║BAR║ 19  20  21  22  23  24 ║ OFF ║")
        lines.append("║ ──  ──  ──  ──  ──  ── ╠═══╣ ──  ──  ──  ──  ──  ── ╠═════╣")

        for row in range(5):
            left_checkers = []
            for i in range(12, 18):
                ch = get_checker(i, row)
                left_checkers.append(f" {ch}  ")

            if row == 0:
                bar_display = f"W:{bar_white}"
            elif row == 1:
                bar_display = f"B:{bar_black}"
            else:
                bar_display = "   "

            right_checkers = []
            for i in range(18, 24):
                ch = get_checker(i, row)
                right_checkers.append(f" {ch}  ")

            if row == 0:
                off_display = f"W:{off_white:2d}"
            elif row == 1:
                off_display = f"B:{off_black:2d}"
            else:
                off_display = "    "

            lines.append(
                f"║{''.join(left_checkers)}║{bar_display}║{''.join(right_checkers)}║{off_display} ║"
            )

        lines.append("╠════════════════════════╬═══╬════════════════════════╬═════╣")

        for row in range(4, -1, -1):
            left_checkers = []
            for i in range(11, 5, -1):
                ch = get_checker(i, row)
                left_checkers.append(f" {ch}  ")

            right_checkers = []
            for i in range(5, -1, -1):
                ch = get_checker(i, row)
                right_checkers.append(f" {ch}  ")

            lines.append(
                f"║{''.join(left_checkers)}║   ║{''.join(right_checkers)}║     ║"
            )

        lines.append("║ ──  ──  ──  ──  ──  ── ╠═══╣ ──  ──  ──  ──  ──  ── ╚═════╝")
        lines.append("║ 12  11  10  09  08  07 ║BAR║ 06  05  04  03  02  01         ")
        lines.append("╚════════════════════════╩═══╩════════════════════════╝        ")

        return "\n".join(lines)

    def render_legend(self, board, current_player=None) -> str:
        """
        Render the board legend and game state.

        Args:
            board: Board object containing game state
            current_player: Current player (optional)

        Returns:
            String representation of legend
        """
        if not board:
            return ""

        lines = []

        bar_white = len(board.bar.get("white", [])) if hasattr(board, "bar") else 0
        bar_black = len(board.bar.get("black", [])) if hasattr(board, "bar") else 0
        off_white = len(board.off.get("white", [])) if hasattr(board, "off") else 0
        off_black = len(board.off.get("black", [])) if hasattr(board, "off") else 0

        lines.append("\n┌────────────────────────────────────────────────────┐")
        lines.append("│ ● = Blancas  |  ○ = Negras                         │")
        lines.append("├────────────────────────────────────────────────────┤")
        lines.append(
            f"│ BARRA → Blancas: {bar_white:2d}  |  Negras: {bar_black:2d}                 │"
        )
        lines.append(
            f"│ FUERA → Blancas: {off_white:2d}  |  Negras: {off_black:2d}                 │"
        )

        if current_player:
            try:
                player_color = (
                    "Blancas (●)" if current_player.color == "white" else "Negras (○)"
                )
                turno_text = f"{current_player.name} - {player_color}"
                padding = max(0, 51 - 9 - len(turno_text))
                lines.append(f"│ TURNO → {turno_text}{' ' * padding} │")
            except AttributeError:
                pass

        lines.append("└────────────────────────────────────────────────────┘")

        return "\n".join(lines)

    def render_possible_moves(self, moves: list, format_func) -> str:
        """
        Render possible moves display.

        Args:
            moves: List of (from_pos, to_pos) tuples
            format_func: Function to format positions

        Returns:
            String representation of possible moves
        """
        if not moves:
            return "\nNo hay movimientos válidos disponibles"

        lines = []
        lines.append("\n╔═══════════════════════════════════════════════════════╗")
        lines.append("║           MOVIMIENTOS POSIBLES                        ║")
        lines.append("╠═══════════════════════════════════════════════════════╣")

        moves_dict = {}
        for from_pos, to_pos in moves:
            from_str = format_func(from_pos)
            to_str = format_func(to_pos)
            if from_str not in moves_dict:
                moves_dict[from_str] = []
            moves_dict[from_str].append(to_str)

        for from_pos in sorted(
            moves_dict.keys(), key=lambda x: (isinstance(x, str), x)
        ):
            to_positions = ", ".join(moves_dict[from_pos])
            move_text = f"  {from_pos} → {to_positions}"
            padding = max(0, 53 - len(move_text))
            lines.append(f"║{move_text}{' ' * padding}  ║")

        lines.append("╠═══════════════════════════════════════════════════════╣")
        total_text = f"  Total: {len(moves)} movimiento(s) válido(s)"
        padding = max(0, 53 - len(total_text))
        lines.append(f"║{total_text}{' ' * padding}  ║")
        lines.append("╚═══════════════════════════════════════════════════════╝")

        return "\n".join(lines)
