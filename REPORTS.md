# Automated Reports
## Coverage Report
```text
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
backgammon/core/BackgammonGame.py     221     25    89%   167-168, 175-176, 224, 243, 258, 278, 283-287, 291-295, 305, 315, 474-476, 500-501, 546
backgammon/core/Board.py              150     14    91%   123, 146, 153, 185, 189, 196-197, 217, 220, 223, 309, 339, 433, 447
backgammon/core/Checker.py             78      5    94%   125, 135, 141, 151, 157
backgammon/core/Dice.py                50      1    98%   69
backgammon/core/Player.py              97      1    99%   284
backgammon/core/__init__.py             6      0   100%
-----------------------------------------------------------------
TOTAL                                 602     46    92%

```
## Pylint Report
```text
************* Module backgammon.pygame_ui.backgammon_board
backgammon/pygame_ui/backgammon_board.py:186:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/backgammon_board.py:190:0: C0301: Line too long (104/100) (line-too-long)
backgammon/pygame_ui/backgammon_board.py:195:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/backgammon_board.py:197:0: C0301: Line too long (102/100) (line-too-long)
backgammon/pygame_ui/backgammon_board.py:16:0: R0902: Too many instance attributes (8/7) (too-many-instance-attributes)
************* Module backgammon.pygame_ui.button
backgammon/pygame_ui/button.py:26:4: R0913: Too many arguments (6/5) (too-many-arguments)
backgammon/pygame_ui/button.py:26:4: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
************* Module backgammon.pygame_ui.board_dimensions
backgammon/pygame_ui/board_dimensions.py:9:0: R0902: Too many instance attributes (13/7) (too-many-instance-attributes)
backgammon/pygame_ui/board_dimensions.py:102:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/pygame_ui/board_dimensions.py:124:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
************* Module backgammon.pygame_ui.pygame_ui
backgammon/pygame_ui/pygame_ui.py:51:8: C0103: Attribute name "BACKGROUND_COLOR" doesn't conform to snake_case naming style (invalid-name)
backgammon/pygame_ui/pygame_ui.py:11:0: R0902: Too many instance attributes (8/7) (too-many-instance-attributes)
backgammon/pygame_ui/pygame_ui.py:44:8: E1101: Module 'pygame' has no 'init' member (no-member)
backgammon/pygame_ui/pygame_ui.py:89:29: E1101: Module 'pygame' has no 'QUIT' member (no-member)
backgammon/pygame_ui/pygame_ui.py:91:29: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
backgammon/pygame_ui/pygame_ui.py:92:32: E1101: Module 'pygame' has no 'K_ESCAPE' member (no-member)
backgammon/pygame_ui/pygame_ui.py:94:29: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
backgammon/pygame_ui/pygame_ui.py:111:8: E1101: Module 'pygame' has no 'quit' member (no-member)
************* Module backgammon.pygame_ui.board_interaction
backgammon/pygame_ui/board_interaction.py:74:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/board_interaction.py:143:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/board_interaction.py:171:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/board_interaction.py:189:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/board_interaction.py:197:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/board_interaction.py:205:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/board_interaction.py:252:0: C0301: Line too long (111/100) (line-too-long)
backgammon/pygame_ui/board_interaction.py:208:4: R0911: Too many return statements (7/6) (too-many-return-statements)
backgammon/pygame_ui/board_interaction.py:208:4: R0912: Too many branches (15/12) (too-many-branches)
************* Module backgammon.pygame_ui.click_detector
backgammon/pygame_ui/click_detector.py:53:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
backgammon/pygame_ui/click_detector.py:55:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
backgammon/pygame_ui/click_detector.py:30:4: R0914: Too many local variables (20/15) (too-many-locals)
************* Module backgammon.pygame_ui.color_scheme
backgammon/pygame_ui/color_scheme.py:9:0: R0903: Too few public methods (0/2) (too-few-public-methods)
************* Module backgammon.pygame_ui.renderers.visual_renderer
backgammon/pygame_ui/renderers/visual_renderer.py:489:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:521:0: C0301: Line too long (103/100) (line-too-long)
backgammon/pygame_ui/renderers/visual_renderer.py:612:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:615:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:618:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:621:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:624:20: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:625:34: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:626:39: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:630:20: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:631:24: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:632:39: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:633:19: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:636:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:638:20: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:639:34: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:640:39: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:644:20: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:645:24: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:646:39: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:647:19: C0303: Trailing whitespace (trailing-whitespace)
backgammon/pygame_ui/renderers/visual_renderer.py:42:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/pygame_ui/renderers/visual_renderer.py:64:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/pygame_ui/renderers/visual_renderer.py:135:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
backgammon/pygame_ui/renderers/visual_renderer.py:214:4: R0913: Too many arguments (6/5) (too-many-arguments)
backgammon/pygame_ui/renderers/visual_renderer.py:214:4: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
backgammon/pygame_ui/renderers/visual_renderer.py:493:8: C0103: Attribute name "SELECTED_COLOR" doesn't conform to snake_case naming style (invalid-name)
backgammon/pygame_ui/renderers/visual_renderer.py:494:8: C0103: Attribute name "VALID_MOVE_COLOR" doesn't conform to snake_case naming style (invalid-name)
backgammon/pygame_ui/renderers/visual_renderer.py:495:8: C0103: Attribute name "INVALID_MOVE_COLOR" doesn't conform to snake_case naming style (invalid-name)
backgammon/pygame_ui/renderers/visual_renderer.py:594:61: E1101: Module 'pygame' has no 'SRCALPHA' member (no-member)
backgammon/pygame_ui/renderers/visual_renderer.py:726:4: R0913: Too many arguments (7/5) (too-many-arguments)
backgammon/pygame_ui/renderers/visual_renderer.py:726:4: R0917: Too many positional arguments (7/5) (too-many-positional-arguments)
backgammon/pygame_ui/renderers/visual_renderer.py:756:4: R0913: Too many arguments (7/5) (too-many-arguments)
backgammon/pygame_ui/renderers/visual_renderer.py:756:4: R0917: Too many positional arguments (7/5) (too-many-positional-arguments)
************* Module backgammon.pygame_ui.renderers.board_renderer
backgammon/pygame_ui/renderers/board_renderer.py:97:0: C0301: Line too long (103/100) (line-too-long)
backgammon/pygame_ui/renderers/board_renderer.py:99:0: C0301: Line too long (103/100) (line-too-long)
backgammon/pygame_ui/renderers/board_renderer.py:23:0: R0902: Too many instance attributes (9/7) (too-many-instance-attributes)
backgammon/pygame_ui/renderers/board_renderer.py:79:4: R0913: Too many arguments (8/5) (too-many-arguments)
backgammon/pygame_ui/renderers/board_renderer.py:79:4: R0917: Too many positional arguments (8/5) (too-many-positional-arguments)
backgammon/pygame_ui/renderers/board_renderer.py:79:4: R0914: Too many local variables (16/15) (too-many-locals)
backgammon/pygame_ui/renderers/board_renderer.py:23:0: R0903: Too few public methods (1/2) (too-few-public-methods)
************* Module backgammon.pygame_ui.renderers.decorative_renderer
backgammon/pygame_ui/renderers/decorative_renderer.py:11:0: R0903: Too few public methods (1/2) (too-few-public-methods)
backgammon/pygame_ui/renderers/decorative_renderer.py:123:0: R0903: Too few public methods (1/2) (too-few-public-methods)
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
backgammon/core/BackgammonGame.py:192:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/core/BackgammonGame.py:217:16: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:223:16: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:229:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:237:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
backgammon/core/BackgammonGame.py:198:4: R0911: Too many return statements (9/6) (too-many-return-statements)
backgammon/core/BackgammonGame.py:260:4: R0911: Too many return statements (8/6) (too-many-return-statements)
************* Module backgammon.core.Board
backgammon/core/Board.py:37:0: C0303: Trailing whitespace (trailing-whitespace)
backgammon/core/Board.py:331:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
backgammon/core/Board.py:317:4: R0912: Too many branches (17/12) (too-many-branches)
backgammon/core/Board.py:331:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
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

    def can_bear_off(self):
        """
        Verifica si la ficha puede hacer bearing off desde su posición actual.

        Returns:
          bool: True si puede hacer bearing off, False en caso contrario
        """ (duplicate-code)

-----------------------------------
Your code has been rated at 9.61/10


```
