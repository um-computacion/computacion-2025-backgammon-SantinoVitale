"""
Dice module for Backgammon game.

This module contains the Dice class which handles dice rolling,
double detection, and move management for the game.
"""

# pylint: disable=invalid-name  # Dice follows PascalCase class naming convention
import random


class Dice:
    """
    Clase que representa los dados del juego Backgammon.
    Maneja la tirada de dados, detección de dobles y gestión de movimientos disponibles.
    """

    def __init__(self):
        """Inicializa los dados con estado vacío"""
        self.last_roll = None
        self.values = []

    def roll_single(self):
        """
        Tira un solo dado.

        Returns:
          int: Valor entre 1 y 6
        """
        return random.randint(1, 6)

    def roll(self):
        """
        Tira ambos dados y actualiza el estado.

        Returns:
          list: Lista con los dos valores obtenidos [dado1, dado2]
        """
        die1 = self.roll_single()
        die2 = self.roll_single()
        self.last_roll = [die1, die2]
        self.values = self.get_moves(self.last_roll)
        return self.last_roll

    def is_double(self):
        """
        Verifica si la última tirada fue un doble.

        Returns:
          bool: True si ambos dados tienen el mismo valor, False en caso contrario
        """
        if self.last_roll is None:
            return False
        return self.last_roll[0] == self.last_roll[1]

    def get_moves(self, roll_values):
        """
        Obtiene los movimientos disponibles basados en la tirada.

        Args:
          roll_values (list): Lista con los valores de los dados

        Returns:
          list: Lista de movimientos disponibles
        """
        if not roll_values:
            return []

        if roll_values is None:
            return []

        if len(roll_values) == 2 and roll_values[0] == roll_values[1]:
            # Doble: 4 movimientos del mismo valor
            return [roll_values[0]] * 4
        # Tirada normal: 2 movimientos
        return list(roll_values)

    def use_move(self, move_value):
        """
        Usa/consume un movimiento disponible.

        Args:
          move_value (int): Valor del movimiento a usar

        Returns:
          bool: True si el movimiento fue usado exitosamente, False si no estaba disponible
        """
        if move_value in self.values:
            self.values.remove(move_value)
            return True
        return False

    def has_moves(self):
        """
        Verifica si hay movimientos disponibles.

        Returns:
          bool: True si hay movimientos disponibles, False en caso contrario
        """
        return len(self.values) > 0

    def can_use_move(self, move_value):
        """
        Verifica si un movimiento específico está disponible.

        Args:
          move_value (int): Valor del movimiento a verificar

        Returns:
          bool: True si el movimiento está disponible, False en caso contrario
        """
        return move_value in self.values

    def get_available_moves(self):
        """
        Obtiene la lista de movimientos disponibles.

        Returns:
          list: Copia de la lista de movimientos disponibles
        """
        return self.values.copy()

    def reset(self):
        """Reinicia el estado de los dados"""
        self.last_roll = None
        self.values = []

    def get_state(self):
        """
        Obtiene el estado actual de los dados.

        Returns:
          dict: Diccionario con el estado actual
        """
        return {"last_roll": self.last_roll, "values": self.values.copy()}

    def set_state(self, state):
        """
        Establece el estado de los dados.

        Args:
          state (dict): Diccionario con el estado a establecer
        """
        self.last_roll = state.get("last_roll")
        self.values = state.get("values", []).copy()

    def __str__(self):
        """
        Representación en string de los dados.

        Returns:
          str: Descripción de la última tirada
        """
        if self.last_roll is None:
            return "Dice: No roll yet"
        return f"Dice: {self.last_roll[0]}, {self.last_roll[1]}"

    def __repr__(self):
        """
        Representación para debugging.

        Returns:
          str: Representación detallada del estado
        """
        return f"Dice(last_roll={self.last_roll}, values={self.values})"
