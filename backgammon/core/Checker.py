class Checker:
    """
    Clase que representa una ficha del juego Backgammon.
    Maneja el color, posición y operaciones relacionadas con las fichas.
    """

    VALID_COLORS = ["white", "black"]
    VALID_POSITIONS = list(range(1, 25)) + ["bar", "off"]

    def __init__(self, color=None):
        """
        Inicializa una ficha con su color.

        Args:
          color (str, optional): Color de la ficha ("white" o "black")

        Raises:
          ValueError: Si el color no es válido
        """
        if color is not None and color not in self.VALID_COLORS:
            raise ValueError(
                f"Invalid color: {color}. Must be one of {self.VALID_COLORS}"
            )

        self.color = color
        self.position = None

    def set_position(self, position):
        """
        Establece la posición de la ficha.

        Args:
          position (int or str): Posición (1-24, "bar", "off")

        Raises:
          ValueError: Si la posición no es válida
          TypeError: Si el tipo de posición no es válido
        """
        # Validar tipo
        if not isinstance(position, (int, str)):
            raise TypeError(f"Position must be int or str, got {type(position)}")

        # Validar rango para enteros
        if isinstance(position, int):
            if position < 1 or position > 24:
                raise ValueError(f"Position {position} out of range (1-24)")

        # Validar strings especiales
        if isinstance(position, str):
            if position not in ["bar", "off"]:
                raise ValueError(
                    f"Invalid string position: {position}. Must be 'bar' or 'off'"
                )

        self.position = position

    def get_position(self):
        """
        Obtiene la posición actual de la ficha.

        Returns:
          int or str or None: Posición actual de la ficha
        """
        return self.position

    def is_on_board(self):
        """
        Verifica si la ficha está en el tablero (posiciones 1-24).

        Returns:
          bool: True si está en el tablero, False en caso contrario
        """
        return isinstance(self.position, int) and 1 <= self.position <= 24

    def is_on_bar(self):
        """
        Verifica si la ficha está en la barra.

        Returns:
          bool: True si está en la barra, False en caso contrario
        """
        return self.position == "bar"

    def is_off_board(self):
        """
        Verifica si la ficha está fuera del tablero.

        Returns:
          bool: True si está fuera del tablero, False en caso contrario
        """
        return self.position == "off"

    def move_to_bar(self):
        """Mueve la ficha a la barra"""
        self.position = "bar"

    def move_off_board(self):
        """Mueve la ficha fuera del tablero"""
        self.position = "off"

    def reset_position(self):
        """Reinicia la posición de la ficha"""
        self.position = None

    def get_direction(self):
        """
        Obtiene la dirección de movimiento según el color.

        Returns:
          int: -1 para blancas (24->1), 1 para negras (1->24), 0 si no hay color
        """
        if self.color == "white":
            return -1
        elif self.color == "black":
            return 1
        else:
            return 0

    def can_bear_off(self):
        """
        Verifica si la ficha puede hacer bearing off desde su posición actual.

        Returns:
          bool: True si puede hacer bearing off, False en caso contrario
        """
        if not self.is_on_board():
            return False

        if self.color == "white":
            return 1 <= self.position <= 6
        elif self.color == "black":
            return 19 <= self.position <= 24
        else:
            return False

    def is_in_home_board(self):
        """
        Verifica si la ficha está en el home board.

        Returns:
          bool: True si está en home board, False en caso contrario
        """
        if not self.is_on_board():
            return False

        if self.color == "white":
            return 1 <= self.position <= 6
        elif self.color == "black":
            return 19 <= self.position <= 24
        else:
            return False

    def copy(self):
        """
        Crea una copia de la ficha.

        Returns:
          Checker: Nueva instancia con el mismo estado
        """
        copied_checker = Checker(self.color)
        copied_checker.position = self.position
        return copied_checker

    @staticmethod
    def get_home_board_positions(color):
        """
        Obtiene las posiciones del home board para un color.

        Args:
          color (str): Color ("white" o "black")

        Returns:
          list: Lista de posiciones del home board

        Raises:
          ValueError: Si el color no es válido
        """
        if color == "white":
            return list(range(1, 7))
        elif color == "black":
            return list(range(19, 25))
        else:
            raise ValueError(f"Invalid color: {color}")

    @staticmethod
    def get_opposite_color(color):
        """
        Obtiene el color opuesto.

        Args:
          color (str): Color actual

        Returns:
          str: Color opuesto

        Raises:
          ValueError: Si el color no es válido
        """
        if color == "white":
            return "black"
        elif color == "black":
            return "white"
        else:
            raise ValueError(f"Invalid color: {color}")

    def __str__(self):
        """Representación en string de la ficha"""
        if self.position is not None:
            return f"Checker({self.color}) at {self.position}"
        else:
            return f"Checker({self.color})"

    def __repr__(self):
        """Representación para debugging"""
        return f"Checker(color='{self.color}', position={self.position})"
