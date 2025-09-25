# Automated Reports
## Coverage Report
```text
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
backgammon/core/BackgammonGame.py     180     12    93%   59, 177, 238-240, 338-340, 348-350, 364-365, 410
backgammon/core/Board.py              114     25    78%   102, 112, 135, 142, 174, 178, 185-186, 206, 209, 212, 234-250, 298, 318, 332
backgammon/core/CLI.py                162     19    88%   48-53, 61, 63, 70-75, 88-93, 152-154, 250, 267-270, 287, 290-293
backgammon/core/Checker.py             78      7    91%   51, 117, 127, 134, 144, 151, 183
backgammon/core/Dice.py                50      2    96%   62, 158
backgammon/core/Player.py              97     11    89%   82, 174, 188, 202, 257, 279, 294-298
backgammon/core/__init__.py             6      0   100%
-----------------------------------------------------------------
TOTAL                                 687     76    89%

```
## Pylint Report
```text
************* Module backgammon.core.Dice
backgammon/core/Dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
backgammon/core/Dice.py:1:0: C0103: Module name "Dice" doesn't conform to snake_case naming style (invalid-name)
backgammon/core/Dice.py:64:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
************* Module backgammon.core.BackgammonGame
backgammon/core/BackgammonGame.py:1:0: C0103: Module name "BackgammonGame" doesn't conform to snake_case naming style (invalid-name)
backgammon/core/BackgammonGame.py:15:0: R0902: Too many instance attributes (12/7) (too-many-instance-attributes)
backgammon/core/BackgammonGame.py:319:4: R0911: Too many return statements (7/6) (too-many-return-statements)
backgammon/core/BackgammonGame.py:15:0: R0904: Too many public methods (25/20) (too-many-public-methods)
backgammon/core/BackgammonGame.py:6:0: W0611: Unused import copy (unused-import)
************* Module backgammon.core.Board
backgammon/core/Board.py:214:9: W0511: TODO: Agregar verificación de que todas las fichas están en home board (fixme)
backgammon/core/Board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
backgammon/core/Board.py:1:0: C0103: Module name "Board" doesn't conform to snake_case naming style (invalid-name)
backgammon/core/Board.py:16:8: C0104: Disallowed name "bar" (disallowed-name)
backgammon/core/Board.py:306:33: W0613: Unused argument 'color' (unused-argument)
backgammon/core/Board.py:306:40: W0613: Unused argument 'dice' (unused-argument)
************* Module backgammon.core.Player
backgammon/core/Player.py:316:0: C0301: Line too long (169/100) (line-too-long)
backgammon/core/Player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
backgammon/core/Player.py:1:0: C0103: Module name "Player" doesn't conform to snake_case naming style (invalid-name)
backgammon/core/Player.py:169:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/core/Player.py:183:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/core/Player.py:197:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/core/Player.py:252:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/core/Player.py:1:0: R0904: Too many public methods (22/20) (too-many-public-methods)
************* Module backgammon.core.CLI
backgammon/core/CLI.py:1:0: C0103: Module name "CLI" doesn't conform to snake_case naming style (invalid-name)
backgammon/core/CLI.py:25:8: W0107: Unnecessary pass statement (unnecessary-pass)
backgammon/core/CLI.py:27:4: R0912: Too many branches (17/12) (too-many-branches)
backgammon/core/CLI.py:213:14: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
backgammon/core/CLI.py:265:12: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/core/CLI.py:286:12: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/core/CLI.py:363:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/core/CLI.py:380:16: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/CLI.py:8:0: W0611: Unused import sys (unused-import)
************* Module backgammon.core.__init__
backgammon/core/__init__.py:6:0: C0304: Final newline missing (missing-final-newline)
************* Module backgammon.core
backgammon/core/__init__.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module backgammon.core.Checker
backgammon/core/Checker.py:1:0: C0114: Missing module docstring (missing-module-docstring)
backgammon/core/Checker.py:1:0: C0103: Module name "Checker" doesn't conform to snake_case naming style (invalid-name)
backgammon/core/Checker.py:112:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/core/Checker.py:129:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/core/Checker.py:146:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/core/Checker.py:178:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/core/Checker.py:199:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/core/Checker.py:208:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
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
==backgammon.core.Checker:[111:125]
==backgammon.core.Player:[168:182]
        if self.color == "white":
            return -1
        elif self.color == "black":
            return 1
        else:
            return 0

    def can_bear_off(self):
        """
        Verifica si la ficha puede hacer bearing off desde su posición actual.

        Returns:
          bool: True si puede hacer bearing off, False en caso contrario
        """ (duplicate-code)

-----------------------------------
Your code has been rated at 9.73/10


```
