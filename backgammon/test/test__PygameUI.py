import unittest
from unittest.mock import patch, MagicMock, Mock
from backgammon.core import PygameUI

class TestPygameUI(unittest.TestCase):

  def setUp(self):
    with patch('pygame.init'), patch('pygame.display.set_mode'), patch('pygame.display.set_caption'):
      self.pygameUI = PygameUI()

  @patch('pygame.init')
  @patch('pygame.display.set_mode')
  @patch('pygame.display.set_caption')
  def test_pygame_ui_initialization(self, mock_caption, mock_display, mock_init):
    ui = PygameUI()
    mock_init.assert_called_once()
    mock_display.assert_called_once()
    mock_caption.assert_called_once()
    self.assertIsNotNone(ui.screen)
    self.assertIsNotNone(ui.clock)

  @patch('pygame.init')
  @patch('pygame.display.set_mode')
  def test_pygame_ui_initialization_with_custom_size(self, mock_display, mock_init):
    ui = PygameUI(width=1024, height=768)
    mock_display.assert_called_with((1024, 768))

  def test_get_screen_dimensions(self):
    width, height = self.pygameUI.get_screen_size()
    self.assertIsInstance(width, int)
    self.assertIsInstance(height, int)
    self.assertGreater(width, 0)
    self.assertGreater(height, 0)

  @patch('pygame.draw.circle')
  @patch('pygame.draw.rect')
  def test_draw_board(self, mock_rect, mock_circle):
    mock_board = MagicMock()
    mock_board.points = [[] for _ in range(24)]
    mock_board.bar = {'white': [], 'black': []}
    mock_board.off = {'white': [], 'black': []}
    
    self.pygameUI.draw_board(mock_board)
    self.assertTrue(mock_rect.called or mock_circle.called)

  @patch('pygame.draw.circle')
  def test_draw_checker(self, mock_circle):
    mock_checker = MagicMock()
    mock_checker.color = "white"
    position = (100, 200)
    
    self.pygameUI.draw_checker(mock_checker, position)
    mock_circle.assert_called()

  @patch('pygame.draw.circle')
  def test_draw_checker_black(self, mock_circle):
    mock_checker = MagicMock()
    mock_checker.color = "black"
    position = (150, 250)
    
    self.pygameUI.draw_checker(mock_checker, position)
    mock_circle.assert_called()

  def test_get_point_coordinates(self):
    coords = self.pygameUI.get_point_coordinates(0)
    self.assertIsInstance(coords, tuple)
    self.assertEqual(len(coords), 2)
    
    coords_24 = self.pygameUI.get_point_coordinates(23)
    self.assertIsInstance(coords_24, tuple)

  def test_get_point_coordinates_invalid(self):
    with self.assertRaises((ValueError, IndexError)):
      self.pygameUI.get_point_coordinates(24)
    
    with self.assertRaises((ValueError, IndexError)):
      self.pygameUI.get_point_coordinates(-1)

  @patch('pygame.event.get')
  def test_handle_events_quit(self, mock_events):
    mock_event = MagicMock()
    mock_event.type = 256
    mock_events.return_value = [mock_event]
    
    result = self.pygameUI.handle_events()
    self.assertEqual(result, 'quit')

  @patch('pygame.event.get')
  def test_handle_events_mouse_click(self, mock_events):
    mock_event = MagicMock()
    mock_event.type = 1025
    mock_event.pos = (100, 200)
    mock_event.button = 1
    mock_events.return_value = [mock_event]
    
    result = self.pygameUI.handle_events()
    self.assertIsInstance(result, dict)
    self.assertIn('type', result)
    self.assertEqual(result['type'], 'click')

  @patch('pygame.event.get')
  def test_handle_events_key_press(self, mock_events):
    mock_event = MagicMock()
    mock_event.type = 768
    mock_event.key = 27
    mock_events.return_value = [mock_event]
    
    result = self.pygameUI.handle_events()
    self.assertIsInstance(result, dict)
    self.assertEqual(result['type'], 'key')

  def test_point_to_coordinates_conversion(self):
    coord_13 = self.pygameUI.point_to_coordinates(13)
    coord_24 = self.pygameUI.point_to_coordinates(24)
    
    coord_1 = self.pygameUI.point_to_coordinates(1)
    coord_12 = self.pygameUI.point_to_coordinates(12)
    
    self.assertIsInstance(coord_13, tuple)
    self.assertIsInstance(coord_1, tuple)

  def test_coordinates_to_point_conversion(self):
    point = self.pygameUI.coordinates_to_point((100, 100))
    self.assertIsInstance(point, (int, type(None)))
    
    if point is not None:
      self.assertIn(point, range(1, 25))

  @patch('pygame.font.Font')
  def test_display_text(self, mock_font):
    mock_font_instance = MagicMock()
    mock_font.return_value = mock_font_instance
    mock_surface = MagicMock()
    mock_font_instance.render.return_value = mock_surface
    
    self.pygameUI.display_text("Test message", (100, 100))
    mock_font_instance.render.assert_called()

  @patch('pygame.display.flip')
  def test_update_display(self, mock_flip):
    self.pygameUI.update_display()
    mock_flip.assert_called_once()

  @patch('pygame.time.Clock.tick')
  def test_control_frame_rate(self, mock_tick):
    self.pygameUI.tick(60)
    mock_tick.assert_called_with(60)

  def test_get_bar_coordinates(self):
    self.assertIsInstance(self.pygameUI.get_bar_coordinates("white"), tuple)
    self.assertIsInstance(self.pygameUI.get_bar_coordinates("black"), tuple)
    white_bar = self.pygameUI.get_bar_coordinates("white")
    black_bar = self.pygameUI.get_bar_coordinates("black")
    
    self.assertIsInstance(white_bar, tuple)
    self.assertIsInstance(black_bar, tuple)
    self.assertNotEqual(white_bar, black_bar)

  def test_get_off_board_coordinates(self):
    white_off = self.pygameUI.get_off_board_coordinates("white")
    black_off = self.pygameUI.get_off_board_coordinates("black")
    
    self.assertIsInstance(white_off, tuple)
    self.assertIsInstance(black_off, tuple)

  @patch('pygame.draw.polygon')
  def test_draw_point_triangle(self, mock_polygon):
    self.pygameUI.draw_point_triangle(5, "white")
    mock_polygon.assert_called()

  @patch('pygame.draw.rect')
  def test_draw_board_background(self, mock_rect):
    self.pygameUI.draw_board_background()
    mock_rect.assert_called()

  def test_highlight_point(self):
    result = self.pygameUI.highlight_point(5)
    # Should not raise exception
    self.assertIsNone(result)

    self.pygameUI.highlight_point(5)
    self.pygameUI.clear_highlights()
    # Should not raise exception

  @patch('pygame.draw.circle')
  def test_draw_dice(self, mock_circle):
    dice_values = [3, 5]
    position = (400, 300)
    
    self.pygameUI.draw_dice(dice_values, position)
    self.assertTrue(mock_circle.called)

  def test_get_dice_coordinates(self):
    coords = self.pygameUI.get_dice_coordinates()
    self.assertIsInstance(coords, tuple)
    self.assertEqual(len(coords), 2)

  @patch('pygame.draw.rect')
  def test_draw_player_info(self, mock_rect):
    mock_player = MagicMock()
    mock_player.name = "Player1"
    mock_player.color = "white"
    mock_player.checkers_off_board = 5
    
    self.pygameUI.draw_player_info(mock_player, (10, 10))
    self.assertTrue(mock_rect.called)

  def test_check_collision_with_point(self):
    collision = self.pygameUI.check_point_collision((100, 100))
    self.assertIsInstance(collision, (int, type(None)))

  def test_check_collision_with_bar(self):
    bar_coords = self.pygameUI.get_bar_coordinates("white")
    collision = self.pygameUI.check_bar_collision(bar_coords)
    self.assertIsInstance(collision, bool)

  @patch('pygame.draw.line')
  def test_draw_board_lines(self, mock_line):
    self.pygameUI.draw_board_lines()
    mock_line.assert_called()

  def test_scale_coordinates(self):
    scaled = self.pygameUI.scale_coordinates((100, 100), 1.5)
    self.assertIsInstance(scaled, tuple)
    self.assertEqual(scaled, (150, 150))

  @patch('pygame.Surface')
  def test_create_button(self, mock_surface):
    button = self.pygameUI.create_button("Start Game", (100, 50), (200, 100))
    self.assertIsNotNone(button)

  def test_is_valid_move_visual(self):
    result = self.pygameUI.is_valid_move_visual(1, 4)
    self.assertIsInstance(result, bool)

  @patch('pygame.mixer.Sound')
  def test_play_sound_effect(self, mock_sound):
    mock_sound_instance = MagicMock()
    mock_sound.return_value = mock_sound_instance
    
    self.pygameUI.play_sound("move")

  def test_animate_checker_move(self):
    start_pos = (100, 100)
    end_pos = (200, 200)
    
    result = self.pygameUI.animate_checker_move(start_pos, end_pos)
    self.assertIsNone(result)

  @patch('pygame.quit')
  def test_cleanup(self, mock_quit):
    self.pygameUI.cleanup()
    mock_quit.assert_called_once()

  def test_get_color_rgb(self):
    white_rgb = self.pygameUI.get_color_rgb("white")
    black_rgb = self.pygameUI.get_color_rgb("black")
    
    self.assertIsInstance(white_rgb, tuple)
    self.assertIsInstance(black_rgb, tuple)
    self.assertEqual(len(white_rgb), 3)
    self.assertEqual(len(black_rgb), 3)

if __name__ == "__main__":
  unittest.main()