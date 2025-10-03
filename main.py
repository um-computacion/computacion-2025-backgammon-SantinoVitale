"""
Main entry point for the Backgammon game.
Provides user interface selection and game initialization.
"""

import sys
from backgammon.core.BackgammonGame import BackgammonGame
from backgammon.cli.CLI import CLI


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
    print("2. Pygame (Interfaz Gráfica) - Próximamente")
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
            print("\n👋 Adiós!")
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
        print("\n🎲 Iniciando el juego de Backgammon!")
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
    """Placeholder for Pygame interface (not yet implemented)."""
    print("\n🚧 Pygame Interfaz - Próximamente!")
    print("=" * 40)
    print("La interfaz gráfica utilizando Pygame está actualmente")
    print("en desarrollo y estará disponible en una futura actualización.")
    print("\nCaracterísticas planeadas para la interfaz Pygame:")
    print("• Representación visual del tablero")
    print("• Funcionalidad de clic para mover")
    print("• Animaciones y efectos de sonido")
    print("• Experiencia de usuario mejorada")
    print("\nPor ahora, por favor utiliza la interfaz CLI (Opción 1)")
    print("=" * 40)


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
                # Show Pygame coming soon message
                start_pygame_game()

                # Ask if user wants to try CLI instead
                print("¿Quisieras intentar la interfaz CLI en su lugar? (y/n)")
                try:
                    retry_choice = input("Opción: ").strip().lower()
                    if retry_choice in ['y', 'yes']:
                        start_cli_game()
                        break
                    print("Regresando al menú principal...\n")
                    continue
                except (EOFError, KeyboardInterrupt):
                    print("\n👋 ¡Adiós!")
                    break

            if choice == '3':
                # Exit the application
                print("\n👋 ¡Gracias por tu interés en Backgammon!")
                print("¡Vuelve pronto para jugar!")
                break

    except KeyboardInterrupt:
        print("\n\n👋 ¡Adiós!")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"\n❌ Ocurrió un error inesperado: {e}")
        print("Por favor, intenta de nuevo o informa sobre este problema.")
        sys.exit(1)


if __name__ == "__main__":
    main()
