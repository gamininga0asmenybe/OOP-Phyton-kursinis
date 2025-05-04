import unittest
from components import Portal, Platform, Star, FallingObstacle

class TestPortal(unittest.TestCase):
    def test_portal_size(self):
        portal = Portal(0, 0, 40, 60)
        self.assertEqual(portal.rect.width, 40)
        self.assertEqual(portal.rect.height, 60)

class TestPlatform(unittest.TestCase):
    def test_platform_position(self):
        platform = Platform(10, 20, 100, 15)
        self.assertEqual(platform.rect.topleft, (10, 20))

class TestStar(unittest.TestCase):
    def test_star_position(self):
        star = Star(300, 150)
        self.assertEqual((star.rect.centerx, star.rect.centery), (300, 150))

class TestFallingObstacle(unittest.TestCase):
    def test_obstacle_falling(self):
        obstacle = FallingObstacle(speed=4)
        start_y = obstacle.rect.y
        obstacle.update()
        self.assertGreater(obstacle.rect.y, start_y)

if __name__ == "__main__":
    unittest.main()
