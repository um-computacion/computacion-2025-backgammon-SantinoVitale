# Always follow the SOLID principles.
# Always follow the TDD method.
# Give a detailed explanation for every prompt and document the prompt given as well as the generated response inside the prompts/prompts-desarrollo.md, prompts-documentacion.md or prompts-testing.md. Use only these files for prompting documentation.
# Place all changes on CHANGELOG.md according to the norm and place the date of the changes in English. Date in Year-Month-Day format.
# Answer always in English.

# Use consistent type hints in all functions, methods, and classes (PEP 484).
# Always add docstrings to classes and methods (PEP 257).
# Do not import libraries that are not used (avoid unnecessary imports like sys or os).
# Code must remain simple and readable: avoid over-engineering and overuse of AI-generated boilerplate.
# Follow PEP 8 style guidelines for Python code formatting.
# Program like a Junior developer, avoiding complex or advanced programming techniques.

# Testing Framework: ALWAYS use unittest (Python's built-in testing framework)
# NEVER use pytest or any other testing framework
# All test files must use unittest.TestCase as base class
# Use unittest.mock for mocking (Mock, MagicMock, patch, etc.)
# Run tests with: python -m unittest discover backgammon
# DO NOT USE ANY EMOJIS IN THE CODE OR PRINT STATEMENTS or i gonna kill you

# Versioning Rules for CHANGELOG.md

Follow these rules to determine the appropriate version number when updating CHANGELOG.md:

## Version Format: MAJOR.MINOR.PATCH (e.g., 0.1.10)

### MAJOR (0.x.x)
- Increment when: Complete system redesign, breaking API changes, or major architectural changes
- Current project is in 0.x.x (pre-release phase)
- Examples: Complete rewrite of core classes, fundamental game logic changes

### MINOR (x.1.x) 
- Increment when: New core classes implemented, new major features added, significant functionality expansion
- Reset PATCH to 0 when incrementing MINOR
- Examples: 
  - New complete class implementation (BackgammonGame, Board, Player, etc.)
  - New UI implementation (CLI, Pygame)
  - Major feature additions (save/load system, undo/redo, statistics)

### PATCH (x.x.1)
- Increment when: Improvements to existing functionality, testing enhancements, bug fixes, documentation updates
- Examples:
  - Mock implementations and testing improvements
  - Code refactoring without new features
  - Performance optimizations
  - Bug fixes and error handling improvements
  - Documentation updates and code style improvements

## Specific Guidelines for This Project:

### Always increment PATCH for:
- Adding/improving mocks in tests
- Refactoring existing code without adding features
- Performance improvements
- Code style and formatting changes
- Documentation improvements
- Bug fixes

### Increment MINOR for:
- Implementing new core classes (Dice, Player, Board, CLI, etc.)
- Adding complete new features (game statistics, save/load, etc.)
- New interface implementations (UI systems)
- Major testing framework additions

### Current Development Phase Rules:
- Stay in 0.x.x until the complete game is functional
- Consider moving to 1.0.0 when: full game implementation, all tests passing, complete documentation, and at least one working UI

## Examples from Current Project:
- 0.1.8: CLI class implementation (MINOR - new major component)
- 0.1.9: BackgammonGame class implementation (MINOR - new major component)  
- 0.1.10: Mock improvements in Dice tests (PATCH - testing enhancement)
- Next: 0.1.11 for additional mock improvements (PATCH)
- Next: 0.2.0 if implementing complete Pygame UI (MINOR - major new feature)