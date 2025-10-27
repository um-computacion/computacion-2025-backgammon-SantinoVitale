# Automated Reports
## Coverage Report
```text
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
backgammon/core/BackgammonGame.py     221     25    89%   167-168, 175-176, 222, 238, 253, 273, 278-282, 286-290, 300, 310, 469-471, 495-496, 541
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
backgammon/pygame_ui/backgammon_board.py:16:0: R0902: Too many instance attributes (8/7) (too-many-instance-attributes)
************* Module backgammon.pygame_ui.button
backgammon/pygame_ui/button.py:26:4: R0913: Too many arguments (6/5) (too-many-arguments)
backgammon/pygame_ui/button.py:26:4: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
************* Module backgammon.pygame_ui.board_dimensions
backgammon/pygame_ui/board_dimensions.py:9:0: R0902: Too many instance attributes (13/7) (too-many-instance-attributes)
************* Module backgammon.pygame_ui.pygame_ui
backgammon/pygame_ui/pygame_ui.py:11:0: R0902: Too many instance attributes (8/7) (too-many-instance-attributes)
backgammon/pygame_ui/pygame_ui.py:44:8: E1101: Module 'pygame' has no 'init' member (no-member)
backgammon/pygame_ui/pygame_ui.py:89:29: E1101: Module 'pygame' has no 'QUIT' member (no-member)
backgammon/pygame_ui/pygame_ui.py:91:29: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
backgammon/pygame_ui/pygame_ui.py:92:32: E1101: Module 'pygame' has no 'K_ESCAPE' member (no-member)
backgammon/pygame_ui/pygame_ui.py:94:29: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
backgammon/pygame_ui/pygame_ui.py:111:8: E1101: Module 'pygame' has no 'quit' member (no-member)
************* Module backgammon.pygame_ui.board_interaction
backgammon/pygame_ui/board_interaction.py:278:4: R0911: Too many return statements (7/6) (too-many-return-statements)
backgammon/pygame_ui/board_interaction.py:278:4: R0912: Too many branches (15/12) (too-many-branches)
************* Module backgammon.pygame_ui.click_detector
backgammon/pygame_ui/click_detector.py:30:4: R0914: Too many local variables (20/15) (too-many-locals)
************* Module backgammon.pygame_ui.color_scheme
backgammon/pygame_ui/color_scheme.py:9:0: R0903: Too few public methods (0/2) (too-few-public-methods)
************* Module backgammon.pygame_ui.renderers.visual_renderer
backgammon/pygame_ui/renderers/visual_renderer.py:211:4: R0913: Too many arguments (6/5) (too-many-arguments)
backgammon/pygame_ui/renderers/visual_renderer.py:211:4: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
backgammon/pygame_ui/renderers/visual_renderer.py:595:61: E1101: Module 'pygame' has no 'SRCALPHA' member (no-member)
backgammon/pygame_ui/renderers/visual_renderer.py:601:59: W0613: Unused argument 'board' (unused-argument)
backgammon/pygame_ui/renderers/visual_renderer.py:719:4: R0913: Too many arguments (7/5) (too-many-arguments)
backgammon/pygame_ui/renderers/visual_renderer.py:719:4: R0917: Too many positional arguments (7/5) (too-many-positional-arguments)
backgammon/pygame_ui/renderers/visual_renderer.py:749:4: R0913: Too many arguments (7/5) (too-many-arguments)
backgammon/pygame_ui/renderers/visual_renderer.py:749:4: R0917: Too many positional arguments (7/5) (too-many-positional-arguments)
************* Module backgammon.pygame_ui.renderers.board_renderer
backgammon/pygame_ui/renderers/board_renderer.py:23:0: R0902: Too many instance attributes (9/7) (too-many-instance-attributes)
backgammon/pygame_ui/renderers/board_renderer.py:79:4: R0913: Too many arguments (9/5) (too-many-arguments)
backgammon/pygame_ui/renderers/board_renderer.py:79:4: R0917: Too many positional arguments (9/5) (too-many-positional-arguments)
backgammon/pygame_ui/renderers/board_renderer.py:79:4: R0914: Too many local variables (17/15) (too-many-locals)
backgammon/pygame_ui/renderers/board_renderer.py:23:0: R0903: Too few public methods (1/2) (too-few-public-methods)
************* Module backgammon.pygame_ui.renderers.decorative_renderer
backgammon/pygame_ui/renderers/decorative_renderer.py:11:0: R0903: Too few public methods (1/2) (too-few-public-methods)
backgammon/pygame_ui/renderers/decorative_renderer.py:123:0: R0903: Too few public methods (1/2) (too-few-public-methods)
************* Module backgammon.cli.GameController
backgammon/cli/GameController.py:1:0: C0103: Module name "GameController" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.cli.BackgammonCLI
backgammon/cli/BackgammonCLI.py:1:0: C0103: Module name "BackgammonCLI" doesn't conform to snake_case naming style (invalid-name)
backgammon/cli/BackgammonCLI.py:133:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
backgammon/cli/BackgammonCLI.py:122:4: R0912: Too many branches (22/12) (too-many-branches)
backgammon/cli/BackgammonCLI.py:122:4: R0915: Too many statements (67/50) (too-many-statements)
************* Module backgammon.cli.CommandParser
backgammon/cli/CommandParser.py:1:0: C0103: Module name "CommandParser" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.cli.UserInterface
backgammon/cli/UserInterface.py:1:0: C0103: Module name "UserInterface" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.cli.BoardRenderer
backgammon/cli/BoardRenderer.py:1:0: C0103: Module name "BoardRenderer" doesn't conform to snake_case naming style (invalid-name)
backgammon/cli/BoardRenderer.py:17:4: R0912: Too many branches (13/12) (too-many-branches)
************* Module backgammon.cli.InputValidator
backgammon/cli/InputValidator.py:1:0: C0103: Module name "InputValidator" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.core.BackgammonGame
backgammon/core/BackgammonGame.py:198:4: R0911: Too many return statements (9/6) (too-many-return-statements)
backgammon/core/BackgammonGame.py:255:4: R0911: Too many return statements (8/6) (too-many-return-statements)
************* Module backgammon.core.Board
backgammon/core/Board.py:331:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
backgammon/core/Board.py:317:4: R0912: Too many branches (17/12) (too-many-branches)
backgammon/core/Board.py:331:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
************* Module backgammon.test.test__BackgammonGame
backgammon/test/test__BackgammonGame.py:1:0: C0103: Module name "test__BackgammonGame" doesn't conform to snake_case naming style (invalid-name)
backgammon/test/test__BackgammonGame.py:541:19: W0212: Access to a protected member _calculate_move_distance of a client class (protected-access)
backgammon/test/test__BackgammonGame.py:563:19: W0212: Access to a protected member _calculate_move_distance of a client class (protected-access)
************* Module backgammon.test.test__board
backgammon/test/test__board.py:16:0: R0904: Too many public methods (30/20) (too-many-public-methods)
************* Module backgammon.test.test__user_interface
backgammon/test/test__user_interface.py:79:47: W0613: Unused argument 'mock_input' (unused-argument)
backgammon/test/test__user_interface.py:86:34: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__user_interface.py:86:46: W0613: Unused argument 'mock_input' (unused-argument)
backgammon/test/test__user_interface.py:93:41: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__user_interface.py:93:53: W0613: Unused argument 'mock_input' (unused-argument)
backgammon/test/test__user_interface.py:100:41: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__user_interface.py:100:53: W0613: Unused argument 'mock_input' (unused-argument)
backgammon/test/test__user_interface.py:107:49: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__user_interface.py:107:61: W0613: Unused argument 'mock_input' (unused-argument)
backgammon/test/test__user_interface.py:114:49: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__user_interface.py:114:61: W0613: Unused argument 'mock_input' (unused-argument)
backgammon/test/test__user_interface.py:120:46: W0613: Unused argument 'mock_input' (unused-argument)
backgammon/test/test__user_interface.py:126:43: W0613: Unused argument 'mock_input' (unused-argument)
backgammon/test/test__user_interface.py:11:0: R0904: Too many public methods (34/20) (too-many-public-methods)
************* Module backgammon.test.test__game_controller
backgammon/test/test__game_controller.py:11:0: R0904: Too many public methods (31/20) (too-many-public-methods)
************* Module backgammon.test.test__Player
backgammon/test/test__Player.py:1:0: C0103: Module name "test__Player" doesn't conform to snake_case naming style (invalid-name)
************* Module backgammon.test.test__button
backgammon/test/test__button.py:18:42: W0613: Unused argument 'mock_rect_class' (unused-argument)
backgammon/test/test__button.py:35:41: W0613: Unused argument 'mock_rect_class' (unused-argument)
backgammon/test/test__button.py:50:45: W0613: Unused argument 'mock_rect_class' (unused-argument)
backgammon/test/test__button.py:64:46: W0613: Unused argument 'mock_rect_class' (unused-argument)
backgammon/test/test__button.py:82:49: W0613: Unused argument 'mock_rect_class' (unused-argument)
backgammon/test/test__button.py:98:39: W0613: Unused argument 'mock_rect_class' (unused-argument)
backgammon/test/test__button.py:113:38: W0613: Unused argument 'mock_rect_class' (unused-argument)
backgammon/test/test__button.py:132:36: W0613: Unused argument 'mock_rect_class' (unused-argument)
backgammon/test/test__button.py:146:37: W0613: Unused argument 'mock_rect_class' (unused-argument)
backgammon/test/test__button.py:167:14: W0613: Unused argument 'mock_rect_class' (unused-argument)
backgammon/test/test__button.py:197:42: W0613: Unused argument 'mock_rect_class' (unused-argument)
backgammon/test/test__button.py:224:35: W0613: Unused argument 'mock_rect_class' (unused-argument)
************* Module backgammon.test.test__backgammon_board
backgammon/test/test__backgammon_board.py:15:43: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:29:42: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:41:28: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:54:50: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:72:38: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:85:50: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__backgammon_board.py:85:62: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:105:44: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:124:42: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:143:47: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:162:50: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:185:39: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:200:36: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:261:8: W0212: Access to a protected member _update_button_state of a client class (protected-access)
backgammon/test/test__backgammon_board.py:246:51: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__backgammon_board.py:246:63: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:284:8: W0212: Access to a protected member _update_button_state of a client class (protected-access)
backgammon/test/test__backgammon_board.py:268:48: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:295:8: W0212: Access to a protected member _update_button_state of a client class (protected-access)
backgammon/test/test__backgammon_board.py:289:47: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:319:8: W0212: Access to a protected member _handle_dice_button_click of a client class (protected-access)
backgammon/test/test__backgammon_board.py:303:52: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__backgammon_board.py:303:64: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:335:8: W0212: Access to a protected member _handle_dice_button_click of a client class (protected-access)
backgammon/test/test__backgammon_board.py:327:71: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:351:8: W0212: Access to a protected member _handle_dice_button_click of a client class (protected-access)
backgammon/test/test__backgammon_board.py:342:64: W0613: Unused argument 'mock_rect' (unused-argument)
backgammon/test/test__backgammon_board.py:367:8: W0612: Unused variable 'board' (unused-variable)
************* Module backgammon.test.test__pygame_ui
backgammon/test/test__pygame_ui.py:17:43: W0613: Unused argument 'mock_board_class' (unused-argument)
backgammon/test/test__pygame_ui.py:35:42: W0613: Unused argument 'mock_board_class' (unused-argument)
backgammon/test/test__pygame_ui.py:66:28: W0613: Unused argument 'mock_board_class' (unused-argument)
backgammon/test/test__pygame_ui.py:89:47: W0613: Unused argument 'mock_board_class' (unused-argument)
backgammon/test/test__pygame_ui.py:102:33: W0613: Unused argument 'mock_board_class' (unused-argument)
backgammon/test/test__pygame_ui.py:124:46: W0613: Unused argument 'mock_board_class' (unused-argument)
backgammon/test/test__pygame_ui.py:146:27: E1101: Module 'pygame' has no 'QUIT' member (no-member)
backgammon/test/test__pygame_ui.py:153:26: E1101: Module 'pygame' has no 'QUIT' member (no-member)
backgammon/test/test__pygame_ui.py:141:38: W0613: Unused argument 'mock_board_class' (unused-argument)
backgammon/test/test__pygame_ui.py:168:30: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
backgammon/test/test__pygame_ui.py:169:31: E1101: Module 'pygame' has no 'K_ESCAPE' member (no-member)
backgammon/test/test__pygame_ui.py:176:26: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
backgammon/test/test__pygame_ui.py:177:25: E1101: Module 'pygame' has no 'K_ESCAPE' member (no-member)
backgammon/test/test__pygame_ui.py:163:44: W0613: Unused argument 'mock_board_class' (unused-argument)
backgammon/test/test__pygame_ui.py:192:38: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
backgammon/test/test__pygame_ui.py:199:26: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
backgammon/test/test__pygame_ui.py:187:45: W0613: Unused argument 'mock_board_class' (unused-argument)
backgammon/test/test__pygame_ui.py:212:47: W0613: Unused argument 'mock_board_class' (unused-argument)
backgammon/test/test__pygame_ui.py:232:43: W0613: Unused argument 'mock_board_class' (unused-argument)
backgammon/test/test__pygame_ui.py:263:27: E1101: Module 'pygame' has no 'QUIT' member (no-member)
backgammon/test/test__pygame_ui.py:272:26: E1101: Module 'pygame' has no 'QUIT' member (no-member)
backgammon/test/test__pygame_ui.py:256:33: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__pygame_ui.py:256:45: W0613: Unused argument 'mock_board_class' (unused-argument)
backgammon/test/test__pygame_ui.py:291:27: E1101: Module 'pygame' has no 'QUIT' member (no-member)
backgammon/test/test__pygame_ui.py:296:26: E1101: Module 'pygame' has no 'QUIT' member (no-member)
backgammon/test/test__pygame_ui.py:286:56: W0613: Unused argument 'mock_board_class' (unused-argument)
backgammon/test/test__pygame_ui.py:320:8: E1128: Assigning result of a function call, where the function returns None (assignment-from-none)
backgammon/test/test__pygame_ui.py:313:48: W0613: Unused argument 'mock_board_class' (unused-argument)
************* Module backgammon.test.test__input_validator
backgammon/test/test__input_validator.py:10:0: R0904: Too many public methods (21/20) (too-many-public-methods)
************* Module backgammon.test.test__board_interaction
backgammon/test/test__board_interaction.py:85:46: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:93:51: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:116:58: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:126:51: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:153:44: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:161:55: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:178:50: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:217:50: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:227:59: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:243:61: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:265:17: W0212: Access to a protected member _calculate_valid_destinations of a client class (protected-access)
backgammon/test/test__board_interaction.py:276:17: W0212: Access to a protected member _calculate_valid_destinations of a client class (protected-access)
backgammon/test/test__board_interaction.py:298:17: W0212: Access to a protected member _calculate_valid_destinations of a client class (protected-access)
backgammon/test/test__board_interaction.py:305:17: W0212: Access to a protected member _calculate_valid_destinations_from_bar of a client class (protected-access)
backgammon/test/test__board_interaction.py:323:8: W0212: Access to a protected member _execute_move of a client class (protected-access)
backgammon/test/test__board_interaction.py:339:8: W0212: Access to a protected member _execute_move of a client class (protected-access)
backgammon/test/test__board_interaction.py:329:40: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:353:8: W0212: Access to a protected member _execute_move of a client class (protected-access)
backgammon/test/test__board_interaction.py:367:8: W0212: Access to a protected member _execute_move_from_bar of a client class (protected-access)
backgammon/test/test__board_interaction.py:358:49: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:375:8: W0212: Access to a protected member _execute_move_to_off of a client class (protected-access)
backgammon/test/test__board_interaction.py:372:52: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:391:8: W0212: Access to a protected member _execute_move_to_off of a client class (protected-access)
backgammon/test/test__board_interaction.py:381:47: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:408:8: W0212: Access to a protected member _check_turn_completion of a client class (protected-access)
backgammon/test/test__board_interaction.py:406:49: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:420:8: W0212: Access to a protected member _check_turn_completion of a client class (protected-access)
backgammon/test/test__board_interaction.py:413:59: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:433:8: W0212: Access to a protected member _check_turn_completion of a client class (protected-access)
backgammon/test/test__board_interaction.py:425:56: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:446:8: W0212: Access to a protected member _check_turn_completion of a client class (protected-access)
backgammon/test/test__board_interaction.py:438:56: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:474:8: W0212: Access to a protected member _try_select_point of a client class (protected-access)
backgammon/test/test__board_interaction.py:461:54: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:493:8: W0212: Access to a protected member _try_select_point of a client class (protected-access)
backgammon/test/test__board_interaction.py:480:48: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:513:8: W0212: Access to a protected member _try_select_point of a client class (protected-access)
backgammon/test/test__board_interaction.py:498:48: W0613: Unused argument 'mock_print' (unused-argument)
backgammon/test/test__board_interaction.py:1:0: R0801: Similar lines in 2 files
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
Your code has been rated at 9.50/10


```
