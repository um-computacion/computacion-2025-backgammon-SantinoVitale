# Juego de Backgammon

### Alumno: Santino Vitale - 64006

## Prerrequisitos

1. Instalar Python 3.11+
2. Crear entorno virtual:
   ```bash
   python -m venv env
   .\env\Scripts\activate  # En Windows
   source env/bin/activate  # En macOS/Linux
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Cómo Ejecutar

### Ejecutar la aplicación

```bash
python main.py
```

Elige la opción que desees del menú interactivo:
1. Interfaz CLI
2. Interfaz Pygame
3. Salir

### Uso de CLI

La interfaz CLI proporciona una forma basada en texto para jugar Backgammon. Estos son los comandos disponibles:

- **ayuda/help**: Muestra el menú de ayuda con todos los comandos disponibles
- **reglas/rules**: Muestra las reglas del juego
- **movimientos/moves**: Muestra todos los movimientos posibles para el jugador actual
- **salir/quit**: Salir del juego

#### Cómo Realizar un Movimiento:

Ingresa los movimientos usando el formato: `POSICIÓN_ORIGEN POSICIÓN_DESTINO`

Ejemplos:
- `1 5` - Mover desde la posición 1 a la posición 5
- `barra 3` - Ingresar una ficha desde la barra a la posición 3
- `6 fuera` - Sacar una ficha desde la posición 6

#### Cómo Jugar en CLI:

1. Inicia el juego con `python main.py` y selecciona la opción 1
2. Ingresa los nombres de los jugadores cuando se te solicite
3. El juego lanzará los dados automáticamente al inicio de cada turno
4. Usa `movimientos` para ver todos los movimientos posibles
5. Ingresa tu movimiento usando el formato descrito arriba
6. Continúa hasta que todas las fichas sean sacadas del tablero

### Uso de Pygame

La interfaz Pygame proporciona una representación visual del tablero de Backgammon con controles de mouse y teclado.

#### Controles:

- **ESPACIO**: Lanzar dados
- **R**: Reiniciar juego
- **ESC**: Salir del juego
- **Click del Mouse**: Seleccionar fichas y realizar movimientos

#### Cómo Jugar en Pygame:

1. Inicia el juego con `python main.py` y selecciona la opción 2
2. Haz click en el botón "Roll Dice" o presiona ESPACIO para lanzar los dados
3. Haz click en una ficha para seleccionarla (resaltada en verde)
4. Haz click en un destino válido para mover la ficha (posiciones válidas mostradas en azul)
5. El juego cambiará de turno automáticamente cuando no haya movimientos disponibles
6. Gana sacando todas tus fichas del tablero primero

#### Indicadores Visuales:

- **Resaltado verde**: Ficha seleccionada
- **Resaltado azul**: Destinos válidos para la ficha seleccionada
- **Visualización de dados**: Muestra el lanzamiento actual y los movimientos restantes
- **Indicador de turno**: Muestra de quién es el turno
- **Mensaje de victoria**: Se muestra cuando un jugador gana