# Automated Reports
## Coverage Report
```text
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
backgammon/core/BackgammonGame.py     213     48    77%   54-57, 87-88, 160-165, 168-173, 179, 207-225, 238, 258, 263-267, 271-275, 285, 295, 453-455, 463-465, 479-480, 525
backgammon/core/Board.py              150     59    61%   110, 120, 143, 150, 182, 186, 193-194, 214, 217, 220, 242-258, 306, 325-381, 394-415, 427, 441
backgammon/core/Checker.py             78      7    91%   60, 125, 135, 141, 151, 157, 188
backgammon/core/Dice.py                50      2    96%   69, 164
backgammon/core/Player.py              97     11    89%   91, 182, 195, 208, 262, 284, 299-303
backgammon/core/__init__.py             6      0   100%
-----------------------------------------------------------------
TOTAL                                 594    127    79%

```
## Pylint Report
```text
************* Module backgammon.cli.CLI
backgammon/cli/CLI.py:459:50: C0303: Trailing whitespace (trailing-whitespace)
backgammon/cli/CLI.py:485:61: C0303: Trailing whitespace (trailing-whitespace)
backgammon/cli/CLI.py:510:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/cli/CLI.py:516:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/cli/CLI.py:44:4: R0915: Too many statements (54/50) (too-many-statements)
backgammon/cli/CLI.py:492:20: R1724: Unnecessary "elif" after "continue", remove the leading "el" from "elif" (no-else-continue)
backgammon/cli/CLI.py:446:8: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
backgammon/cli/CLI.py:446:8: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
backgammon/cli/CLI.py:421:4: R0915: Too many statements (70/50) (too-many-statements)
************* Module backgammon.core.BackgammonGame
backgammon/core/BackgammonGame.py:343:51: C0303: Trailing whitespace (trailing-whitespace)
backgammon/core/BackgammonGame.py:205:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/core/BackgammonGame.py:210:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:219:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:240:4: R0911: Too many return statements (8/6) (too-many-return-statements)
************* Module backgammon.core.Board
backgammon/core/Board.py:328:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
backgammon/core/Board.py:314:4: R0912: Too many branches (17/12) (too-many-branches)
backgammon/core/Board.py:328:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
************* Module backgammon.test.test__BackgammonGame
backgammon/test/test__BackgammonGame.py:257:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/test/test__BackgammonGame.py:270:0: C0301: Line too long (118/100) (line-too-long)
backgammon/test/test__BackgammonGame.py:279:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/test/test__BackgammonGame.py:285:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/test/test__BackgammonGame.py:287:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/test/test__BackgammonGame.py:293:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/test/test__BackgammonGame.py:295:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/test/test__BackgammonGame.py:299:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/test/test__BackgammonGame.py:301:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/test/test__BackgammonGame.py:1:0: C0103: Module name "test__BackgammonGame" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.test.test__Player
backgammon/test/test__Player.py:1:0: C0103: Module name "test__Player" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.test.test__CLI
backgammon/test/test__CLI.py:1:0: C0103: Module name "test__CLI" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.test.test_Board
backgammon/test/test_Board.py:1:0: C0103: Module name "test_Board" doesn't conform to snake_case naming style (invalid-name)
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
Your code has been rated at 9.83/10


```
