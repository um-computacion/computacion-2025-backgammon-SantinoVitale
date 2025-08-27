# Changelog

Todos los cambios se verán reflejados en este documento.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
y se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

