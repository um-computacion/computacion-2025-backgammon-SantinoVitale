# Automated Reports
## Coverage Report
```text
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
backgammon/core/BackgammonGame.py     179     12    93%   59, 177, 238-240, 338-340, 348-350, 364-365, 410
backgammon/core/Board.py              114     25    78%   109, 119, 142, 149, 181, 185, 192-193, 213, 216, 219, 241-257, 305, 325, 339
backgammon/core/CLI.py                160     19    88%   48-53, 61, 63, 70-75, 88-93, 152-154, 250, 267-269, 286, 289-291
backgammon/core/Checker.py             78      7    91%   60, 125, 135, 141, 151, 157, 188
backgammon/core/Dice.py                50      2    96%   69, 164
backgammon/core/Player.py              97     11    89%   91, 182, 195, 208, 262, 284, 299-303
backgammon/core/__init__.py             6      0   100%
-----------------------------------------------------------------
TOTAL                                 684     76    89%

```
## Pylint Report
```text
************* Module backgammon.__main__
backgammon/__main__.py:15:0: C0304: Final newline missing (missing-final-newline)
backgammon/__main__.py:12:0: C0413: Import "from main import main" should be placed at the top of the module (wrong-import-position)
************* Module backgammon.test.test__BackgammonGame
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

    def can_bear_off(self):
        """
        Verifica si la ficha puede hacer bearing off desde su posición actual.

        Returns:
          bool: True si puede hacer bearing off, False en caso contrario
        """ (duplicate-code)

-----------------------------------
Your code has been rated at 9.95/10


```
