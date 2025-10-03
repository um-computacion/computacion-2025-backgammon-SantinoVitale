# Automated Reports
## Coverage Report
```text
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
backgammon/core/BackgammonGame.py     219     50    77%   54-57, 87-88, 160-165, 168-173, 179, 212, 217-237, 252, 272, 277-281, 285-289, 299, 309, 468-470, 478-480, 494-495, 540
backgammon/core/Board.py              150     59    61%   113, 123, 146, 153, 185, 189, 196-197, 217, 220, 223, 245-261, 309, 328-387, 400-421, 433, 447
backgammon/core/Checker.py             78      6    92%   125, 135, 141, 151, 157, 188
backgammon/core/Dice.py                50      2    96%   69, 164
backgammon/core/Player.py              97      9    91%   182, 195, 262, 284, 299-303
backgammon/core/__init__.py             6      0   100%
-----------------------------------------------------------------
TOTAL                                 600    126    79%

```
## Pylint Report
```text
************* Module backgammon.cli.CLI
backgammon/cli/CLI.py:164:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/cli/CLI.py:562:0: C0301: Line too long (106/100) (line-too-long)
backgammon/cli/CLI.py:569:0: C0301: Line too long (101/100) (line-too-long)
backgammon/cli/CLI.py:44:4: R0915: Too many statements (54/50) (too-many-statements)
backgammon/cli/CLI.py:391:11: R1714: Consider merging these comparisons with 'in' by using 'position in ('bar', 'barra')'. Use a set instead if elements are hashable. (consider-using-in)
backgammon/cli/CLI.py:393:11: R1714: Consider merging these comparisons with 'in' by using 'position in ('off', 'fuera')'. Use a set instead if elements are hashable. (consider-using-in)
backgammon/cli/CLI.py:517:20: R1724: Unnecessary "elif" after "continue", remove the leading "el" from "elif" (no-else-continue)
backgammon/cli/CLI.py:466:8: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
backgammon/cli/CLI.py:466:8: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
backgammon/cli/CLI.py:466:8: R1702: Too many nested blocks (9/5) (too-many-nested-blocks)
backgammon/cli/CLI.py:466:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
backgammon/cli/CLI.py:441:4: R0915: Too many statements (86/50) (too-many-statements)
************* Module backgammon.core.BackgammonGame
backgammon/core/BackgammonGame.py:206:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/core/BackgammonGame.py:211:16: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:217:16: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:223:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:231:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:192:4: R0911: Too many return statements (9/6) (too-many-return-statements)
backgammon/core/BackgammonGame.py:254:4: R0911: Too many return statements (8/6) (too-many-return-statements)
************* Module backgammon.core.Board
backgammon/core/Board.py:14:0: C0301: Line too long (138/100) (line-too-long)
backgammon/core/Board.py:17:0: C0301: Line too long (111/100) (line-too-long)
backgammon/core/Board.py:331:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
backgammon/core/Board.py:317:4: R0912: Too many branches (17/12) (too-many-branches)
backgammon/core/Board.py:331:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
************* Module backgammon.test.test__BackgammonGame
backgammon/test/test__BackgammonGame.py:1:0: C0103: Module name "test__BackgammonGame" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.test.test__Player
backgammon/test/test__Player.py:1:0: C0103: Module name "test__Player" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.test.test__CLI
backgammon/test/test__CLI.py:338:0: C0303: Trailing whitespace (trailing-whitespace)
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
Your code has been rated at 9.85/10


```
