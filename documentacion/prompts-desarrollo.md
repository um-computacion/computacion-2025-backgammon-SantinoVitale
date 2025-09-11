Todos los tests TDD implementados previamente pasan correctamente.

## Prompt 4

### Modelo: Claude Sonnet 4

### Prompt: 
Podrias hacer las funciones para la clase checker para el juego de Backgammon?

### Instrucciones del sistema:
- Seguir principios SOLID
- Seguir metodología TDD
- Documentar prompts en archivos específicos
- Actualizar CHANGELOG.md según normas
- Incluir 3-5 líneas de contexto al usar replace_string_in_file

### Respuesta:

Implementación completa de la clase Checker en `backgammon/core/Checker.py`:

```python
class Checker:
  """
  Clase que representa una ficha del juego Backgammon.
  Maneja el color, posición y operaciones relacionadas con las fichas.
  """
  
  VALID_COLORS = ["white", "black"]
  VALID_POSITIONS = list(range(1, 25)) + ["bar", "off"]
  
  def __init__(self, color=None):
    """Inicializa una ficha con su color con validación"""
    if color is not None and color not in self.VALID_COLORS:
      raise ValueError(f"Invalid color: {color}. Must be one of {self.VALID_COLORS}")
    self.color = color
    self.position = None
  
  def set_position(self, position):
    """Establece la posición con validaciones robustas"""
    if not isinstance(position, (int, str)):
      raise TypeError(f"Position must be int or str, got {type(position)}")
    
    if isinstance(position, int):
      if position < 1 or position > 24:
        raise ValueError(f"Position {position} out of range (1-24)")
    
    if isinstance(position, str):
      if position not in ["bar", "off"]:
        raise ValueError(f"Invalid string position: {position}")
    
    self.position = position
  
  def get_position(self):
    """Obtiene la posición actual"""
    return self.position
  
  def is_on_board(self):
    """Verifica si está en tablero (posiciones 1-24)"""
    return isinstance(self.position, int) and 1 <= self.position <= 24
  
  def is_on_bar(self):
    """Verifica si está en la barra"""
    return self.position == "bar"
  
  def is_off_board(self):
    """Verifica si está fuera del tablero"""
    return self.position == "off"
  
  def move_to_bar(self):
    """Mueve la ficha a la barra"""
    self.position = "bar"
  
  def move_off_board(self):
    """Mueve la ficha fuera del tablero"""
    self.position = "off"
  
  def reset_position(self):
    """Reinicia la posición"""
    self.position = None
  
  def get_direction(self):
    """Dirección de movimiento: -1 white, 1 black, 0 sin color"""
    if self.color == "white":
      return -1
    elif self.color == "black":
      return 1
    else:
      return 0
  
  def can_bear_off(self):
    """Verifica si puede hacer bearing off desde posición actual"""
    if not self.is_on_board():
      return False
    
    if self.color == "white":
      return 1 <= self.position <= 6
    elif self.color == "black":
      return 19 <= self.position <= 24
    else:
      return False
  
  def is_in_home_board(self):
    """Verifica si está en home board"""
    if not self.is_on_board():
      return False
    
    if self.color == "white":
      return 1 <= self.position <= 6
    elif self.color == "black":
      return 19 <= self.position <= 24
    else:
      return False
  
  def copy(self):
    """Crea una copia de la ficha"""
    copied_checker = Checker(self.color)
    copied_checker.position = self.position
    return copied_checker
  
  @staticmethod
  def get_home_board_positions(color):
    """Obtiene posiciones del home board por color"""
    if color == "white":
      return list(range(1, 7))
    elif color == "black":
      return list(range(19, 25))
    else:
      raise ValueError(f"Invalid color: {color}")
  
  @staticmethod
  def get_opposite_color(color):
    """Obtiene el color opuesto"""
    if color == "white":
      return "black"
    elif color == "black":
      return "white"
    else:
      raise ValueError(f"Invalid color: {color}")
  
  def __str__(self):
    """Representación string con posición si existe"""
    if self.position is not None:
      return f"Checker({self.color}) at {self.position}"
    else:
      return f"Checker({self.color})"
  
  def __repr__(self):
    """Representación para debugging"""
    return f"Checker(color='{self.color}', position={self.position})"
```

### Uso en el proyecto:
- Implementación completa utilizada sin modificaciones
- Todos los tests pasan exitosamente (24/24 tests OK)
- Clase completamente funcional y robusta
- Archivo: backgammon/core/Checker.py

### Principios SOLID aplicados:
- **Single Responsibility**: Checker solo maneja estado y operaciones de una ficha individual
- **Open/Closed**: Extensible para nuevas funcionalidades sin modificar código existente
- **Liskov Substitution**: Todas las instancias de Checker son intercambiables
- **Interface Segregation**: Métodos específicos y cohesivos para operaciones de fichas
- **Dependency Inversion**: No depende de implementaciones concretas

### Funcionalidades implementadas:
- Validación de colores y posiciones
- Gestión de posiciones especiales (bar, off)
- Lógica específica del Backgammon (home board, bearing off)
- Direcciones de movimiento por color
- Operaciones de copia y estado
- Métodos estáticos utilitarios
- Representaciones string robustas

### Tests ejecutados:
```
Ran 24 tests in 0.005s
OK
```
## Prompt 3

### Modelo: Claude Sonnet 4

### Prompt: 
Necesito crear la clase Dice para el juego de Backgammon hecho con python para el CLI y para jugar con Pygame. Deberia estar creado de manera que pase los test hechos previamente

### Instrucciones del sistema:
- Seguir principios SOLID
- Seguir metodología TDD
- Documentar prompts en archivos específicos
- Actualizar CHANGELOG.md según normas
- Incluir 3-5 líneas de contexto al usar replace_string_in_file

### Respuesta:

Implementación completa de la clase Dice en `backgammon/core/Dice.py`:

```python
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
    """Tira un solo dado. Returns: int: Valor entre 1 y 6"""
    return random.randint(1, 6)
  
  def roll(self):
    """Tira ambos dados y actualiza el estado. Returns: list: Lista con los dos valores obtenidos"""
    die1 = self.roll_single()
    die2 = self.roll_single()
    self.last_roll = [die1, die2]
    self.values = self.get_moves(self.last_roll)
    return self.last_roll
  
  def is_double(self):
    """Verifica si la última tirada fue un doble."""
    if self.last_roll is None:
      return False
    return self.last_roll[0] == self.last_roll[1]
  
  def get_moves(self, roll_values):
    """Obtiene los movimientos disponibles basados en la tirada."""
    if not roll_values or roll_values is None:
      return []
    
    if len(roll_values) == 2 and roll_values[0] == roll_values[1]:
      return [roll_values[0]] * 4  # Doble: 4 movimientos
    else:
      return list(roll_values)  # Tirada normal: 2 movimientos
  
  def use_move(self, move_value):
    """Usa/consume un movimiento disponible."""
    if move_value in self.values:
      self.values.remove(move_value)
      return True
    return False
  
  def has_moves(self):
    """Verifica si hay movimientos disponibles."""
    return len(self.values) > 0
  
  def can_use_move(self, move_value):
    """Verifica si un movimiento específico está disponible."""
    return move_value in self.values
  
  def get_available_moves(self):
    """Obtiene la lista de movimientos disponibles."""
    return self.values.copy()
  
  def reset(self):
    """Reinicia el estado de los dados"""
    self.last_roll = None
    self.values = []
  
  def get_state(self):
    """Obtiene el estado actual de los dados."""
    return {'last_roll': self.last_roll, 'values': self.values.copy()}
  
  def set_state(self, state):
    """Establece el estado de los dados."""
    self.last_roll = state.get('last_roll')
    self.values = state.get('values', []).copy()
  
  def __str__(self):
    """Representación en string de los dados."""
    if self.last_roll is None:
      return "Dice: No roll yet"
    return f"Dice: {self.last_roll[0]}, {self.last_roll[1]}"
  
  def __repr__(self):
    """Representación para debugging."""
    return f"Dice(last_roll={self.last_roll}, values={self.values})"
```

### Uso en el proyecto:
- Implementación completa utilizada sin modificaciones
- Todos los tests pasan exitosamente (27/27 tests OK)
- Configuración de módulos Python con archivos __init__.py
- Archivo: backgammon/core/Dice.py

### Principios SOLID aplicados:
- **Single Responsibility**: La clase Dice solo maneja la lógica de dados
- **Open/Closed**: Extensible para nuevas funcionalidades de dados
- **Liskov Substitution**: Implementa interfaz consistente
- **Interface Segregation**: Métodos específicos y cohesivos
- **Dependency Inversion**: No depende de implementaciones concretas

### Tests ejecutados:
```
Ran 27 tests in 0.008s
OK
```

Todos los tests TDD implementados previamente pasan correctamente.

## Prompt 2

### Modelo: Claude Sonnet 4

### Prompt: 
Ahora podrias crear la clase de Player para el juego de Backgammon de manera que pase los tests

### Instrucciones del sistema:
- Seguir principios SOLID
- Seguir metodología TDD
- Documentar prompts en archivos específicos
- Actualizar CHANGELOG.md según normas
- Incluir 3-5 líneas de contexto al usar replace_string_in_file

### Respuesta:

Implementación completa de la clase Player en `backgammon/core/Player.py`:

```python
class Player:
  """
  Clase que representa un jugador del juego Backgammon.
  Maneja el estado del jugador, sus fichas y las operaciones relacionadas.
  """
  
  VALID_COLORS = ["white", "black"]
  
  def __init__(self, name=None, color=None):
    """Inicializa un jugador con nombre y color opcionales"""
    self.name = name
    self._color = None
    self.checkers_on_board = 15
    self.checkers_off_board = 0
    self.checkers_on_bar = 0
    
    if color is not None:
      self.set_color(color)
    else:
      self._color = color
  
  def set_name(self, name):
    """Establece el nombre del jugador"""
    self.name = name
  
  def set_color(self, color):
    """Establece el color del jugador con validación"""
    if color not in self.VALID_COLORS:
      raise ValueError(f"Invalid color: {color}. Must be one of {self.VALID_COLORS}")
    self._color = color
  
  def move_checker_off(self):
    """Mueve una ficha fuera del tablero (bearing off)"""
    if self.checkers_on_board <= 0:
      raise ValueError("No checkers on board to move off")
    self.checkers_on_board -= 1
    self.checkers_off_board += 1
  
  def move_checker_to_bar(self):
    """Mueve una ficha del tablero a la barra"""
    if self.checkers_on_board <= 0:
      raise ValueError("No checkers on board to move to bar")
    self.checkers_on_board -= 1
    self.checkers_on_bar += 1
  
  def move_checker_from_bar(self):
    """Mueve una ficha de la barra al tablero"""
    if self.checkers_on_bar <= 0:
      raise ValueError("No checkers on bar to move from")
    self.checkers_on_bar -= 1
    self.checkers_on_board += 1
  
  def has_won(self):
    """Verifica si el jugador ha ganado"""
    return self.checkers_off_board == 15 and self.checkers_on_board == 0 and self.checkers_on_bar == 0
  
  def has_checkers_on_bar(self):
    """Verifica si hay fichas en la barra"""
    return self.checkers_on_bar > 0
  
  def can_bear_off(self, board):
    """Verifica si puede hacer bearing off"""
    return board.all_checkers_in_home_board(self.color)
  
  def get_direction(self):
    """Obtiene dirección de movimiento: -1 para white, 1 para black"""
    if self.color == "white":
      return -1
    elif self.color == "black":
      return 1
    else:
      return 0
  
  def get_home_board_range(self):
    """Obtiene rango del home board"""
    if self.color == "white":
      return range(1, 7)
    elif self.color == "black":
      return range(19, 25)
    else:
      return range(0, 0)
  
  def reset(self):
    """Reinicia estado del jugador"""
    self.checkers_on_board = 15
    self.checkers_off_board = 0
    self.checkers_on_bar = 0
  
  # Métodos adicionales: copy(), get_state(), set_state(), __str__(), __repr__()
```

### Uso en el proyecto:
- Implementación completa utilizada sin modificaciones
- Todos los tests pasan exitosamente (30/30 tests OK)
- Actualizado archivo __init__.py del módulo core
- Archivo: backgammon/core/Player.py

### Principios SOLID aplicados:
- **Single Responsibility**: La clase Player solo maneja estado y operaciones del jugador
- **Open/Closed**: Extensible para nuevas funcionalidades sin modificar código existente
- **Liskov Substitution**: Implementa interfaz consistente para todos los jugadores
- **Interface Segregation**: Métodos específicos y cohesivos
- **Dependency Inversion**: Interactúa con abstracciones (board) no implementaciones

### Tests ejecutados:
```
Ran 30 tests in 0.008s
OK
```

Todos los tests TDD implementados previamente pasan correctamente.

## Prompt 3

### Modelo: Claude Sonnet 4

### Prompt: 
Ahora podrias crear la clase Board de manera que cumpla con los test de Board para el juego Backgammon

### Instrucciones del sistema:
- Seguir principios SOLID
- Seguir metodología TDD
- Documentar prompts en archivos específicos
- Actualizar CHANGELOG.md según normas
- Incluir 3-5 líneas de contexto al usar replace_string_in_file

### Respuesta:

Implementación completa de las clases Board y Checker en `backgammon/core/Board.py` y `backgammon/core/Checker.py`:

**Clase Checker:**
```python
class Checker:
  """Clase que representa una ficha del juego Backgammon."""
  
  def __init__(self, color):
    """Inicializa una ficha con su color."""
    self.color = color
    self.position = None
```

**Clase Board:**
```python
from .Checker import Checker

class Board:
  """Clase que representa el tablero del juego Backgammon."""
  
  def __init__(self):
    """Inicializa el tablero con 24 puntos vacíos y áreas especiales"""
    self.points = [[] for _ in range(24)]  # 24 puntos del tablero
    self.bar = {"white": [], "black": []}  # Barra para fichas capturadas
    self.off = {"white": [], "black": []}  # Área fuera del tablero
  
  def setup_initial_position(self):
    """Configura la posición inicial estándar del Backgammon"""
    self.reset()
    # Posición inicial: 30 fichas totales (15 por jugador)
    self.points[0] = [Checker("white"), Checker("white")]
    self.points[5] = [Checker("black") for _ in range(5)]
    self.points[7] = [Checker("black") for _ in range(3)]
    self.points[11] = [Checker("white") for _ in range(5)]
    self.points[12] = [Checker("black") for _ in range(5)]
    self.points[16] = [Checker("white") for _ in range(3)]
    self.points[18] = [Checker("white") for _ in range(5)]
    self.points[23] = [Checker("black"), Checker("black")]
  
  def get_point_count(self, point_index):
    """Obtiene el número de fichas en un punto"""
    if point_index < 0 or point_index >= 24:
      raise IndexError(f"Point index {point_index} out of range (0-23)")
    return len(self.points[point_index])
  
  def get_point_top_color(self, point_index):
    """Obtiene el color de las fichas en un punto"""
    if point_index < 0 or point_index >= 24:
      raise IndexError(f"Point index {point_index} out of range (0-23)")
    if len(self.points[point_index]) == 0:
      return None
    return self.points[point_index][0].color
  
  def is_point_available(self, point_index, color):
    """Verifica si un punto está disponible para un color específico"""
    if point_index < 0 or point_index >= 24:
      return False
    point = self.points[point_index]
    
    # Punto vacío, mismo color, o una ficha oponente (captura)
    if len(point) == 0 or point[0].color == color:
      return True
    return len(point) == 1 and point[0].color != color
  
  def move_checker(self, from_point, to_point, color):
    """Mueve una ficha de un punto a otro"""
    # Validaciones
    if not (0 <= from_point < 24 and 0 <= to_point < 24):
      return False
    if len(self.points[from_point]) == 0:
      return False
    if self.points[from_point][-1].color != color:
      return False
    if not self.is_point_available(to_point, color):
      return False
    
    # Realizar movimiento
    checker = self.points[from_point].pop()
    
    # Capturar ficha oponente si existe
    if len(self.points[to_point]) == 1 and self.points[to_point][0].color != color:
      captured_checker = self.points[to_point].pop()
      self.bar[captured_checker.color].append(captured_checker)
    
    self.points[to_point].append(checker)
    return True
  
  def move_from_bar(self, color, to_point):
    """Mueve una ficha de la barra al tablero"""
    if len(self.bar[color]) == 0 or not self.is_point_available(to_point, color):
      return False
    
    checker = self.bar[color].pop()
    if len(self.points[to_point]) == 1 and self.points[to_point][0].color != color:
      captured_checker = self.points[to_point].pop()
      self.bar[captured_checker.color].append(captured_checker)
    
    self.points[to_point].append(checker)
    return True
  
  def bear_off(self, from_point, color):
    """Saca una ficha del tablero (bearing off)"""
    if not (0 <= from_point < 24) or len(self.points[from_point]) == 0:
      return False
    if self.points[from_point][-1].color != color:
      return False
    
    checker = self.points[from_point].pop()
    self.off[color].append(checker)
    return True
  
  def get_state(self) / set_state(self, state):
    """Métodos para guardar/cargar estado del tablero"""
  
  def reset(self):
    """Reinicia el tablero a estado vacío"""
    self.points = [[] for _ in range(24)]
    self.bar = {"white": [], "black": []}
    self.off = {"white": [], "black": []}
```

### Uso en el proyecto:
- Implementación completa utilizada sin modificaciones
- Todos los tests pasan exitosamente (14/14 tests OK)
- Actualizado archivo __init__.py del módulo core con Board y Checker
- Archivos: backgammon/core/Board.py, backgammon/core/Checker.py

### Principios SOLID aplicados:
- **Single Responsibility**: Board maneja solo lógica del tablero, Checker solo representa fichas
- **Open/Closed**: Extensible para nuevas reglas sin modificar código existente
- **Liskov Substitution**: Interfaz consistente para operaciones del tablero
- **Interface Segregation**: Métodos específicos para cada operación
- **Dependency Inversion**: Board depende de abstracción Checker

### Tests ejecutados:
```
Ran 14 tests in 0.004s
OK

 
 # #   P r o m p t   5 
 
 # # #   M o d e l o :   C l a u d e   S o n n e t   4 
 
 # # #   P r o m p t :   
 P o d r i a s   a h o r a   h a c e r   l a   c l a s e   C L I   d e   m a n e r a   q u e   c u m p l a   c o n   l o s   t e s t   d e l   j u e g o   d e   b a c k g a m m o n ? 
 
 # # #   I n s t r u c c i o n e s   d e l   s i s t e m a : 
 -   S e g u i r   p r i n c i p i o s   S O L I D 
 -   S e g u i r   m e t o d o l o g � a   T D D 
 -   D o c u m e n t a r   p r o m p t s   e n   a r c h i v o s   e s p e c � f i c o s 
 -   A c t u a l i z a r   C H A N G E L O G . m d   s e g � n   n o r m a s 
 -   I n c l u i r   3 - 5   l � n e a s   d e   c o n t e x t o   a l   u s a r   r e p l a c e _ s t r i n g _ i n _ f i l e 
 
 # # #   R e s p u e s t a : 
 
 I m p l e m e n t a c i � n   c o m p l e t a   d e   l a   c l a s e   C L I   e n   \  a c k g a m m o n / c o r e / C L I . p y \ : 
 
 L a   c l a s e   C L I   p r o v e e   u n a   i n t e r f a z   d e   l � n e a   d e   c o m a n d o s   p a r a   e l   j u e g o   d e   B a c k g a m m o n ,   s i g u i e n d o   l o s   p r i n c i p i o s   S O L I D : 
 
 * * C a r a c t e r � s t i c a s   p r i n c i p a l e s : * * 
 -   * * D i s p l a y   M e t h o d s * * :   M u e s t r a   e l   t a b l e r o ,   m e n s a j e s ,   e r r o r e s   y   e s t a d � s t i c a s 
 -   * * I n p u t   M e t h o d s * * :   O b t i e n e   m o v i m i e n t o s ,   n o m b r e s   d e   j u g a d o r e s   y   c o n f i g u r a c i o n e s 
 -   * * V a l i d a t i o n * * :   V a l i d a   e n t r a d a   d e   u s u a r i o   c o n   r e i n t e n t o s   a u t o m � t i c o s 
 -   * * F o r m a t t i n g * * :   F o r m a t e a   p o s i c i o n e s   y   e l e m e n t o s   d e l   j u e g o   c o n s i s t e n t e m e n t e 
 -   * * G a m e   F l o w * * :   M a n e j a   p a u s a s ,   c o n f i r m a c i o n e s   y   a y u d a 
 
 * * M � t o d o s   i m p l e m e n t a d o s : * * 
 -   \ d i s p l a y _ b o a r d ( ) \ :   M u e s t r a   e l   t a b l e r o   e n   f o r m a t o   A S C I I   c o n   p u n t o s   1 - 2 4 ,   b a r   y   o f f 
 -   \ g e t _ m o v e _ i n p u t ( ) \ :   O b t i e n e   m o v i m i e n t o s   d e l   u s u a r i o   c o n   v a l i d a c i � n   ( f o r m a t o :   \  
 1  
 4 \ ,   \ b a r  
 2 0 \ ,   \ 1  
 o f f \ ) 
 -   \ d i s p l a y _ m e s s a g e ( ) / d i s p l a y _ e r r o r ( ) \ :   M u e s t r a   m e n s a j e s   g e n e r a l e s   y   d e   e r r o r 
 -   \ g e t _ p l a y e r _ n a m e ( ) \ :   O b t i e n e   n o m b r e s   d e   j u g a d o r e s   c o n   v a l o r e s   p o r   d e f e c t o 
 -   \ c o n f i r m _ m o v e ( ) / c o n f i r m _ q u i t ( ) \ :   C o n f i r m a c i o n e s   d e   u s u a r i o 
 -   \ d i s p l a y _ w i n n e r ( ) / d i s p l a y _ c u r r e n t _ p l a y e r ( ) \ :   I n f o r m a c i � n   d e   e s t a d o   d e l   j u e g o 
 -   \ d i s p l a y _ d i c e _ r o l l ( ) \ :   M u e s t r a   r e s u l t a d o s   d e   d a d o s   c o n   d e t e c c i � n   d e   d o b l e s 
 -   \ d i s p l a y _ a v a i l a b l e _ m o v e s ( ) \ :   L i s t a   m o v i m i e n t o s   d i s p o n i b l e s 
 -   \ g e t _ g a m e _ m o d e ( ) / g e t _ d i f f i c u l t y ( ) \ :   S e l e c c i � n   d e   o p c i o n e s   d e   j u e g o 
 -   \ d i s p l a y _ h e l p ( ) / d i s p l a y _ g a m e _ r u l e s ( ) \ :   S i s t e m a   d e   a y u d a   y   r e g l a s 
 -   \  o r m a t _ p o s i t i o n ( ) \ :   F o r m a t e a   p o s i c i o n e s   p a r a   v i s u a l i z a c i � n 
 -   \ g e t _ v a l i d _ p o s i t i o n ( ) \ :   V a l i d a c i � n   d e   p o s i c i o n e s   c o n   r e i n t e n t o s 
 -   \ c l e a r _ s c r e e n ( ) \ :   L i m p i a   p a n t a l l a   m u l t i p l a t a f o r m a 
 -   \ p a u s e _ g a m e ( ) \ :   P a u s a   c o n   e n t r a d a   d e   u s u a r i o 
 -   \ d i s p l a y _ s t a t i s t i c s ( ) \ :   M u e s t r a   e s t a d � s t i c a s   d e l   j u e g o 
 
 * * P r i n c i p i o s   S O L I D   a p l i c a d o s : * * 
 -   * * S i n g l e   R e s p o n s i b i l i t y * * :   C a d a   m � t o d o   t i e n e   u n a   r e s p o n s a b i l i d a d   e s p e c � f i c a 
 -   * * O p e n / C l o s e d * * :   E x t e n s i b l e   p a r a   n u e v a s   f u n c i o n a l i d a d e s   d e   d i s p l a y / i n p u t 
 -   * * L i s k o v   S u b s t i t u t i o n * * :   I n t e r f a z   c o n s i s t e n t e   p a r a   t o d a s   l a s   o p e r a c i o n e s   C L I 
 -   * * I n t e r f a c e   S e g r e g a t i o n * * :   M � t o d o s   e s p e c i a l i z a d o s   p a r a   c a d a   t i p o   d e   i n t e r a c c i � n 
 -   * * D e p e n d e n c y   I n v e r s i o n * * :   C L I   n o   d e p e n d e   d e   i m p l e m e n t a c i o n e s   e s p e c � f i c a s   d e   o b j e t o s   d e l   j u e g o 
 
 * * V a l i d a c i � n   y   m a n e j o   d e   e r r o r e s : * * 
 -   V a l i d a c i � n   d e   f o r m a t o   d e   e n t r a d a   d e   m o v i m i e n t o s 
 -   R e i n t e n t o s   a u t o m � t i c o s   p a r a   e n t r a d a   i n v � l i d a 
 -   M a n e j o   d e   c a s o s   e s p e c i a l e s   ( b a r ,   o f f ,   n � m e r o s   1 - 2 4 ) 
 -   D e t e c c i � n   d e   d o b l e s   e n   d a d o s 
 -   V a l o r e s   p o r   d e f e c t o   p a r a   n o m b r e s   v a c � o s 
 
 # # #   T e s t s   e j e c u t a d o s : 
 \ \ \ 
 R a n   3 1   t e s t s   i n   0 . 0 2 4 s 
 O K 
 \ \ \ 
 
 T o d o s   l o s   3 1   t e s t s   T D D   i m p l e m e n t a d o s   p r e v i a m e n t e   p a s a n   c o r r e c t a m e n t e .  
 