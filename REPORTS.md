# Automated Reports
## Coverage Report
```text
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
backgammon/core/BackgammonGame.py     219     26    88%   164-165, 172-173, 212, 218, 237, 252, 272, 277-281, 285-289, 299, 309, 468-470, 494-495, 540
backgammon/core/Board.py              150     14    91%   123, 146, 153, 185, 189, 196-197, 217, 220, 223, 309, 339, 433, 447
backgammon/core/Checker.py             78      5    94%   125, 135, 141, 151, 157
backgammon/core/Dice.py                50      1    98%   69
backgammon/core/Player.py              97      1    99%   284
backgammon/core/__init__.py             6      0   100%
-----------------------------------------------------------------
TOTAL                                 600     47    92%

```
## Pylint Report
```text
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
backgammon/core/Board.py:14:0: C0301: Line too long (138/100) (line-too-long)
backgammon/core/Board.py:17:0: C0301: Line too long (111/100) (line-too-long)
backgammon/core/Board.py:331:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
backgammon/core/Board.py:317:4: R0912: Too many branches (17/12) (too-many-branches)
backgammon/core/Board.py:331:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
************* Module backgammon.test.test__BackgammonGame
backgammon/test/test__BackgammonGame.py:584:0: C0305: Trailing newlines (trailing-newlines)
backgammon/test/test__BackgammonGame.py:1:0: C0103: Module name "test__BackgammonGame" doesn't conform to snake_case naming style (invalid-name)
backgammon/test/test__BackgammonGame.py:528:19: W0212: Access to a protected member _calculate_move_distance of a client class (protected-access)
backgammon/test/test__BackgammonGame.py:535:19: W0212: Access to a protected member _calculate_move_distance of a client class (protected-access)
backgammon/test/test__BackgammonGame.py:541:19: W0212: Access to a protected member _calculate_move_distance of a client class (protected-access)
backgammon/test/test__BackgammonGame.py:548:19: W0212: Access to a protected member _calculate_move_distance of a client class (protected-access)
backgammon/test/test__BackgammonGame.py:554:19: W0212: Access to a protected member _calculate_move_distance of a client class (protected-access)
backgammon/test/test__BackgammonGame.py:561:19: W0212: Access to a protected member _calculate_move_distance of a client class (protected-access)
************* Module backgammon.test.test__Player
backgammon/test/test__Player.py:1:0: C0103: Module name "test__Player" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.test.test__CLI
backgammon/test/test__CLI.py:338:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/test/test__CLI.py:1:0: C0103: Module name "test__CLI" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.test.test_Board
backgammon/test/test_Board.py:1:0: C0103: Module name "test_Board" doesn't conform to snake_case naming style (invalid-name)
backgammon/test/test_Board.py:214:25: W0212: Access to a protected member _can_bear_off of a client class (protected-access)
backgammon/test/test_Board.py:220:25: W0212: Access to a protected member _can_bear_off of a client class (protected-access)
backgammon/test/test_Board.py:226:25: W0212: Access to a protected member _can_bear_off of a client class (protected-access)
backgammon/test/test_Board.py:234:24: W0212: Access to a protected member _can_bear_off of a client class (protected-access)
backgammon/test/test_Board.py:242:24: W0212: Access to a protected member _can_bear_off of a client class (protected-access)
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
Your code has been rated at 9.84/10


```
