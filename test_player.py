import unittest
import pygame
from player import Player
from config import PLAYER_JUMP_STRENGTH

class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((100, 100))
        self.player = Player(10, 10, image_path="player_image.png", width=30, height=40)

    def test_jump(self):
        self.player.on_ground = True
        self.player.jump()
        self.assertEqual(self.player.speed_y, PLAYER_JUMP_STRENGTH)
        self.assertFalse(self.player.on_ground)

    def test_reset_position(self):
        self.player.reset_position(50, 60)
        self.assertEqual(self.player.rect.x, 50)
        self.assertEqual(self.player.rect.y, 60)
        self.assertEqual(self.player.speed_x, 0)
        self.assertEqual(self.player.speed_y, 0)

    def tearDown(self):
        pygame.quit()

if __name__ == "__main__":
    unittest.main()
