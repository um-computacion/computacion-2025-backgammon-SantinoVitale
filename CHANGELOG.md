# Changelog

Todos los cambios se verán reflejados en este documento.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
y se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.13] - 2025-09-23

### Mejorado

- Implementación de mocks para entrada/salida y interacciones de usuario en tests de `CLI`:
  - `backgammon/test/test__CLI.py` — mejoras en testing con mocks para aislamiento de I/O incluyendo mocking de builtins.input() para simulación de entrada de usuario con validación y reintentos, sys.stdout para captura y verificación de salida de consola, Mock objects para Player attributes en testing de display methods, y StringIO para testing de output sin efectos secundarios en consola
- Estrategias de testing de interfaz implementadas:
  - Aislamiento completo de lógica de CLI sin dependencias de entrada/salida real
  - Testing determinístico de validación de entrada con múltiples intentos fallidos
  - Verificación de formato y contenido de mensajes de salida
  - Simulación controlada de objetos Player para testing de métodos de display

### Notas

- Los mocks permiten testear la lógica de CLI sin interacción humana real o efectos en consola
- Mejora significativa en testing de validación de entrada con secuencias complejas de errores
- Testing más rápido y limpio al eliminar dependencias de entrada/salida del sistema
- Validación robusta de formato de mensajes y manejo de objetos de juego
- Preparación para testing de flujos complejos de interacción usuario-sistema

## [0.1.12] - 2025-09-23

### Mejorado

- Implementación de mocks para interacciones con Board en tests de `Player`:
  - `backgammon/test/test__Player.py` — mejoras en testing con mocks para aislamiento de dependencias del tablero incluyendo mocking de Board.all_checkers_in_home_board() para testing de bearing off, Board.move_checker() para validación de movimientos de jugador, Board.get_possible_moves() para obtención de movimientos disponibles, y Board.is_valid_move() para verificación de validez de movimientos
- Estrategias de testing de componentes implementadas:
  - Aislamiento completo de lógica de Player sin dependencias del estado del Board
  - Testing determinístico de métodos de Player que requieren interacción con tablero
  - Verificación de parámetros correctos en llamadas a métodos del Board
  - Simulación de diferentes estados del tablero para testing exhaustivo

### Notas

- Los mocks permiten testear la lógica de Player independientemente del comportamiento del Board
- Mejora significativa en la cobertura de casos donde Player interactúa con Board
- Testing más rápido al eliminar la necesidad de configurar estados complejos del tablero
- Validación robusta de que Player llama correctamente a los métodos del Board
- Preparación para testing de escenarios complejos de bearing off y movimientos válidos

## [0.1.11] - 2025-09-23

### Mejorado

- Implementación de mocks para interacciones entre componentes en tests de `BackgammonGame`:
  - `backgammon/test/test__BackgammonGame.py` — mejoras en testing con mocks para aislamiento de componentes incluyendo mocking de Dice.roll() para tiradas determinísticas, Player.has_won() para testing de condiciones de victoria, Board.move_checker() para validación de lógica de movimiento, y CLI.get_move_input() para simulación de interacciones de usuario
- Estrategias de testing implementadas:
  - Aislamiento efectivo de lógica de BackgammonGame sin dependencias externas
  - Testing determinístico de flujo de juego y transiciones de estado
  - Verificación de llamadas correctas entre componentes del sistema
  - Simulación controlada de escenarios de juego específicos

### Notas

- Los mocks permiten testear la lógica orquestadora sin depender del comportamiento de componentes
- Mejora en la velocidad de ejecución de tests al eliminar operaciones complejas
- Cobertura más completa de casos edge y condiciones específicas de juego
- Validación robusta de las interacciones entre BackgammonGame y otros componentes
- Base sólida para expansión de mocks en Player, Board, CLI y otros componentes

## [0.1.10] - 2025-09-23

### Mejorado

- Implementación de mocks avanzados en tests de `Dice`:
  - `backgammon/test/test_Dice.py` — mejoras en testing con mocks para casos determinísticos incluyendo testing de todas las combinaciones de dobles, secuencias de tiradas consecutivas, valores límite (boundary values), patrones de uso de movimientos con dobles, y verificación de actualización de estado con entradas conocidas
- Análisis y recomendaciones de testing implementadas:
  - Cobertura mejorada de edge cases con resultados predecibles
  - Testing determinístico para lógica de manejo de dobles
  - Verificación robusta de gestión de estado interno
  - Aislamiento de lógica de negocio de la aleatoriedad

### Notas

- Los mocks permiten testing confiable y reproducible de la lógica de dados
- Mejora significativa en la cobertura de casos edge sin dependencia de randomness
- Tests más rápidos y determinísticos para validación de lógica de negocio
- Separación clara entre testing de lógica y testing de comportamiento aleatorio
- Preparación para expansión de mocks en otros componentes del sistema

## [0.1.9] - 2025-09-11

### Agregado

- Implementación completa de la clase `BackgammonGame`:
  - `backgammon/core/BackgammonGame.py` — clase principal orquestadora del Backgammon incluyendo gestión completa del flujo de juego, coordinación de componentes (Board, Players, Dice, UI), manejo de turnos, validación de movimientos, condiciones de victoria, save/load de estado, estadísticas, sistema undo/redo, pausa/reanudación, soporte multi-UI (CLI/Pygame) y gestión avanzada de estado
- Configuración de módulos Python actualizada:
  - `backgammon/core/__init__.py` — agregado import de las clases BackgammonGame y PygameUI para el módulo core

### Notas

- La implementación de `BackgammonGame` pasa todos los tests TDD (36/36 tests OK)
- Clase diseñada siguiendo principios SOLID como orquestador principal del juego
- Integración completa con todos los componentes existentes (Board, Player, Dice, CLI)
- Sistema robusto de gestión de estado con serialización completa
- Soporte para múltiples interfaces de usuario (CLI/Pygame)
- Funcionalidades avanzadas: undo/redo, estadísticas, pausa/reanudación
- Compatible con metodología TDD y arquitectura modular establecida

## [0.1.8] - 2025-09-11

### Agregado

- Implementación completa de la clase `CLI`:
  - `backgammon/core/CLI.py` — clase completamente funcional para interfaz de línea de comandos del Backgammon incluyendo visualización ASCII del tablero, entrada de movimientos del usuario, validaciones, manejo de mensajes/errores, confirmaciones, ayuda, reglas del juego, estadísticas y flujo de juego
- Configuración de módulos Python actualizada:
  - `backgammon/core/__init__.py` — agregado import de la clase CLI para el módulo core

### Notas

- La implementación de `CLI` pasa todos los tests TDD (31/31 tests OK)
- Clase diseñada siguiendo principios SOLID con responsabilidades bien separadas
- Interfaz robusta con validación de entrada y reintentos automáticos
- Soporte completo para visualización del tablero en formato ASCII
- Manejo de casos especiales (bar, off, dobles, bearing off)
- Sistema de ayuda y reglas integrado
- Compatible con el resto del sistema del juego

## [0.1.7]

### Agregado

- Implementación completa de la clase `Board`:
  - `backgammon/core/Board.py` — clase completamente funcional para manejo del tablero del Backgammon incluyendo 24 puntos, barra, área off, movimientos de fichas, capturas, bearing off, posición inicial estándar y manejo de estado
- Implementación completa de la clase `Checker`:
  - `backgammon/core/Checker.py` — clase completamente funcional para representar fichas individuales del Backgammon incluyendo color, posición, validaciones, movimientos especiales (bar/off), lógica del home board, bearing off, direcciones de juego y operaciones de copia
- Implementación completa de la clase `Player`:
  - `backgammon/core/Player.py` — clase completamente funcional para manejo de jugadores del Backgammon incluyendo gestión de fichas, validaciones de color, movimientos entre tablero/barra/off, condiciones de victoria, direcciones de juego y estado persistente
- Implementación completa de la clase `Dice`:
  - `backgammon/core/Dice.py` — clase completamente funcional para manejo de dados del Backgammon incluyendo tiradas, detección de dobles, gestión de movimientos disponibles, estado persistente y representaciones string
- Tests completos para la clase principal del juego:
  - `backgammon/tests/test__BackgammonGame.py` — tests completos para la clase `BackgammonGame` incluyendo inicialización, setup de juego, lógica de turnos, movimientos, condiciones de victoria, manejo de estado, guardado/carga y estadísticas
- Configuración de módulos Python:
  - `backgammon/__init__.py` — archivo de inicialización del paquete backgammon
  - `backgammon/core/__init__.py` — imports de las clases Dice, Player, Board y Checker para el módulo core

### Cambiado

- Estructura de módulos mejorada para permitir imports correctos entre paquetes

### Notas

- La implementación de `Checker` pasa todos los tests TDD (24/24 tests OK)
- La implementación de `Board` pasa todos los tests TDD (14/14 tests OK)
- La implementación de `Player` pasa todos los tests TDD (30/30 tests OK)
- La implementación de `Dice` pasa todos los tests TDD (27/27 tests OK)
- Clases diseñadas siguiendo principios SOLID y buenas prácticas de Python
- Compatible tanto para CLI como para interfaces Pygame
- Incluye manejo de estado completo para guardar/cargar partidas
- Invariante de 15 fichas por jugador mantenido en todas las operaciones
- Posición inicial estándar del Backgammon implementada (30 fichas totales)
- Incluye manejo de estado completo para guardar/cargar partidas
- Invariante de 15 fichas por jugador mantenido en todas las operaciones

## [0.1.6] - 2025-09-04

### Agregado

- Tests completos para las clases de interfaz y lógica del juego:
  - `backgammon/tests/test_Board.py` — tests completos para la clase `Board` incluyendo inicialización del tablero, movimientos de fichas, gestión de la barra, bearing off, validaciones de movimientos y manejo de estado
  - `backgammon/tests/test__CLI.py` — tests completos para la clase `CLI` incluyendo entrada de usuario, validaciones, visualización del tablero, manejo de mensajes, confirmaciones y navegación del juego
  - `backgammon/tests/test__PygameUI.py` — tests completos para la clase `PygameUI` incluyendo inicialización de Pygame, renderizado visual, manejo de eventos, detección de colisiones, animaciones y efectos de audio

### Cambiado

- Tests existentes mejorados para seguir principios TDD más estrictos
- Uso extensivo de mocks para aislar dependencias externas (pygame, input/output)
- Implementación de indentación de 2 espacios consistente en todos los archivos de test

### Notas

- Los tests de `Board` cubren toda la lógica del tablero incluyendo casos edge como movimientos inválidos y posiciones especiales
- Los tests de `CLI` incluyen validación robusta de entrada de usuario con reintentos y manejo de errores
- Los tests de `PygameUI` utilizan mocks extensivos para pygame, permitiendo testing sin dependencias gráficas
- Cobertura de tests diseñada para alcanzar aproximadamente 90% cuando las clases estén implementadas
- Todos los tests fallarán inicialmente siguiendo metodología TDD hasta implementar las clases correspondientes

## [0.1.5] - 2025-08-28

### Agregado

- Tests completos para las clases principales del juego:
  - `backgammon/tests/test_Dice.py` — tests completos para la clase `Dice` incluyendo tiradas, detección de dobles, gestión de movimientos disponibles y casos edge
  - `backgammon/tests/test_Checker.py` — tests completos para la clase `Checker` incluyendo posicionamiento, validaciones, movimientos especiales (bar/off) y funcionalidades del home board
  - `backgammon/tests/test_Player.py` — tests completos para la clase `Player` incluyendo gestión de fichas, condiciones de victoria, movimientos y validaciones de estado

### Cambiado

- Estructura de testing: movida la carpeta `tests/` desde la raíz del proyecto a `backgammon/tests/` para respetar el documento del proyecto.
- Tests existentes actualizados para seguir principios TDD con cobertura del ~90%
- Implementación de mocks en tests de `Player` para aislar dependencias con `Board`

### Notas

- Los tests implementados siguen principios TDD y fallarán hasta que se implementen las clases correspondientes
- Se utilizó indentación de 2 espacios en todos los tests para consistencia
- Los tests incluyen validaciones exhaustivas, casos edge y manejo de errores
- Cobertura de tests diseñada para alcanzar aproximadamente 90% cuando las clases estén implementadas

## [0.1.4] - 2025-08-27

### Agregado

- `tests/` — archivos de pruebas unitarias para las clases actuales definidas en `core/`. Los tests sirven como esqueleto inicial y cubren las responsabilidades principales de las clases presentes.
- `backgammon/subcarpeta/__init__.py` — reemplazo de los archivos sueltos en `backgammon/subcarpeta` por un `__init__.py` para que el paquete sea importable y la estructura funcione correctamente.
- Nuevos archivos de clases en `core/` añadidos (p. ej.: `Board.py`, `BackgammonGame.py`, `Player.py`, `Checker.py`, `Dice.py`). Estos archivos contienen las clases pensadas hasta el momento y sus interfaces iniciales.

### Cambiado

- `.gitignore` — corrección de exclusiones que estaban agregadas innecesariamente.

### Notas

- Los tests añadidos son iniciales y deben ampliarse y refinarse a medida que evolucionen las clases.
- El cambio en `backgammon/` es estructural (paquete) y no introduce lógica adicional.

## [0.1.1] - 2025-08-26

### Agregado

- Carpeta `documentacion/` con los siguientes archivos:
	- `documentacion/JUSTIFICACION.md` — plantilla y contenido mínimo para la justificación del diseño (resumen del diseño general, justificación de clases y atributos, decisiones de diseño, manejo de excepciones, estrategias de testing, referencias SOLID, anexos UML).
	- `documentacion/prompts-desarrollo.md` — formato para registrar prompts usados en desarrollo (modelo, prompt exacto, instrucciones de sistema, respuesta y uso).
	- `documentacion/prompts-documentacion.md` — formato para registrar prompts usados para generar documentación.
	- `documentacion/prompts-testing.md` — formato para registrar prompts usados en la fase de testing.

### Notas

- Estos archivos son documentación inicial / plantillas que acompañan la estructura del proyecto.
- No se añadieron cambios funcionales al código; se trata de material de apoyo para diseño y trazabilidad de prompts.

## [0.1.0] - 2025-08-25

### Agregado

- Estructura inicial del proyecto y carpetas solicitadas:
	- `backgammon/` (módulo principal)
		- `requirements.txt` (dependencias del proyecto)
		- `assets/` (recursos estáticos) — `assets.py`
		- `cli/` — `cli.py`
		- `core/` — `core.py`
		- `pygame_ui/` — `pygame_ui.py`
	- `documentacion/` (documentos del proyecto) — `JUSTIFICACION.md`, `prompts-*.md`
	- `tests/` (esqueleto para pruebas)

- Archivos de soporte iniciales:
	- `README.md`
	- `CHANGELOG.md` (este archivo)

### Notas

- Versión inicial que refleja sólo la creación de la estructura y archivos base.
- A medida que se añadan funcionalidades se irán documentando aquí siguiendo el formato.

