# Automated Reports
## Coverage Report
```text
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
backgammon/core/BackgammonGame.py     219     26    88%   164-165, 172-173, 212, 218, 237, 252, 272, 277-281, 285-289, 299, 309, 468-470, 494-495, 540
backgammon/core/Board.py              150     14    91%   120, 143, 150, 182, 186, 193-194, 214, 217, 220, 306, 336, 430, 444
backgammon/core/Checker.py             78      5    94%   125, 135, 141, 151, 157
backgammon/core/Dice.py                50      1    98%   69
backgammon/core/Player.py              97      1    99%   284
backgammon/core/__init__.py             6      0   100%
-----------------------------------------------------------------
TOTAL                                 600     47    92%

```
## Pylint Report
```text
************* Module backgammon.pygame_ui.side_panel_renderer
backgammon/pygame_ui/side_panel_renderer.py:11:0: R0903: Too few public methods (1/2) (too-few-public-methods)
************* Module backgammon.pygame_ui.point_renderer
backgammon/pygame_ui/point_renderer.py:42:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/pygame_ui/point_renderer.py:65:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
************* Module backgammon.pygame_ui.pygame
backgammon/pygame_ui/pygame.py:47:8: C0103: Attribute name "BACKGROUND_COLOR" doesn't conform to snake_case naming style (invalid-name)
backgammon/pygame_ui/pygame.py:11:0: R0902: Too many instance attributes (8/7) (too-many-instance-attributes)
backgammon/pygame_ui/pygame.py:38:8: E1101: Module 'pygame' has no 'init' member (no-member)
backgammon/pygame_ui/pygame.py:83:29: E1101: Module 'pygame' has no 'QUIT' member (no-member)
backgammon/pygame_ui/pygame.py:85:29: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
backgammon/pygame_ui/pygame.py:86:32: E1101: Module 'pygame' has no 'K_ESCAPE' member (no-member)
backgammon/pygame_ui/pygame.py:111:8: E1101: Module 'pygame' has no 'quit' member (no-member)
************* Module backgammon.pygame_ui.bar_renderer
backgammon/pygame_ui/bar_renderer.py:11:0: R0903: Too few public methods (1/2) (too-few-public-methods)
************* Module backgammon.pygame_ui.board_dimensions
backgammon/pygame_ui/board_dimensions.py:9:0: R0902: Too many instance attributes (13/7) (too-many-instance-attributes)
backgammon/pygame_ui/board_dimensions.py:102:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/pygame_ui/board_dimensions.py:124:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
************* Module backgammon.pygame_ui.board_renderer
backgammon/pygame_ui/board_renderer.py:14:0: R0903: Too few public methods (1/2) (too-few-public-methods)
************* Module backgammon.pygame_ui.color_scheme
backgammon/pygame_ui/color_scheme.py:9:0: R0903: Too few public methods (0/2) (too-few-public-methods)
************* Module backgammon.cli.CLI
backgammon/cli/CLI.py:44:4: R0914: Too many local variables (18/15) (too-many-locals)
backgammon/cli/CLI.py:44:4: R0915: Too many statements (65/50) (too-many-statements)
backgammon/cli/CLI.py:636:8: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
backgammon/cli/CLI.py:636:8: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
backgammon/cli/CLI.py:636:8: R1702: Too many nested blocks (9/5) (too-many-nested-blocks)
backgammon/cli/CLI.py:636:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
backgammon/cli/CLI.py:602:4: R0915: Too many statements (96/50) (too-many-statements)
backgammon/cli/CLI.py:14:0: R0904: Too many public methods (21/20) (too-many-public-methods)
************* Module backgammon.core.BackgammonGame
backgammon/core/BackgammonGame.py:211:16: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:217:16: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:223:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:231:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:192:4: R0911: Too many return statements (9/6) (too-many-return-statements)
backgammon/core/BackgammonGame.py:254:4: R0911: Too many return statements (8/6) (too-many-return-statements)
************* Module backgammon.core.Board
backgammon/core/Board.py:328:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
backgammon/core/Board.py:314:4: R0912: Too many branches (17/12) (too-many-branches)
backgammon/core/Board.py:328:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
************* Module backgammon.test.test__BackgammonGame
backgammon/test/test__BackgammonGame.py:1:0: C0103: Module name "test__BackgammonGame" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.test.test__Player
backgammon/test/test__Player.py:1:0: C0103: Module name "test__Player" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.test.test__CLI
backgammon/test/test__CLI.py:1:0: C0103: Module name "test__CLI" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.test.test_Board
backgammon/test/test_Board.py:1:0: C0103: Module name "test_Board" doesn't conform to snake_case naming style (invalid-name)
backgammon/test/test_Board.py:13:0: R0904: Too many public methods (30/20) (too-many-public-methods)
************* Module backgammon.test.test_Checker
backgammon/test/test_Checker.py:1:0: C0103: Module name "test_Checker" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.test.test_Dice
backgammon/test/test_Dice.py:1:0: C0103: Module name "test_Dice" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.test.__init__
backgammon/test/__init__.py:1:0: R0801: Similar lines in 2 files
==backgammon.core.Checker:[120:133]
==backgammon.core.Player:[177:190]
        if self.color == "white":
            return -1
        if self.color == "black":
            return 1
        return 0

    def get_home_board_range(self):
        """
        Obtiene el rango del home board para este jugador.

        Returns:
          range: Rango de posiciones del home board
        """ (duplicate-code)

-----------------------------------
Your code has been rated at 9.77/10


```
