# Justificación del Diseño - Backgammon Game

## Resumen del diseño general

El proyecto implementa un juego completo de Backgammon siguiendo una arquitectura modular basada en los principios SOLID y el patrón de diseño MVC (Model-View-Controller) adaptado. El sistema se divide en tres capas principales:

### Arquitectura de tres capas:

1. **Capa de Lógica de Negocio (core/)**: Contiene las clases fundamentales del juego independientes de la interfaz de usuario:
   - `BackgammonGame`: Orquestador principal que coordina todos los componentes del juego
   - `Board`: Gestión del tablero con 24 puntos, barra y área off
   - `Player`: Representación de jugadores con gestión de fichas (15 por jugador)
   - `Checker`: Representación de fichas individuales con color y posición
   - `Dice`: Manejo de dados con detección de dobles y gestión de movimientos disponibles

2. **Capa de Interfaz de Usuario (cli/ y pygame_ui/)**: Dos interfaces independientes e intercambiables:
   - **CLI (Command Line Interface)**: 
     - Refactorizada siguiendo SOLID con 6 clases especializadas
     - `BackgammonCLI`: Coordinador principal
     - `BoardRenderer`, `CommandParser`, `InputValidator`, `GameController`, `UserInterface`: Componentes especializados
   - **Pygame UI**: Interfaz gráfica con arquitectura modular
     - `PygameUI`: Punto de entrada y control del bucle principal
     - `BackgammonBoard`: Coordinador de tablero
     - `BoardInteraction`: Manejo de interacciones del mouse
     - Sistema de renderers especializado en `renderers/`

3. **Capa de Testing (test/)**: Suite completa de 460 tests unitarios con 92% de cobertura:
   - Tests exhaustivos para cada componente utilizando unittest
   - Uso extensivo de mocks para aislamiento de dependencias
   - Testing de casos edge y validación de reglas del Backgammon

### Patrones de diseño aplicados:

- **Patrón Coordinador**: `BackgammonGame` orquesta sin implementar lógica específica
- **Patrón Strategy**: Interfaces UI intercambiables (CLI/Pygame)
- **Separation of Concerns**: Cada clase tiene una única responsabilidad clara
- **Dependency Injection**: Las clases reciben sus dependencias en el constructor
- **State Pattern**: Gestión robusta de estados del juego (inicialización, turnos, victoria)

### Flujo de datos:

```
Usuario → UI (CLI/Pygame) → BackgammonGame → Board/Player/Dice → BackgammonGame → UI → Usuario
```

El diseño permite extender el juego fácilmente con nuevas interfaces (ej: web UI) o funcionalidades (ej: IA) sin modificar el código existente, respetando el principio Open/Closed.

## Justificación de las clases elegidas (por qué, responsabilidades)

### Capa Core (backgammon/core/)

- **BackgammonGame**: Orquestador principal. Coordina Board, Players, Dice y UI. Maneja flujo de turnos, validación de movimientos y condiciones de victoria.

- **Board**: Gestiona estado del tablero (24 puntos, barra, off). Ejecuta movimientos, valida disponibilidad de puntos y calcula movimientos posibles según reglas de Backgammon.

- **Player**: Representa jugador con nombre, color y contadores de fichas (15 totales). Provee dirección de movimiento y verifica condición de victoria.

- **Checker**: Representa ficha individual con color y posición. Valida posiciones permitidas (1-24, "bar", "off") y determina si está en home board.

- **Dice**: Maneja tiradas, detecta dobles (4 movimientos) y gestiona consumo de movimientos disponibles durante el turno.

### Capa CLI (backgammon/cli/)

Refactorización SOLID de CLI monolítica original en 6 clases especializadas:

- **BackgammonCLI**: Coordinador que delega a componentes especializados.
- **BoardRenderer**: Visualización ASCII del tablero.
- **CommandParser**: Parseo y routing de comandos.
- **InputValidator**: Validación de formato de entrada.
- **GameController**: Abstracción entre CLI y BackgammonGame.
- **UserInterface**: Operaciones de I/O (print, input).

Cada clase cumple Single Responsibility Principle, facilitando testing y mantenimiento.

### Capa Pygame UI (backgammon/pygame_ui/)

- **PygameUI**: Punto de entrada, inicialización y bucle principal a 60 FPS.

- **BackgammonBoard**: Coordinador visual. Gestiona renderers, estado de selección y botones.

- **BoardInteraction**: Maneja lógica de clicks, selección de fichas y ejecución de movimientos.

- **ClickDetector**: Convierte coordenadas de mouse en posiciones lógicas del juego.

- **Button**: Componente reutilizable con estados hover/disabled.

- **Renderers (visual_renderer.py, decorative_renderer.py, board_renderer.py)**: 
  - PointRenderer, CheckerRenderer, DiceRenderer, HighlightRenderer, TextRenderer (visuales)
  - BarRenderer, SidePanelRenderer (decorativos)
  - BoardRenderer (coordinador de renderers)
  
  Separación permite modificar visualización sin afectar lógica.

- **ColorScheme y BoardDimensions**: Centralizan configuración visual (colores, posiciones). Evitan números mágicos en el código.

## Justificación de atributos (por qué se eligieron)

### BackgammonGame
- `board`, `dice`, `players`: Referencias a componentes principales. Inyección de dependencias para flexibilidad.
- `current_player_index`: Índice (0/1) en lugar de referencia directa. Facilita serialización y cambio de turnos.
- `ui`: Referencia opcional a interfaz. Permite usar el juego con o sin UI (testing).
- `move_history`: Lista de tuplas (from, to, color). Permite implementar undo/redo.
- `is_started`, `is_paused`: Flags de estado. Control del flujo del juego.
- `start_time`, `end_time`: Timestamps para estadísticas de duración.

### Board
- `points`: Lista de 24 listas (stacks de Checker). Estructura simple que refleja el tablero físico.
- `bar`: Dict con keys "white"/"black". Separación por color para acceso directo.
- `off`: Dict con keys "white"/"black". Fichas sacadas del juego por color.

Justificación: Uso de listas y diccionarios básicos facilita serialización, debugging y visualización del estado.

### Player
- `name`: String identificador. Para mensajes de UI.
- `_color`: Atributo privado con property. Validación obligatoria en setter.
- `checkers_on_board`, `checkers_off_board`, `checkers_on_bar`: Contadores enteros. Mantienen invariante (suma = 15).
- `VALID_COLORS`: Constante de clase. Previene errores de typo en strings.

Justificación: Separación de contadores evita recorrer todo el tablero para obtener estado del jugador.

### Checker
- `color`: String "white"/"black". Identifica propietario.
- `position`: Union[int, str, None]. Flexible para representar cualquier ubicación (1-24, "bar", "off", None).
- `VALID_COLORS`, `VALID_POSITIONS`: Constantes de clase. Validación y documentación.

Justificación: Posición None permite representar fichas no inicializadas. Type hints Union documentan valores permitidos.

### Dice
- `last_roll`: List[int] o None. Guarda última tirada para referencia.
- `values`: List[int]. Movimientos disponibles actuales (2 normales, 4 en dobles).

Justificación: Separar `last_roll` (histórico) de `values` (consumibles) permite ver tirada original mientras se consumen movimientos.

### CLI Components
- **BackgammonCLI**: Instancias de 5 componentes especializados. Composición sobre herencia.
- **BoardRenderer**: Sin atributos de estado. Stateless facilita testing.
- **CommandParser**: Constante `SPECIAL_COMMANDS`. Lista centralizada de comandos.
- **InputValidator**: Sin estado. Funciones puras de validación.
- **GameController**: Referencia a `game`. Patrón Facade.
- **UserInterface**: Sin estado persistente. Solo I/O.

Justificación: Clases stateless son más fáciles de testear y thread-safe.

### Pygame UI Components
- **PygameUI**: `screen`, `clock`, `running`. Estado mínimo del bucle principal.
- **BackgammonBoard**: Referencias a renderers, `selected_point`, `valid_destinations`. Estado de selección UI separado de lógica.
- **BoardInteraction**: `selected_point`, `selected_bar`, `valid_move_destinations`. Estado de interacción independiente.
- **Button**: `rect`, `enabled`, `is_hover`. Estado visual del componente.

Justificación: Estado UI separado de estado del juego permite desincronización temporal sin afectar lógica del juego.

## Decisiones de diseño relevantes

### 1. Sistema de Coordenadas Dual
**Decisión**: Mantener dos sistemas de coordenadas diferentes:
- **Interno (Board)**: 0-23 (índices de array)
- **Usuario (UI)**: 1-24 (notación Backgammon estándar)

**Justificación**: Los usuarios esperan notación 1-24 tradicional, pero internamente los arrays 0-indexed son más naturales en Python. La conversión se hace en la capa UI, manteniendo la lógica core limpia.

### 2. Dirección de Movimiento
**Decisión**: White se mueve de 24→1 (descendente), Black de 1→24 (ascendente).

**Justificación**: Refleja la disposición estándar del Backgammon físico. La dirección se calcula dinámicamente según el color del jugador, no hardcodeada en cada movimiento.

### 3. Inyección de Dependencias
**Decisión**: BackgammonGame recibe UI como parámetro opcional en constructor.

**Justificación**: Permite testing sin UI y cambiar interfaz en runtime. Inversión de dependencias: el core no depende de UI concreta.

### 4. Refactorización CLI con SOLID
**Decisión**: Dividir CLI monolítica en 6 clases especializadas (v0.8.0).

**Justificación**: 
- CLI original tenía múltiples responsabilidades (renderizado, parsing, validación, I/O)
- Difícil de testear y mantener
- Nueva arquitectura permite cambiar cualquier componente sin afectar otros
- Facilita testing unitario con mocks

### 5. Gestión de Movimientos con Dados
**Decisión**: Dice mantiene lista de movimientos disponibles que se consumen uno a uno.

**Justificación**: Permite validar antes de ejecutar y soporta regla de dobles (4 movimientos) sin lógica especial. BackgammonGame calcula distancia y consume el dado correspondiente.

### 6. Separación de Renderers en Pygame
**Decisión**: Un renderer especializado por tipo de elemento visual.

**Justificación**: Cada renderer es independiente y testeable. Agregar nuevos elementos (ej: animaciones) no requiere modificar renderers existentes. Sigue Open/Closed Principle.

### 7. Estado de Juego Serializable
**Decisión**: get_state() / set_state() en todas las clases principales.

**Justificación**: Permite save/load de partidas, undo/redo y debugging. Uso de estructuras simples (dict, list) facilita JSON serialization.

### 8. Validación en Capas
**Decisión**: Triple validación de movimientos:
1. InputValidator: formato sintáctico
2. BackgammonGame.is_valid_move(): lógica del juego
3. Board.is_point_available(): reglas del tablero

**Justificación**: Separación de concerns. Cada capa valida su dominio. Mejora mensajes de error y facilita debugging.

### 9. Uso de Type Hints Completos
**Decisión**: Type hints en todas las funciones y métodos (PEP 484).

**Justificación**: Documentación viva, detección temprana de errores con mypy, mejor autocompletado en IDEs. Union types documentan valores especiales ("bar", "off").

### 10. Testing con Mocks Extensivos
**Decisión**: Uso de unittest.mock para aislar dependencias en tests.

**Justificación**: Tests determinísticos y rápidos. Random en Dice no afecta tests. I/O mockeado permite testing sin interacción humana. Pygame mockeado evita dependencias gráficas.

### 11. Consolidación de Renderers (v0.7.2)
**Decisión**: Reducir de 9 archivos a 3 (visual_renderer.py, decorative_renderer.py, board_renderer.py).

**Justificación**: Estructura anterior era over-engineering para proyecto académico. Mantiene separación de clases pero reduce complejidad de navegación. Balance entre SOLID y simplicidad.

### 12. Invariante de 15 Fichas
**Decisión**: Player mantiene contadores separados que siempre suman 15.

**Justificación**: Permite validar estado del juego sin recorrer tablero completo. Facilita detección de bugs. Separación hace código más legible que un único contador.

## Excepciones y manejo de errores (qué excepciones definidas y por qué)

### Excepciones Estándar Utilizadas

El proyecto no define excepciones customizadas, utilizando excepciones estándar de Python para simplicidad:

#### ValueError
Usado para errores de valor/estado inválido:
- **Player.set_color()**: Color no válido (debe ser "white" o "black")
- **Player.move_checker_off()**: No hay fichas en tablero para mover
- **Player.move_checker_to_bar()**: No hay fichas disponibles
- **Checker.__init__()**: Color inválido en construcción
- **Checker.set_position()**: Posición string inválida (no "bar" ni "off")
- **Checker.set_position()**: Posición numérica fuera de rango (1-24)
- **CommandParser.parse_move_input()**: Formato de comando inválido

**Justificación**: ValueError es semánticamente correcto para valores que violan restricciones del dominio.

#### IndexError
Usado para acceso a índices fuera de rango:
- **Board.get_point_count()**: Índice de punto fuera de 0-23
- **Board.get_point_top_color()**: Índice de punto fuera de 0-23

**Justificación**: IndexError es la excepción estándar para índices inválidos en Python. Mantiene consistencia con listas/arrays.

#### TypeError
Usado para tipos de datos incorrectos:
- **Checker.set_position()**: Tipo que no es int ni str

**Justificación**: TypeError es apropiado cuando el tipo del argumento es incorrecto.

### Estrategia de Validación

#### 1. Fail-Fast con Validación Temprana
Las validaciones se hacen al principio de los métodos, lanzando excepciones inmediatamente. Previene estados inconsistentes.

#### 2. Validación en Setters
Propiedades con validación (ej: `Player.color` con property) aseguran que el estado nunca sea inválido.

#### 3. Validación por Capas
- **UI**: Valida formato y sintaxis (InputValidator)
- **Game**: Valida lógica y reglas del juego (BackgammonGame)
- **Board**: Valida estado del tablero (Board)

Cada capa confía en que la anterior ya validó su parte.

#### 4. Retorno de Booleanos en Lugar de Excepciones
Métodos como `Board.move_checker()` retornan `bool` en lugar de lanzar excepciones:
- `True`: Movimiento exitoso
- `False`: Movimiento inválido

**Justificación**: Movimientos inválidos son casos esperados en el flujo normal del juego, no errores excepcionales. Facilita testing y control de flujo.

#### 5. Uso de Constantes para Validación
```python
VALID_COLORS = ["white", "black"]
VALID_POSITIONS = list(range(1, 25)) + ["bar", "off"]
```

Centralizan valores permitidos, evitan typos y facilitan extensión.

### Manejo de Errores en UI

#### CLI
- Try-catch en bucle principal para manejar KeyboardInterrupt (Ctrl+C)
- Validación de entrada con reintentos automáticos
- Mensajes de error descriptivos en español

#### Pygame
- Event handling robusto (quit, keyboard, mouse)
- Validación silenciosa (clicks inválidos simplemente no hacen nada)
- Feedback visual en lugar de mensajes de error

**Justificación**: UI debe ser tolerante a errores del usuario, nunca crashear. Errores de usuario se manejan con feedback, no excepciones.

## Estrategias de testing y cobertura (qué se probó y por qué)

### Métricas de Testing

- **Total de tests**: 460 tests unitarios (unittest framework)
- **Cobertura global**: 92% (superando objetivo de 90%)
- **Cobertura por módulo**:
  - BackgammonGame: 89%
  - Board: 91%
  - Player: 99%
  - Checker: 94%
  - Dice: 98%
  - CLI Components: 100%
  - Pygame UI: 91%

### Metodología TDD (Test-Driven Development)

**Proceso seguido**:
1. Escribir tests que fallan (definir comportamiento esperado)
2. Implementar código mínimo para pasar tests
3. Refactorizar manteniendo tests verdes
4. Repetir

**Beneficios obtenidos**:
- Diseño guiado por casos de uso reales
- Documentación viva (tests como especificación)
- Confianza en refactorizaciones (ej: CLI v0.8.0)
- Detección temprana de bugs

### Estrategias de Testing por Componente

#### 1. Testing de Lógica Core (Board, Player, Dice, Checker)
**Qué se probó**:
- Estados iniciales y transiciones válidas
- Validaciones de entrada (valores límite, tipos incorrectos)
- Casos edge (fichas en barra, bearing off, dobles)
- Invariantes del juego (15 fichas por jugador)
- Serialización de estado (get_state/set_state)

**Técnicas**:
- Tests parametrizados para múltiples casos similares
- Mocks de Dice.roll() para tiradas determinísticas
- Fixtures para estados complejos del tablero

#### 2. Testing de BackgammonGame (Orquestador)
**Qué se probó**:
- Flujo completo de juego (inicio, turnos, victoria)
- Integración entre componentes (Board, Player, Dice, UI)
- Validación de movimientos multicapa
- Cálculo de distancias según dirección del jugador
- Consumo correcto de dados

**Técnicas**:
- Mocks de componentes para aislar lógica de orquestación
- Verificación de llamadas entre componentes (assert_called_with)
- Tests de integración end-to-end

#### 3. Testing de CLI Components
**Qué se probó**:
- BoardRenderer: Formato ASCII correcto, símbolos apropiados
- CommandParser: Parsing de todos los formatos de comando
- InputValidator: Validación de rangos y formatos
- GameController: Delegación correcta a BackgammonGame
- UserInterface: I/O correcta
- BackgammonCLI: Flujo completo de interacción

**Técnicas**:
- Mock de builtins.input() para simular entrada de usuario
- Mock de sys.stdout para capturar salida
- StringIO para verificar mensajes sin contaminar consola
- Tests de integración entre componentes CLI

#### 4. Testing de Pygame UI
**Qué se probó**:
- PygameUI: Inicialización, bucle principal, eventos
- BackgammonBoard: Coordinación de renderers y estado
- BoardInteraction: Lógica de clicks y movimientos
- ClickDetector: Conversión de coordenadas mouse→lógica
- Renderers: Llamadas correctas a pygame.draw
- Button: Estados y detección de clicks

**Técnicas**:
- Mock extensivo de pygame (display, event, Rect, Surface)
- Tests sin dependencias gráficas (CI-friendly)
- Verificación de llamadas a métodos pygame
- Simulación de eventos (QUIT, KEYDOWN, MOUSEBUTTONDOWN)

#### 5. Testing de Casos Edge
**Casos especiales probados**:
- Movimientos desde la barra
- Bearing off (sacar fichas)
- Dobles (4 movimientos en lugar de 2)
- Bloqueo de puntos (2+ fichas oponente)
- Captura de fichas solitarias
- Tablero lleno vs vacío
- Turnos sin movimientos válidos
- Fichas comprimidas (>5 en un punto)

### Uso de Mocks para Aislamiento

**unittest.mock utilizado para**:
- **Random**: Dice.roll() mockea random.randint() para tiradas predecibles
- **I/O**: input() y print() mockeados para testing sin interacción humana
- **Pygame**: Módulo completo mockeado para tests sin ventanas gráficas
- **Componentes**: Board, Player, Dice mockeados en tests de BackgammonGame

**Beneficios**:
- Tests determinísticos (sin aleatoriedad)
- Tests rápidos (sin I/O real ni gráficos)
- Aislamiento (fallo localizado en componente específico)
- CI/CD compatible (tests corren en GitHub Actions)

### Áreas no Cubiertas (8% restante)

Las líneas no cubiertas son principalmente:
- Branches de error poco comunes (casos defensivos)
- Métodos de utilidad poco usados
- Código de UI avanzado (animaciones futuras)
- Métodos deprecated mantenidos por compatibilidad

**Justificación**: 92% es cobertura excelente. El 8% restante es código de bajo riesgo o experimentación futura.

## Referencias a requisitos SOLID y cómo se cumplen

### S - Single Responsibility Principle (Principio de Responsabilidad Única)

**"Una clase debe tener una sola razón para cambiar"**

✅ **Cumplimiento demostrado**:
- **Board**: Solo gestiona estado del tablero. No renderiza, no valida input del usuario.
- **Player**: Solo mantiene estado del jugador. No ejecuta movimientos directamente.
- **Dice**: Solo maneja dados y movimientos disponibles. No decide qué movimientos hacer.
- **CLI Components**: Cada uno tiene una responsabilidad única:
  - BoardRenderer: Solo visualización
  - CommandParser: Solo parsing
  - InputValidator: Solo validación de formato
  - GameController: Solo coordinación con el juego
  - UserInterface: Solo I/O
- **Pygame Renderers**: Cada renderer dibuja un solo tipo de elemento.

**Ejemplo concreto**: La refactorización CLI (v0.8.0) dividió CLI monolítica en 6 clases, cada una con una única responsabilidad clara.

### O - Open/Closed Principle (Principio Abierto/Cerrado)

**"Abierto para extensión, cerrado para modificación"**

✅ **Cumplimiento demostrado**:
- **BackgammonGame acepta cualquier UI**: Puede trabajar con CLI, PygameUI, o futuras interfaces sin modificar su código.
- **Sistema de Renderers**: Agregar nuevo elemento visual solo requiere crear nuevo renderer, no modificar existentes.
- **CommandParser**: Nuevos comandos se agregan a lista sin modificar lógica de parsing.
- **Interfaces intercambiables**: main.py puede cambiar entre CLI y Pygame sin modificar BackgammonGame.

**Ejemplo concreto**: Agregar PygameUI no requirió cambios en BackgammonGame, solo implementar la misma interfaz que CLI.

### L - Liskov Substitution Principle (Principio de Sustitución de Liskov)

**"Objetos de subclases deben poder reemplazar objetos de la clase base"**

✅ **Cumplimiento demostrado**:
- **Cualquier UI puede sustituir otra**: CLI y PygameUI son intercambiables desde la perspectiva de BackgammonGame.
- **Herencia mínima**: El proyecto favorece composición sobre herencia, evitando problemas de sustitución.
- **Polimorfismo por duck typing**: Python permite que cualquier objeto con los métodos correctos funcione sin herencia formal.

**Nota**: El proyecto usa más composición que herencia, lo cual simplifica LSP.

### I - Interface Segregation Principle (Principio de Segregación de Interfaces)

**"Clientes no deben depender de interfaces que no usan"**

✅ **Cumplimiento demostrado**:
- **UI mínima**: BackgammonGame solo requiere métodos `display_message()` y `display_board()` de UI. No exige métodos innecesarios.
- **GameController**: CLI no accede directamente a BackgammonGame completo, solo a métodos necesarios.
- **Renderers especializados**: Cada renderer expone solo el método `render()` necesario, no API completa.
- **ClickDetector**: Solo expone métodos de detección de clicks, no gestión completa de eventos.

**Ejemplo concreto**: PygameUI puede omitir métodos de CLI (get_player_name, get_move_input) porque BackgammonGame no los requiere.

### D - Dependency Inversion Principle (Principio de Inversión de Dependencias)

**"Depender de abstracciones, no de concreciones"**

✅ **Cumplimiento demostrado**:
- **BackgammonGame no depende de CLI concreta**: Acepta cualquier objeto UI con los métodos necesarios (duck typing).
- **CLI depende de GameController**: No accede directamente a implementación de BackgammonGame.
- **Inyección de dependencias**: Board, Player, Dice se pasan a BackgammonGame en constructor, no se crean internamente.
- **Mocks en testing**: Facilidad para mockear componentes demuestra bajo acoplamiento.

**Ejemplo concreto**:
```python
# BackgammonGame no depende de CLI concreta
def __init__(self, ui=None):  # Acepta cualquier UI
    self.ui = ui

# CLI depende de abstracción GameController
self.game_controller = GameController(game)
```

### Principios Adicionales Aplicados

#### DRY (Don't Repeat Yourself)
- ColorScheme y BoardDimensions centralizan constantes
- Métodos auxiliares reutilizables (get_direction, is_in_home_board)
- Sistema de renderers evita duplicación de código de dibujo

#### YAGNI (You Aren't Gonna Need It)
- No se implementaron funcionalidades especulativas
- Clases simples sin sobre-ingeniería
- Consolidación de renderers (v0.7.2) eliminó complejidad innecesaria

#### KISS (Keep It Simple, Stupid)
- Estructuras de datos simples (listas, diccionarios)
- Algoritmos directos sin optimizaciones prematuras
- Código legible como prioridad sobre "clever code"

### Evidencia en el Código

**Pylint Score**: 9.50/10 - demuestra adherencia a estándares de calidad y buenas prácticas.

**Test Coverage**: 92% - posible gracias a bajo acoplamiento y alta cohesión (SOLID facilita testing).

## Anexos: diagramas UML

### Diagrama de Clases - Core Module

```
┌─────────────────────────────────────────────────────────────────┐
│                        BackgammonGame                            │
├─────────────────────────────────────────────────────────────────┤
│ - board: Board                                                   │
│ - dice: Dice                                                     │
│ - players: List[Player]                                          │
│ - current_player_index: int                                      │
│ - ui: Optional[UI]                                               │
│ - is_started: bool                                               │
│ - move_history: List[Tuple]                                      │
├─────────────────────────────────────────────────────────────────┤
│ + setup_board(): None                                            │
│ + setup_players(name1, name2): None                              │
│ + start_game(): None                                             │
│ + roll_dice(): List[int]                                         │
│ + make_move(from_pos, to_pos): bool                              │
│ + is_valid_move(from_pos, to_pos): bool                          │
│ + get_possible_moves(): List[Tuple]                              │
│ + switch_turns(): None                                           │
│ + is_game_over(): bool                                           │
│ + get_winner(): Optional[Player]                                 │
└─────────────────────────────────────────────────────────────────┘
                    │
                    │ uses
                    ▼
┌──────────────────────────────┐       ┌──────────────────────────┐
│         Board                │       │        Player             │
├──────────────────────────────┤       ├──────────────────────────┤
│ - points: List[List[Checker]]│       │ - name: str              │
│ - bar: Dict[str, List]       │       │ - _color: str            │
│ - off: Dict[str, List]       │       │ - checkers_on_board: int │
├──────────────────────────────┤       │ - checkers_off_board: int│
│ + setup_initial_position()   │       │ - checkers_on_bar: int   │
│ + move_checker(from, to)     │       ├──────────────────────────┤
│ + move_from_bar(color, to)   │       │ + set_color(color)       │
│ + bear_off(from, color)      │       │ + move_checker_off()     │
│ + is_point_available()       │       │ + move_checker_to_bar()  │
│ + get_possible_moves()       │       │ + has_won(): bool        │
└──────────────────────────────┘       └──────────────────────────┘
        │ contains                               │
        │ 0..*                                   │ has 15
        ▼                                        ▼
┌──────────────────────────────┐       ┌──────────────────────────┐
│        Checker               │       │         Dice              │
├──────────────────────────────┤       ├──────────────────────────┤
│ - color: str                 │       │ - last_roll: List[int]   │
│ - position: Union[int, str]  │       │ - values: List[int]      │
├──────────────────────────────┤       ├──────────────────────────┤
│ + set_position(pos)          │       │ + roll(): List[int]      │
│ + is_on_board(): bool        │       │ + is_double(): bool      │
│ + is_on_bar(): bool          │       │ + use_move(value): bool  │
│ + is_in_home_board(): bool   │       │ + has_moves(): bool      │
└──────────────────────────────┘       │ + get_available_moves()  │
                                        └──────────────────────────┘
```

### Diagrama de Clases - CLI Module (Arquitectura SOLID)

```
┌─────────────────────────────────────────────────────────────────┐
│                      BackgammonCLI                               │
│                      (Coordinator)                               │
├─────────────────────────────────────────────────────────────────┤
│ - board_renderer: BoardRenderer                                  │
│ - command_parser: CommandParser                                  │
│ - input_validator: InputValidator                                │
│ - game_controller: GameController                                │
│ - ui: UserInterface                                              │
├─────────────────────────────────────────────────────────────────┤
│ + run_game(): None                                               │
│ + display_board(): None                                          │
│ + get_move_input(): Tuple                                        │
└─────────────────────────────────────────────────────────────────┘
           │         │         │         │         │
           │ uses    │ uses    │ uses    │ uses    │ uses
           ▼         ▼         ▼         ▼         ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
    │  Board   │ │ Command  │ │  Input   │ │   Game   │ │   User   │
    │ Renderer │ │  Parser  │ │Validator │ │Controller│ │Interface │
    └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
    │render()   │parse_move()│validate()  │make_move() │display()  │
                              Single Responsibility per Class
```

### Diagrama de Clases - Pygame UI Module

```
┌─────────────────────────────────────────────────────────────────┐
│                         PygameUI                                 │
├─────────────────────────────────────────────────────────────────┤
│ - screen: Surface                                                │
│ - clock: Clock                                                   │
│ - board: BackgammonBoard                                         │
│ - game: BackgammonGame                                           │
├─────────────────────────────────────────────────────────────────┤
│ + run_game(): None                                               │
│ + handle_events(): bool                                          │
│ + display_board(): None                                          │
└─────────────────────────────────────────────────────────────────┘
                    │ uses
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BackgammonBoard                               │
│                    (Visual Coordinator)                          │
├─────────────────────────────────────────────────────────────────┤
│ - board_renderer: BoardRenderer                                  │
│ - interaction: BoardInteraction                                  │
│ - click_detector: ClickDetector                                  │
│ - dice_button: Button                                            │
│ - selected_point: Optional[int]                                  │
├─────────────────────────────────────────────────────────────────┤
│ + render(screen): None                                           │
│ + handle_mouse_click(pos): None                                  │
│ + update_hover_state(pos): None                                  │
└─────────────────────────────────────────────────────────────────┘
        │              │                │              │
        │ uses         │ uses           │ uses         │ uses
        ▼              ▼                ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│    Board     │ │    Board     │ │    Click     │ │    Button    │
│   Renderer   │ │ Interaction  │ │   Detector   │ │              │
├──────────────┤ ├──────────────┤ ├──────────────┤ ├──────────────┤
│+ render()    │ │+ handle_     │ │+ is_point_   │ │+ render()    │
│              │ │  point_click │ │  clicked()   │ │+ is_clicked()│
└──────────────┘ │+ calculate_  │ │+ is_bar_     │ └──────────────┘
                 │  valid_dests │ │  clicked()   │
                 └──────────────┘ └──────────────┘
```

### Diagrama de Secuencia - Flujo de Movimiento

```
Usuario    CLI/UI    BackgammonGame    Board    Dice
  │          │             │            │        │
  │ input    │             │            │        │
  ├─────────>│             │            │        │
  │          │ make_move() │            │        │
  │          ├────────────>│            │        │
  │          │             │is_valid()  │        │
  │          │             ├───────────>│        │
  │          │             │<───────────┤        │
  │          │             │  true      │        │
  │          │             │            │        │
  │          │             │move_checker│        │
  │          │             ├───────────>│        │
  │          │             │<───────────┤        │
  │          │             │  success   │        │
  │          │             │            │        │
  │          │             │ use_move() │        │
  │          │             ├───────────────────>│
  │          │             │<───────────────────┤
  │          │<────────────┤  true      │        │
  │          │   true      │            │        │
  │<─────────┤             │            │        │
  │ display  │             │            │        │
```

### Diagrama de Estados - Game Flow

```
┌─────────────┐
│             │
│ NOT_STARTED │
│             │
└──────┬──────┘
       │ start_game()
       ▼
┌─────────────┐
│             │
│   PLAYING   │◄────────────────┐
│             │                 │
└──────┬──────┘                 │
       │                        │
       │ roll_dice()            │
       ▼                        │
┌─────────────┐                 │
│             │                 │
│  TURN_MOVE  │                 │
│             │                 │
└──────┬──────┘                 │
       │                        │
       │ make_move()            │
       │ [has more moves]       │
       ├────────────────────────┘
       │
       │ [no more moves]
       │ switch_turns()
       │
       │ [is_game_over()]
       ▼
┌─────────────┐
│             │
│  GAME_OVER  │
│             │
└─────────────┘
```

### Diagrama de Componentes - Arquitectura General

```
┌───────────────────────────────────────────────────────────────┐
│                         Main Entry                             │
│                         (main.py)                              │
└────────────────┬──────────────────────┬───────────────────────┘
                 │                      │
                 ▼                      ▼
┌────────────────────────┐    ┌────────────────────────┐
│      CLI Module        │    │   Pygame UI Module     │
│  (BackgammonCLI)       │    │    (PygameUI)          │
└────────┬───────────────┘    └───────┬────────────────┘
         │                            │
         │                            │
         └────────────┬───────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │     Core Module        │
         │  (BackgammonGame)      │
         └────────┬───────────────┘
                  │
         ┌────────┼────────┐
         ▼        ▼        ▼
    ┌───────┐┌───────┐┌───────┐
    │ Board ││Player ││ Dice  │
    └───────┘└───┬───┘└───────┘
                 │
                 ▼
            ┌─────────┐
            │ Checker │
            └─────────┘
```

---

**Notas sobre los diagramas**:
- Los diagramas siguen notación UML estándar adaptada a texto ASCII
- Relaciones: uses (composición), contains (agregación), has (asociación)
- Cardinalidad indicada donde es relevante (0..*, 15, etc.)
- Flechas indican dirección de dependencia