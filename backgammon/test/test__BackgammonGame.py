import unittest
from unittest.mock import MagicMock, patch, Mock
from backgammon.core import BackgammonGame, Board, Player, Dice, CLI, PygameUI

class TestBackgammonGame(unittest.TestCase):

  def setUp(self):
    self.game = BackgammonGame()

  def test_game_initialization(self):
    """Test BackgammonGame initializes correctly"""
    self.assertIsNotNone(self.game)
    self.assertTrue(hasattr(self.game, 'board'))
    self.assertTrue(hasattr(self.game, 'dice'))
    self.assertTrue(hasattr(self.game, 'players'))
    self.assertTrue(hasattr(self.game, 'current_player_index'))

  def test_game_initialization_with_ui_mode(self):
    """Test game initialization with specific UI mode"""
    cli_game = BackgammonGame(ui_mode="cli")
    pygame_game = BackgammonGame(ui_mode="pygame")
    
    self.assertIsNotNone(cli_game.ui)
    self.assertIsNotNone(pygame_game.ui)

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
    
    self.game.board.move_checker.assert_called_once_with(1, 4, "white")
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

  def test_is_valid_move(self):
    """Test checking if a move is valid"""
    self.game.board = MagicMock()
    self.game.dice = MagicMock()
    current_player = MagicMock()
    current_player.color = "white"
    self.game.get_current_player = MagicMock(return_value=current_player)
    
    self.game.board.is_valid_move.return_value = True
    self.game.dice.can_use_move.return_value = True
    
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
    """Test playing a turn with valid move"""
    self.game.roll_dice = MagicMock(return_value=[3, 5])
    self.game.ui = MagicMock()
    self.game.ui.get_move_input = MagicMock(return_value=(1, 4))
    self.game.make_move = MagicMock(return_value=True)
    self.game.has_valid_moves = MagicMock(return_value=True)
    self.game.switch_turns = MagicMock()
    
    self.game.play_turn()
    
    self.game.roll_dice.assert_called_once()
    self.game.ui.get_move_input.assert_called_once()
    self.game.make_move.assert_called_once_with(1, 4)
    self.game.switch_turns.assert_called_once()

  def test_play_turn_no_valid_moves(self):
    """Test playing a turn when no valid moves available"""
    self.game.roll_dice = MagicMock(return_value=[6, 6])
    self.game.ui = MagicMock()
    self.game.has_valid_moves = MagicMock(return_value=False)
    self.game.switch_turns = MagicMock()
    
    self.game.play_turn()
    
    self.game.switch_turns.assert_called_once()
    self.game.ui.display_message.assert_called()

  def test_play_game_until_win(self):
    """Test playing the game until a player wins"""
    self.game.is_game_over = MagicMock(side_effect=[False, False, True])
    self.game.play_turn = MagicMock()
    winner = MagicMock()
    winner.name = "Player1"
    self.game.get_winner = MagicMock(return_value=winner)
    self.game.ui = MagicMock()
    
    self.game.play_game()
    
    self.assertEqual(self.game.play_turn.call_count, 2)
    self.game.ui.display_winner.assert_called_once_with(winner)

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
    self.game.board.get_state.return_value = {'board': 'state'}
    self.game.dice = MagicMock()
    self.game.dice.get_state.return_value = {'dice': 'state'}
    player1 = MagicMock()
    player1.get_state.return_value = {'player1': 'state'}
    player2 = MagicMock()
    player2.get_state.return_value = {'player2': 'state'}
    self.game.players = [player1, player2]
    
    state = self.game.get_game_state()
    
    self.assertIn('board', state)
    self.assertIn('dice', state)
    self.assertIn('players', state)
    self.assertIn('current_player_index', state)

  def test_load_game_state(self):
    """Test loading game state"""
    state = {
      'board': {'board': 'state'},
      'dice': {'dice': 'state'},
      'players': [{'player1': 'state'}, {'player2': 'state'}],
      'current_player_index': 1,
      'is_started': True
    }
    
    self.game.board = MagicMock()
    self.game.dice = MagicMock()
    player1 = MagicMock()
    player2 = MagicMock()
    self.game.players = [player1, player2]
    
    self.game.set_game_state(state)
    
    self.game.board.set_state.assert_called_once_with({'board': 'state'})
    self.game.dice.set_state.assert_called_once_with({'dice': 'state'})
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
    
    self.assertEqual(stats['moves'], 10)
    self.assertEqual(stats['duration'], 300)
    self.assertIn('winner', stats)

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

if __name__ == '__main__':
  unittest.main()