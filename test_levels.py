import unittest
from levels import LevelFactory, PlatformLevel, MazeLevel, PuzzleLevel

class TestLevelFactory(unittest.TestCase):
    def setUp(self):
        self.factory = LevelFactory()

    def test_create_platform_level(self):
        level = self.factory.create_level("platform")
        self.assertIsInstance(level, PlatformLevel)

    def test_create_maze_level(self):
        level = self.factory.create_level("maze")
        self.assertIsInstance(level, MazeLevel)

    def test_create_puzzle_level(self):
        level = self.factory.create_level("puzzle")
        self.assertIsInstance(level, PuzzleLevel)

    def test_create_invalid_level(self):
        level = self.factory.create_level("unknown")
        self.assertIsNone(level)

if __name__ == "__main__":
    unittest.main()
