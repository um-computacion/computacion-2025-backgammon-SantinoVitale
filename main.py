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
    print("             WELCOME TO BACKGAMMON GAME")
    print("=" * 60)
    print("A classic board game for two players")
    print("Developed using Python with multiple interface options")
    print("=" * 60)


def display_interface_menu() -> None:
    """Display the interface selection menu."""
    print("\nPlease choose your preferred interface:")
    print("1. CLI (Command Line Interface) - ✓ Available")
    print("2. Pygame (Graphical Interface) - ⚠️  Coming Soon")
    print("3. Exit")
    print("-" * 40)


def get_user_choice() -> str:
    """
    Get and validate user's interface choice.

    Returns:
        User's validated choice as string
    """
    while True:
        try:
            choice = input("Enter your choice (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return choice
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            sys.exit(0)


def start_cli_game() -> None:
    """Initialize and start the CLI version of the game."""
    try:
        print("\n🎮 Starting CLI Backgammon Game...")

        # Create CLI interface and game
        cli = CLI()
        game = BackgammonGame()
        cli.set_game(game)
        game.set_ui(cli)

        # Start the game using CLI
        print("\n🎲 Starting Backgammon Game!")
        print("Good luck and have fun!")
        print("=" * 50)

        # Start the game loop through CLI
        cli.run_game()

    except (EOFError, KeyboardInterrupt):
        print("\n\n🛑 Game interrupted by user")
        print("👋 Thanks for playing!")
        sys.exit(0)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"\n❌ An error occurred: {e}")
        print("Please try again or report this issue.")
        sys.exit(1)


def start_pygame_game() -> None:
    """Placeholder for Pygame interface (not yet implemented)."""
    print("\n🚧 Pygame Interface - Coming Soon!")
    print("=" * 40)
    print("The graphical interface using Pygame is currently")
    print("under development and will be available in a future update.")
    print("\nFeatures planned for Pygame interface:")
    print("• Visual board representation")
    print("• Click-to-move functionality")
    print("• Animations and sound effects")
    print("• Enhanced user experience")
    print("\nFor now, please use the CLI interface (Option 1)")
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
                print("\nWould you like to try the CLI interface instead? (y/n)")
                try:
                    retry_choice = input("Choice: ").strip().lower()
                    if retry_choice in ['y', 'yes']:
                        start_cli_game()
                        break
                    print("Returning to main menu...\n")
                    continue
                except (EOFError, KeyboardInterrupt):
                    print("\n👋 Goodbye!")
                    break

            if choice == '3':
                # Exit the application
                print("\n👋 Thanks for your interest in Backgammon!")
                print("Come back soon to play!")
                break

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please try again or report this issue.")
        sys.exit(1)


if __name__ == "__main__":
    main()
