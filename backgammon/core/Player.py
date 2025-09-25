class Player:
    """
    Clase que representa un jugador del juego Backgammon.
    Maneja el estado del jugador, sus fichas y las operaciones relacionadas.
    """

    VALID_COLORS = ["white", "black"]

    def __init__(self, name=None, color=None):
        """
        Inicializa un jugador.

        Args:
          name (str, optional): Nombre del jugador
          color (str, optional): Color del jugador ("white" o "black")

        Raises:
          ValueError: Si el color no es válido
        """
        self.name = name
        self._color = None
        self.checkers_on_board = 15
        self.checkers_off_board = 0
        self.checkers_on_bar = 0

        if color is not None:
            self.set_color(color)
        else:
            self._color = color

    @property
    def color(self):
        """Getter para el color del jugador"""
        return self._color

    def set_name(self, name):
        """
        Establece el nombre del jugador.

        Args:
          name (str): Nombre del jugador
        """
        self.name = name

    def set_color(self, color):
        """
        Establece el color del jugador.

        Args:
          color (str): Color del jugador ("white" o "black")

        Raises:
          ValueError: Si el color no es válido
        """
        if color not in self.VALID_COLORS:
            raise ValueError(
                f"Invalid color: {color}. Must be one of {self.VALID_COLORS}"
            )
        self._color = color

    def move_checker_off(self):
        """
        Mueve una ficha fuera del tablero (bearing off).

        Raises:
          ValueError: Si no hay fichas en el tablero para mover
        """
        if self.checkers_on_board <= 0:
            raise ValueError("No checkers on board to move off")

        self.checkers_on_board -= 1
        self.checkers_off_board += 1

    def move_checker_to_bar(self):
        """
        Mueve una ficha del tablero a la barra.

        Raises:
          ValueError: Si no hay fichas en el tablero para mover
        """
        if self.checkers_on_board <= 0:
            raise ValueError("No checkers on board to move to bar")

        self.checkers_on_board -= 1
        self.checkers_on_bar += 1

    def move_checker_from_bar(self):
        """
        Mueve una ficha de la barra al tablero.

        Raises:
          ValueError: Si no hay fichas en la barra para mover
        """
        if self.checkers_on_bar <= 0:
            raise ValueError("No checkers on bar to move from")

        self.checkers_on_bar -= 1
        self.checkers_on_board += 1

    def has_won(self):
        """
        Verifica si el jugador ha ganado (todas las fichas fuera del tablero).

        Returns:
          bool: True si el jugador ha ganado, False en caso contrario
        """
        return (
            self.checkers_off_board == 15
            and self.checkers_on_board == 0
            and self.checkers_on_bar == 0
        )

    def has_checkers_on_bar(self):
        """
        Verifica si el jugador tiene fichas en la barra.

        Returns:
          bool: True si hay fichas en la barra, False en caso contrario
        """
        return self.checkers_on_bar > 0

    def can_bear_off(self, board):
        """
        Verifica si el jugador puede hacer bearing off.

        Args:
          board: Instancia del tablero para verificar posiciones

        Returns:
          bool: True si puede hacer bearing off, False en caso contrario
        """
        return board.all_checkers_in_home_board(self.color)

    def get_total_checkers(self):
        """
        Obtiene el total de fichas del jugador.

        Returns:
          int: Total de fichas (siempre debería ser 15)
        """
        return self.checkers_on_board + self.checkers_off_board + self.checkers_on_bar

    def get_checkers_distribution(self):
        """
        Obtiene la distribución de fichas del jugador.

        Returns:
          dict: Diccionario con la distribución de fichas
        """
        return {
            "on_board": self.checkers_on_board,
            "off_board": self.checkers_off_board,
            "on_bar": self.checkers_on_bar,
        }

    def reset(self):
        """Reinicia el estado del jugador a la posición inicial"""
        self.checkers_on_board = 15
        self.checkers_off_board = 0
        self.checkers_on_bar = 0

    def get_direction(self):
        """
        Obtiene la dirección de movimiento del jugador.

        Returns:
          int: -1 para blancas (24->1), 1 para negras (1->24)
        """
        if self.color == "white":
            return -1
        elif self.color == "black":
            return 1
        else:
            return 0

    def get_home_board_range(self):
        """
        Obtiene el rango del home board para este jugador.

        Returns:
          range: Rango de posiciones del home board
        """
        if self.color == "white":
            return range(1, 7)  # Posiciones 1-6
        elif self.color == "black":
            return range(19, 25)  # Posiciones 19-24
        else:
            return range(0, 0)  # Rango vacío si no hay color

    def get_starting_position(self):
        """
        Obtiene la posición de entrada para bearing in desde la barra.

        Returns:
          int: Posición de entrada (25 para blancas, 0 para negras)
        """
        if self.color == "white":
            return 25
        elif self.color == "black":
            return 0
        else:
            return None

    def is_valid_move(self, from_pos, to_pos, board):
        """
        Verifica si un movimiento es válido para este jugador.

        Args:
          from_pos: Posición de origen
          to_pos: Posición de destino
          board: Instancia del tablero

        Returns:
          bool: True si el movimiento es válido, False en caso contrario
        """
        return board.is_valid_move(from_pos, to_pos, self.color)

    def get_possible_moves(self, board, dice):
        """
        Obtiene los movimientos posibles para este jugador.

        Args:
          board: Instancia del tablero
          dice: Instancia de los dados

        Returns:
          list: Lista de tuplas (from_pos, to_pos) con movimientos posibles
        """
        return board.get_possible_moves(self.color, dice)

    def make_move(self, from_pos, to_pos, board):
        """
        Realiza un movimiento en el tablero.

        Args:
          from_pos: Posición de origen
          to_pos: Posición de destino
          board: Instancia del tablero

        Returns:
          bool: True si el movimiento fue exitoso, False en caso contrario
        """
        return board.move_checker(from_pos, to_pos, self.color)

    def get_opponent_color(self):
        """
        Obtiene el color del oponente.

        Returns:
          str: Color del oponente
        """
        if self.color == "white":
            return "black"
        elif self.color == "black":
            return "white"
        else:
            return None

    def copy(self):
        """
        Crea una copia del jugador.

        Returns:
          Player: Nueva instancia con el mismo estado
        """
        copied_player = Player(self.name, self.color)
        copied_player.checkers_on_board = self.checkers_on_board
        copied_player.checkers_off_board = self.checkers_off_board
        copied_player.checkers_on_bar = self.checkers_on_bar
        return copied_player

    def get_state(self):
        """
        Obtiene el estado actual del jugador.

        Returns:
          dict: Diccionario con el estado del jugador
        """
        return {
            "name": self.name,
            "color": self.color,
            "checkers_on_board": self.checkers_on_board,
            "checkers_off_board": self.checkers_off_board,
            "checkers_on_bar": self.checkers_on_bar,
        }

    def set_state(self, state):
        """
        Establece el estado del jugador.

        Args:
          state (dict): Diccionario con el estado a establecer
        """
        self.name = state.get("name")
        self._color = state.get("color")
        self.checkers_on_board = state.get("checkers_on_board", 15)
        self.checkers_off_board = state.get("checkers_off_board", 0)
        self.checkers_on_bar = state.get("checkers_on_bar", 0)

    def __str__(self):
        """
        Representación en string del jugador.

        Returns:
          str: Descripción del jugador
        """
        return f"Player: {self.name} ({self.color})"

    def __repr__(self):
        """
        Representación para debugging.

        Returns:
          str: Representación detallada del jugador
        """
        return f"Player(name='{self.name}', color='{self.color}', on_board={self.checkers_on_board}, off_board={self.checkers_off_board}, on_bar={self.checkers_on_bar})"
