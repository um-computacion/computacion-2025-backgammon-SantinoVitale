"""
Main entry point for the Backgammon game.
Provides user interface selection and game initialization.
"""

import sys
from backgammon.core.BackgammonGame import BackgammonGame
from backgammon.cli.CLI import CLI
from backgammon.pygame_ui.pygame_ui import PygameUI


def display_welcome_message() -> None:
    """Display the welcome message and game information."""
    print("=" * 60)
    print("             Bienvenido al juego de Backgammon")
    print("=" * 60)
    print("Un juego de mesa clásico para dos jugadores")
    print("Desarrollado en Python con múltiples opciones de interfaz")
    print("=" * 60)


def display_interface_menu() -> None:
    """Display the interface selection menu."""
    print("\nPor favor, elige tu interfaz preferida:")
    print("1. CLI (Interfaz de Línea de Comandos) - ✓ Disponible")
    print("2. Pygame (Interfaz Gráfica) - ✓ Disponible")
    print("3. Salir")
    print("-" * 40)


def get_user_choice() -> str:
    """
    Get and validate user's interface choice.

    Returns:
        User's validated choice as string
    """
    while True:
        try:
            choice = input("Ingresa tu opción (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return choice
            print("Opción inválida. Por favor, ingresa 1, 2 o 3.")
        except (EOFError, KeyboardInterrupt):
            print("\nAdiós!")
            sys.exit(0)


def start_cli_game() -> None:
    """Initialize and start the CLI version of the game."""
    try:
        print("\nIniciando el juego de Backgammon en CLI...")

        # Create CLI interface and game
        cli = CLI()
        game = BackgammonGame()
        cli.set_game(game)
        game.set_ui(cli)

        # Start the game using CLI
        print("\nIniciando el juego de Backgammon!")
        print("¡Buena suerte y diviértete!")
        print("=" * 50)

        # Start the game loop through CLI
        cli.run_game()

    except (EOFError, KeyboardInterrupt):
        print("\n\nJuego interrumpido por el usuario")
        print("Gracias por jugar!")
        sys.exit(0)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"\nOcurrió un error: {e}")
        print("Por favor, intenta de nuevo o informa sobre este problema.")
        sys.exit(1)


def start_pygame_game() -> None:
    """Initialize and start the Pygame version of the game."""
    try:
        print("\nIniciando el juego de Backgammon con Pygame...")
        print("=" * 40)

        # Create Pygame interface and game
        pygame_ui = PygameUI()
        game = BackgammonGame()
        pygame_ui.set_game(game)
        game.set_ui(pygame_ui)

        # Setup players
        game.setup_players("White Player", "Black Player")

        # Setup the board with initial position
        game.setup_board()

        # DON'T roll dice automatically - let user click the button
        # game.roll_dice()  # REMOVED: User will click button to roll

        # Start the game using Pygame
        print("\nIniciando el juego de Backgammon!")
        print("¡Buena suerte y diviértete!")
        print("=" * 50)

        # Start the game loop through Pygame
        pygame_ui.run_game()

    except (EOFError, KeyboardInterrupt):
        print("\n\nJuego interrumpido por el usuario")
        print("Gracias por jugar!")
        sys.exit(0)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"\nOcurrió un error: {e}")
        print("Por favor, intenta de nuevo o informa sobre este problema.")
        sys.exit(1)


def main() -> None:
    """
    Main function to handle interface selection and game initialization.

    This function provides a menu-driven interface allowing users to choose
    between CLI and Pygame interfaces for the Backgammon game.
    """
    try:
        # Display welcome message
        display_welcome_message()

        while True:
            # Show interface selection menu
            display_interface_menu()

            # Get user choice
            choice = get_user_choice()

            if choice == '1':
                # Start CLI game
                start_cli_game()
                break

            if choice == '2':
                # Start Pygame game
                start_pygame_game()
                break

            if choice == '3':
                # Exit the application
                print("\n¡Gracias por tu interés en Backgammon!")
                print("¡Vuelve pronto para jugar!")
                break

    except KeyboardInterrupt:
        print("\n\n¡Adiós!")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"\nOcurrió un error inesperado: {e}")
        print("Por favor, intenta de nuevo o informa sobre este problema.")
        sys.exit(1)


if __name__ == "__main__":
    main()
