"""
Test module for BackgammonGame class.

This module contains unit tests for the BackgammonGame class which manages
the main game logic and state for the backgammon game.
"""

import unittest
from unittest.mock import MagicMock, Mock
from backgammon.core import BackgammonGame, Player
from backgammon.cli import CLI

# pylint: disable=C0116  # many simple test methods without individual docstrings
# pylint: disable=C0103  # module name follows test naming convention
# pylint: disable=R0904  # many public methods needed for comprehensive testing


class TestBackgammonGame(unittest.TestCase):
    """Test cases for the BackgammonGame class."""

    def setUp(self):
        self.game = BackgammonGame()

    def test_game_initialization(self):
        """Test BackgammonGame initializes correctly"""
        self.assertIsNotNone(self.game)
        self.assertTrue(hasattr(self.game, "board"))
        self.assertTrue(hasattr(self.game, "dice"))
        self.assertTrue(hasattr(self.game, "players"))
        self.assertTrue(hasattr(self.game, "current_player_index"))

    def test_game_initialization_with_ui(self):
        """Test game initialization with UI interface"""
        cli = CLI()
        cli_game = BackgammonGame(cli)

        self.assertIsNotNone(cli_game.ui)
        self.assertEqual(cli_game.ui, cli)

    def test_setup_board(self):
        """Test board setup initialization"""
        self.game.board = MagicMock()
        self.game.setup_board()
        self.game.board.setup_initial_position.assert_called_once()

    def test_setup_players_default(self):
        """Test players setup with default names"""
        self.game.setup_players()
        self.assertEqual(len(self.game.players), 2)
        self.assertIsInstance(self.game.players[0], Player)
        self.assertIsInstance(self.game.players[1], Player)
        self.assertEqual(self.game.players[0].color, "white")
        self.assertEqual(self.game.players[1].color, "black")

    def test_setup_players_with_names(self):
        """Test players setup with custom names"""
        self.game.setup_players("Alice", "Bob")
        self.assertEqual(self.game.players[0].name, "Alice")
        self.assertEqual(self.game.players[1].name, "Bob")

    def test_start_game(self):
        """Test starting the game calls setup methods"""
        self.game.setup_board = MagicMock()
        self.game.setup_players = MagicMock()
        self.game.initialize_ui = MagicMock()

        self.game.start_game()

        self.game.setup_board.assert_called_once()
        self.game.setup_players.assert_called_once()
        self.assertTrue(self.game.is_started)

    def test_switch_turns(self):
        """Test switching turns between players"""
        self.game.current_player_index = 0
        self.game.switch_turns()
        self.assertEqual(self.game.current_player_index, 1)

        self.game.switch_turns()
        self.assertEqual(self.game.current_player_index, 0)

    def test_get_current_player(self):
        """Test getting the current player"""
        self.game.players = [Mock(), Mock()]

        self.game.current_player_index = 0
        self.assertEqual(self.game.get_current_player(), self.game.players[0])

        self.game.current_player_index = 1
        self.assertEqual(self.game.get_current_player(), self.game.players[1])

    def test_get_opponent_player(self):
        """Test getting the opponent player"""
        self.game.players = [Mock(), Mock()]

        self.game.current_player_index = 0
        self.assertEqual(self.game.get_opponent_player(), self.game.players[1])

        self.game.current_player_index = 1
        self.assertEqual(self.game.get_opponent_player(), self.game.players[0])

    def test_roll_dice(self):
        """Test rolling dice updates dice values"""
        self.game.dice = MagicMock()
        self.game.dice.roll.return_value = [3, 5]

        values = self.game.roll_dice()

        self.assertEqual(values, [3, 5])
        self.game.dice.roll.assert_called_once()

    def test_is_game_over_false(self):
        """Test game over returns False when no player has won"""
        player1 = MagicMock()
        player2 = MagicMock()
        player1.has_won.return_value = False
        player2.has_won.return_value = False
        self.game.players = [player1, player2]

        self.assertFalse(self.game.is_game_over())

    def test_is_game_over_true(self):
        """Test game over returns True when a player has won"""
        player1 = MagicMock()
        player2 = MagicMock()
        player1.has_won.return_value = True
        player2.has_won.return_value = False
        self.game.players = [player1, player2]

        self.assertTrue(self.game.is_game_over())

    def test_get_winner_none(self):
        """Test get_winner returns None if no player has won"""
        player1 = MagicMock()
        player2 = MagicMock()
        player1.has_won.return_value = False
        player2.has_won.return_value = False
        self.game.players = [player1, player2]

        self.assertIsNone(self.game.get_winner())

    def test_get_winner_player1(self):
        """Test get_winner returns player 1 if they have won"""
        player1 = MagicMock()
        player2 = MagicMock()
        player1.has_won.return_value = True
        player2.has_won.return_value = False
        self.game.players = [player1, player2]

        self.assertEqual(self.game.get_winner(), player1)

    def test_get_winner_player2(self):
        """Test get_winner returns player 2 if they have won"""
        player1 = MagicMock()
        player2 = MagicMock()
        player1.has_won.return_value = False
        player2.has_won.return_value = True
        self.game.players = [player1, player2]

        self.assertEqual(self.game.get_winner(), player2)

    def test_make_move_valid(self):
        """Test making a valid move calls board.move_checker"""
        self.game.board = MagicMock()
        self.game.board.move_checker.return_value = True
        current_player = MagicMock()
        current_player.color = "white"
        self.game.get_current_player = MagicMock(return_value=current_player)

        result = self.game.make_move(1, 4)

        self.game.board.move_checker.assert_called_once_with(0, 3, "white")
        self.assertTrue(result)

    def test_make_move_invalid(self):
        """Test making an invalid move returns False"""
        self.game.board = MagicMock()
        self.game.board.move_checker.return_value = False
        current_player = MagicMock()
        current_player.color = "white"
        self.game.get_current_player = MagicMock(return_value=current_player)

        result = self.game.make_move(1, 24)

        self.assertFalse(result)

    def test_make_move_with_specific_dice_roll(self):
        self.game.start_game()

        # Mock the dice instance directly
        self.game.dice.roll = Mock(return_value=[3, 5])
        self.game.dice.can_use_move = Mock(return_value=True)

        self.game.roll_dice()

        # Mock board to return True for move
        board_mock = Mock()
        board_mock.move_checker = Mock(return_value=True)
        self.game.board = board_mock

        result = self.game.make_move(1, 4)  # Move 3 spaces

        self.assertTrue(result)
        # Verify that the board's move_checker was called with correct parameters
        board_mock.move_checker.assert_called_with(
            0, 3, self.game.get_current_player().color
        )

    def test_is_valid_move(self):
        """Test checking if a move is valid"""
        self.game.board = MagicMock()
        self.game.dice = MagicMock()
        current_player = MagicMock()
        current_player.color = "white"
        self.game.get_current_player = MagicMock(return_value=current_player)

        # Mock the methods that is_valid_move actually uses
        self.game.dice.can_use_move.return_value = True
        self.game.board.points = [
            [MagicMock()] for _ in range(24)
        ]  # Points with checkers
        self.game.board.get_point_top_color.return_value = "white"
        self.game.board.is_point_available.return_value = True

        result = self.game.is_valid_move(1, 4)
        self.assertTrue(result)

    def test_get_possible_moves(self):
        """Test getting possible moves for current player"""
        self.game.board = MagicMock()
        self.game.dice = MagicMock()
        current_player = MagicMock()
        self.game.get_current_player = MagicMock(return_value=current_player)

        expected_moves = [(1, 4), (6, 9)]
        self.game.board.get_possible_moves.return_value = expected_moves

        moves = self.game.get_possible_moves()
        self.assertEqual(moves, expected_moves)

    def test_has_valid_moves_true(self):
        """Test has_valid_moves returns True when moves available"""
        self.game.get_possible_moves = MagicMock(return_value=[(1, 4), (6, 9)])
        self.assertTrue(self.game.has_valid_moves())

    def test_has_valid_moves_false(self):
        """Test has_valid_moves returns False when no moves available"""
        self.game.get_possible_moves = MagicMock(return_value=[])
        self.assertFalse(self.game.has_valid_moves())

    def test_play_turn_with_valid_move(self):
        """Test play_turn only handles dice rolling in new architecture"""
        self.game.roll_dice = MagicMock(return_value=[3, 5])
        self.game.dice = MagicMock()
        self.game.dice.get_available_moves.return_value = (
            []
        )  # No moves available, should roll

        self.game.play_turn()

        # In new architecture, play_turn only rolls dice
        self.game.roll_dice.assert_called_once()

    def test_play_turn_with_available_moves(self):
        """Test play_turn doesn't roll when moves are available"""
        self.game.roll_dice = MagicMock()
        self.game.dice = MagicMock()
        self.game.dice.get_available_moves.return_value = [
            3,
            5,
        ]  # Moves available, shouldn't roll

        self.game.play_turn()

        # Should not roll dice when moves are already available
        self.game.roll_dice.assert_not_called()

    def test_play_turn_no_valid_moves(self):
        """Test play_turn still rolls dice even when no valid moves"""
        self.game.roll_dice = MagicMock(return_value=[6, 6])
        self.game.dice = MagicMock()
        self.game.dice.get_available_moves.return_value = (
            []
        )  # No moves available, should roll

        self.game.play_turn()

        # play_turn only handles dice rolling, not turn switching
        self.game.roll_dice.assert_called_once()

    def test_can_continue_turn_true(self):
        """Test can_continue_turn returns True when moves and dice available"""
        self.game.dice = MagicMock()
        self.game.dice.get_available_moves.return_value = [3, 5]
        self.game.has_valid_moves = MagicMock(return_value=True)

        self.assertTrue(self.game.can_continue_turn())

    def test_can_continue_turn_false(self):
        """Test can_continue_turn returns False when no moves or dice available"""
        self.game.dice = MagicMock()
        self.game.dice.get_available_moves.return_value = []
        self.game.has_valid_moves = MagicMock(return_value=False)

        self.assertFalse(self.game.can_continue_turn())

    def test_complete_turn(self):
        """Test complete_turn switches players"""
        self.game.switch_turns = MagicMock()

        self.game.complete_turn()

        self.game.switch_turns.assert_called_once()

    def test_play_game_until_win(self):
        """Test play_game basic loop (deprecated method, CLI.run_game is preferred)"""
        self.game.is_game_over = MagicMock(side_effect=[False, False, True])
        self.game.play_turn = MagicMock()
        self.game.can_continue_turn = MagicMock(return_value=False)
        self.game.complete_turn = MagicMock()

        self.game.play_game()

        # Verify the basic game loop worked
        self.assertEqual(self.game.play_turn.call_count, 2)
        self.assertEqual(self.game.complete_turn.call_count, 2)

    def test_reset_game(self):
        """Test resetting the game calls reset on components"""
        self.game.board = MagicMock()
        self.game.dice = MagicMock()
        player1 = MagicMock()
        player2 = MagicMock()
        self.game.players = [player1, player2]

        self.game.reset_game()

        self.game.board.reset.assert_called_once()
        self.game.dice.reset.assert_called_once()
        player1.reset.assert_called_once()
        player2.reset.assert_called_once()
        self.assertEqual(self.game.current_player_index, 0)
        self.assertFalse(self.game.is_started)

    def test_pause_game(self):
        """Test pausing the game"""
        self.game.is_paused = False
        self.game.pause_game()
        self.assertTrue(self.game.is_paused)

    def test_resume_game(self):
        """Test resuming the game"""
        self.game.is_paused = True
        self.game.resume_game()
        self.assertFalse(self.game.is_paused)

    def test_save_game_state(self):
        """Test saving game state"""
        self.game.board = MagicMock()
        self.game.board.get_state.return_value = {"board": "state"}
        self.game.dice = MagicMock()
        self.game.dice.get_state.return_value = {"dice": "state"}
        player1 = MagicMock()
        player1.get_state.return_value = {"player1": "state"}
        player2 = MagicMock()
        player2.get_state.return_value = {"player2": "state"}
        self.game.players = [player1, player2]

        state = self.game.get_game_state()

        self.assertIn("board", state)
        self.assertIn("dice", state)
        self.assertIn("players", state)
        self.assertIn("current_player_index", state)

    def test_load_game_state(self):
        """Test loading game state"""
        state = {
            "board": {"board": "state"},
            "dice": {"dice": "state"},
            "players": [{"player1": "state"}, {"player2": "state"}],
            "current_player_index": 1,
            "is_started": True,
        }

        self.game.board = MagicMock()
        self.game.dice = MagicMock()
        player1 = MagicMock()
        player2 = MagicMock()
        self.game.players = [player1, player2]

        self.game.set_game_state(state)

        self.game.board.set_state.assert_called_once_with({"board": "state"})
        self.game.dice.set_state.assert_called_once_with({"dice": "state"})
        self.assertEqual(self.game.current_player_index, 1)
        self.assertTrue(self.game.is_started)

    def test_validate_move_coordinates(self):
        """Test validating move coordinates"""
        # Valid coordinates
        self.assertTrue(self.game.validate_move_coordinates(1, 4))
        self.assertTrue(self.game.validate_move_coordinates("bar", 20))
        self.assertTrue(self.game.validate_move_coordinates(5, "off"))

        # Invalid coordinates
        self.assertFalse(self.game.validate_move_coordinates(0, 4))
        self.assertFalse(self.game.validate_move_coordinates(1, 25))
        self.assertFalse(self.game.validate_move_coordinates(-1, 4))

    def test_get_game_statistics(self):
        """Test getting game statistics"""
        self.game.move_count = 10
        self.game.start_time = 1000
        self.game.end_time = 1300

        stats = self.game.get_game_statistics()

        self.assertEqual(stats["moves"], 10)
        self.assertEqual(stats["duration"], 300)
        self.assertIn("winner", stats)

    def test_undo_last_move(self):
        """Test undoing the last move"""
        self.game.move_history = [(1, 4, "white")]
        self.game.board = MagicMock()

        result = self.game.undo_last_move()

        self.assertTrue(result)
        self.assertEqual(len(self.game.move_history), 0)

    def test_undo_last_move_no_history(self):
        """Test undoing when no move history"""
        self.game.move_history = []

        result = self.game.undo_last_move()

        self.assertFalse(result)

    def test_str_representation(self):
        """Test string representation of game"""
        game_str = str(self.game)
        self.assertIsInstance(game_str, str)
        self.assertIn("BackgammonGame", game_str)

    def test_repr_representation(self):
        """Test repr representation of game"""
        game_repr = repr(self.game)
        self.assertIsInstance(game_repr, str)
        self.assertIn("BackgammonGame", game_repr)

    def test_copy_game(self):
        """Test copying game state"""
        self.game.current_player_index = 1
        self.game.is_started = True

        copied_game = self.game.copy()

        self.assertEqual(copied_game.current_player_index, 1)
        self.assertEqual(copied_game.is_started, True)
        self.assertIsNot(copied_game, self.game)

    def test_game_over_when_player_wins(self):
        self.game.setup_players()

        # Initially no player has won
        for player in self.game.players:
            player.has_won = Mock(return_value=False)

        self.assertFalse(self.game.is_game_over())

        # Now player 2 wins
        self.game.players[1].has_won = Mock(return_value=True)

        self.assertTrue(self.game.is_game_over())

        winner = self.game.get_winner()
        self.assertEqual(winner, self.game.players[1])  # Player 2 won

    def test_set_ui_with_set_game_method(self):
        """Test set_ui when UI has set_game method"""
        mock_ui = Mock()
        mock_ui.set_game = Mock()
        self.game.set_ui(mock_ui)
        self.assertEqual(self.game.ui, mock_ui)
        mock_ui.set_game.assert_called_once_with(self.game)

    def test_start_game_with_ui(self):
        """Test start_game displays board when UI is present"""
        mock_ui = Mock()
        self.game.ui = mock_ui
        self.game.start_game()
        mock_ui.display_message.assert_called()
        mock_ui.display_board.assert_called()

    def test_make_move_from_bar_with_invalid_to_pos(self):
        """Test make_move from bar with invalid to_pos"""
        self.game.setup_players()
        result = self.game.make_move("bar", 0)
        self.assertFalse(result)
        result = self.game.make_move("bar", 25)
        self.assertFalse(result)

    def test_make_move_bear_off_with_invalid_from_pos(self):
        """Test make_move to off with invalid from_pos"""
        self.game.setup_players()
        result = self.game.make_move(0, "off")
        self.assertFalse(result)
        result = self.game.make_move(25, "off")
        self.assertFalse(result)

    def test_make_move_normal_with_invalid_positions(self):
        """Test make_move with invalid from and to positions"""
        self.game.setup_players()
        result = self.game.make_move(0, 5)
        self.assertFalse(result)
        result = self.game.make_move(25, 5)
        self.assertFalse(result)
        result = self.game.make_move(5, 0)
        self.assertFalse(result)
        result = self.game.make_move(5, 25)
        self.assertFalse(result)

    def test_calculate_move_distance_white_invalid_direction(self):
        """Test calculate move distance for white moving in invalid direction"""
        self.game.setup_players()
        distance = self.game._calculate_move_distance(5, 10)
        self.assertEqual(distance, 0)

    def test_calculate_move_distance_black_invalid_direction(self):
        """Test calculate move distance for black moving in invalid direction"""
        self.game.setup_players()
        self.game.current_player_index = 1
        distance = self.game._calculate_move_distance(10, 5)
        self.assertEqual(distance, 0)

    def test_calculate_move_distance_from_bar_white(self):
        """Test calculate move distance from bar for white"""
        self.game.setup_players()
        distance = self.game._calculate_move_distance("bar", 20)
        self.assertEqual(distance, 5)

    def test_calculate_move_distance_from_bar_black(self):
        """Test calculate move distance from bar for black"""
        self.game.setup_players()
        self.game.current_player_index = 1
        distance = self.game._calculate_move_distance("bar", 5)
        self.assertEqual(distance, 5)

    def test_calculate_move_distance_to_off_white(self):
        """Test calculate move distance to off for white"""
        self.game.setup_players()
        distance = self.game._calculate_move_distance(3, "off")
        self.assertEqual(distance, 3)

    def test_calculate_move_distance_to_off_black(self):
        """Test calculate move distance to off for black"""
        self.game.setup_players()
        self.game.current_player_index = 1
        distance = self.game._calculate_move_distance(20, "off")
        self.assertEqual(distance, 5)

    def test_validate_move_coordinates_invalid_to_pos_type(self):
        """Test validate_move_coordinates with invalid to_pos type"""
        result = self.game.validate_move_coordinates(1, None)
        self.assertFalse(result)

    def test_validate_move_coordinates_invalid_to_pos_string(self):
        """Test validate_move_coordinates with invalid to_pos string"""
        result = self.game.validate_move_coordinates(1, "invalid")
        self.assertFalse(result)

    def test_validate_move_coordinates_invalid_to_pos_range(self):
        """Test validate_move_coordinates with out of range to_pos"""
        result = self.game.validate_move_coordinates(1, 0)
        self.assertFalse(result)
        result = self.game.validate_move_coordinates(1, 25)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()

