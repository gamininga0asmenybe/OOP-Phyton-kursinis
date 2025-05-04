import os
import random
import pygame

from player import Player
from components import (
    Platform, FallingObstacle, Portal, Star
)
from config import (
    TILE_SIZE, PLAYER_IMAGE_PATH, PLAYER_WIDTH, PLAYER_HEIGHT,
    SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_SPEED, STAR_IMAGE_PATH, UI_FONT_PATH
    # HEART_IMAGE_PATH nebereikalingas šiam lygiui
)


class Level:
    """Base class for all game levels."""
    def __init__(self):
        self.player = None
        self.platforms = []
        self.components = []

    def update(self, keys):
        """Updates the level state, including player and components."""
        if not self.player:
            return None

        if hasattr(self, 'stars') and hasattr(self, 'collected'):
            for i, star in enumerate(self.stars):
                if not self.collected[i] and self.player.rect.colliderect(
                    star.rect
                ):
                    self.collected[i] = True
                    if star in self.components:
                        self.components.remove(star)

        if self.player:
            self.player.update(keys, self.platforms)

        for component in self.components:
            if hasattr(component, 'update') and callable(component.update):
                try:
                    component.update(self.platforms + self.components)
                except TypeError:
                    component.update()
        return None

    def draw(self, screen):
        """Draws all elements of the level."""
        for platform in self.platforms:
            platform.draw(screen)
        for component in self.components:
            component.draw(screen)
        if self.player:
            self.player.draw(screen)


class PlatformLevel(Level):
    """A level focused on platforming mechanics."""
    def __init__(self):
        super().__init__()
        self.platforms = [
            Platform(50, 490, 150, 10),
            Platform(250, 420, 100, 10),
            Platform(400, 340, 100, 10),
            Platform(150, 260, 100, 10),
            Platform(400, 160, 100, 10),
            Platform(500, 460, 100, 10),
            Platform(300, 180, 100, 0),
            Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20)
        ]
        self.portal = None
        self.portal_position = (700, 100)
        first_platform = self.platforms[0]
        self.start_x = first_platform.rect.centerx - (PLAYER_WIDTH // 2)
        self.start_y = first_platform.rect.top - PLAYER_HEIGHT
        self.player = Player(self.start_x, self.start_y, PLAYER_IMAGE_PATH)
        self.player.on_ground = True
        self.stars = [
            Star(295, 400),
            Star(445, 320),
            Star(185, 240),
            Star (550, 500)
        ]
        self.collected = [False] * len(self.stars)
        self.components.extend(self.stars)

    def update(self, keys):
        """Updates the platform level state."""
        status = super().update(keys)
        for star in self.stars:
             if hasattr(star, 'update') and callable(star.update):
                star.update()

        if all(self.collected) and self.portal is None:
            self.portal = Portal(*self.portal_position, 50, 50)
            self.components.append(self.portal)

        if self.portal and self.player.rect.colliderect(self.portal.rect):
            return "completed"
        return status

    def draw(self, screen):
        """Draws the platform level."""
        super().draw(screen)
        try:
            font_big = pygame.font.Font(UI_FONT_PATH, 28)
            font = pygame.font.Font(UI_FONT_PATH, 24)
        except (pygame.error, FileNotFoundError):
            font_big = pygame.font.SysFont(None, 28)
            font = pygame.font.SysFont(None, 30)

        message = "Surink žvaigždutes, kad atrastum portalą į sekantį lygį"
        text_surface = font_big.render(message, True, (255, 255, 0))
        screen.blit(
            text_surface,
            (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 10)
        )

        collected_text = f"Surinkta: {sum(self.collected)}/{len(self.collected)}"
        text = font.render(collected_text, True, (255, 255, 255))
        screen.blit(text, (10, 10))


class MazeLevel(Level):
    """A level represented as a top-down maze."""
    def __init__(self, maze_file="maze1.txt"):
        super().__init__()
        self.maze_data = []
        self.walls = []
        self.stars = []
        self.portal = None
        self.collected = []
        self.maze_player_width = int(TILE_SIZE * 0.7)
        self.maze_player_height = int(TILE_SIZE * 0.7)
        self.start_x, self.start_y = 0, 0
        self.end_x, self.end_y = -1, -1
        self.load_maze(maze_file)

        self.player = Player(
            self.start_x, self.start_y, PLAYER_IMAGE_PATH,
            self.maze_player_width, self.maze_player_height
        )
        self.components.extend(self.stars)

    def load_maze(self, filename):
        """Loads maze layout from a text file."""
        filepath = os.path.join(os.path.dirname(__file__), filename)
        try:
            with open(filepath, 'r') as f:
                self.maze_data = [line.strip() for line in f]
        except FileNotFoundError:
            print(f"Error: Maze file '{filepath}' not found.")
            self.maze_data = ["P*E"]
            self.walls.append(Platform(0, 0, TILE_SIZE, TILE_SIZE))
            return

        for r, row in enumerate(self.maze_data):
            for c, char in enumerate(row):
                x, y = c * TILE_SIZE, r * TILE_SIZE
                if char == '#':
                    wall = Platform(x, y, TILE_SIZE, TILE_SIZE)
                    self.walls.append(wall)
                    self.platforms.append(wall)
                elif char == 'P':
                    self.start_x, self.start_y = x, y
                elif char == '*':
                    star = Star(x + TILE_SIZE // 2, y + TILE_SIZE // 2)
                    self.stars.append(star)
                elif char == 'E':
                    self.end_x, self.end_y = x, y
        self.collected = [False] * len(self.stars)

    def draw(self, screen):
        """Draws the maze level with camera offset."""
        if self.player:
            offset_x = self.player.rect.centerx - SCREEN_WIDTH // 2
            offset_y = self.player.rect.centery - SCREEN_HEIGHT // 2
        else:
            offset_x, offset_y = 0, 0

        for wall in self.walls:
            screen.blit(wall.image, wall.rect.move(-offset_x, -offset_y))

        for component in self.components:
             if hasattr(component, 'rect') and hasattr(component, 'image'):
                 screen.blit(
                    component.image, component.rect.move(-offset_x, -offset_y)
                 )

        if self.player:
            screen.blit(
                self.player.image, self.player.rect.move(-offset_x, -offset_y)
            )

        try:
            font = pygame.font.Font(UI_FONT_PATH, 24)
        except (pygame.error, FileNotFoundError):
            font = pygame.font.SysFont(None, 30)

        collected_text = f"Surinkta: {sum(self.collected)}/{len(self.collected)}"
        text = font.render(collected_text, True, (255, 255, 255))
        screen.blit(text, (10, 10))

    def update(self, keys):
        """Updates the maze level state (player movement, collection)."""
        if self.player:
            old_x, old_y = self.player.rect.topleft
            self.player.speed_x = 0
            self.player.speed_y = 0
            if keys[pygame.K_LEFT]:
                self.player.speed_x = -PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                self.player.speed_x = PLAYER_SPEED
            if keys[pygame.K_UP]:
                self.player.speed_y = -PLAYER_SPEED
            if keys[pygame.K_DOWN]:
                self.player.speed_y = PLAYER_SPEED

            self.player.rect.x += self.player.speed_x
            for wall in self.walls:
                if self.player.rect.colliderect(wall.rect):
                    self.player.rect.x = old_x
                    break

            self.player.rect.y += self.player.speed_y
            for wall in self.walls:
                if self.player.rect.colliderect(wall.rect):
                    self.player.rect.y = old_y
                    break

            for i, star in enumerate(self.stars):
                if not self.collected[i] and self.player.rect.colliderect(
                    star.rect
                ):
                    self.collected[i] = True
                    if star in self.components:
                        self.components.remove(star)

        for component in self.components:
            if hasattr(component, 'update') and callable(component.update):
                try:
                    component.update()
                except TypeError:
                    pass 

        
        if self.end_x != -1 and all(self.collected) and self.portal is None:
            self.portal = Portal(self.end_x, self.end_y, TILE_SIZE, TILE_SIZE)
            self.components.append(self.portal)
            print("Portal created in maze!")

       
        if self.portal and self.player and self.player.rect.colliderect(
            self.portal.rect
        ):
            print("Maze level completed!")
            return "completed"

        return None


class PuzzleLevel(Level):
    """A level combining platforming with puzzle elements and hazards."""
    def __init__(self):
        super().__init__()
        self.start_pos = (100, 500 - PLAYER_HEIGHT)
        self.player = Player(*self.start_pos, PLAYER_IMAGE_PATH)
        self.platforms = [Platform(0, 580, SCREEN_WIDTH, 20)] 

        self.total_lives = 3
        self.lives = self.total_lives


        self.obstacles = pygame.sprite.Group()
        for _ in range(7):
            obstacle = FallingObstacle(speed=random.randint(3, 6))
            self.obstacles.add(obstacle)
            self.components.append(obstacle)

        
        self.falling_stars = pygame.sprite.Group()
        for _ in range(1): 
            star = Star(0, 0, falling=True, speed=random.randint(2, 5))
            self.falling_stars.add(star)
            self.components.append(star)

        self.collected_falling_stars = 0
        self.star_goal = 3 

        # Sukuriame raudoną kvadratuką gyvybėms rodyti
        self.heart_image = pygame.Surface((25, 25)) # Kvadratuko dydis
        self.heart_image.fill((255, 0, 0)) # Raudona spalva

    def update(self, keys):
        """Updates the puzzle level state."""
        super().update(keys) 

        
        if self.player:
            collided_stars = pygame.sprite.spritecollide(
                self.player, self.falling_stars, False
            )
            for star in collided_stars:
                self.collected_falling_stars += 1
                print(
                   f"Collected star! Total: {self.collected_falling_stars}"
                )
                star.reset_pos() 
                if self.collected_falling_stars >= self.star_goal:
                    
                    return "show_end_message"

       
        if self.player:
            collided_obstacles = pygame.sprite.spritecollide(
                self.player, self.obstacles, False
            )
            if collided_obstacles:
                self.lives -= 1
                print(f"Hit! Lives left: {self.lives}")
                for obstacle in collided_obstacles:
                    obstacle.reset_pos() 
                if self.lives <= 0:
                    print("Game Over! Restarting level.")
                    return "restart" 
                else:
                    self.player.reset_position(*self.start_pos)

        return None

    def draw(self, screen):
        """Draws the puzzle level and UI elements."""
        super().draw(screen) 

        try:
            font = pygame.font.Font(UI_FONT_PATH, 28)
            font_instr = pygame.font.Font(UI_FONT_PATH, 28)
        except (pygame.error, FileNotFoundError):
            font = pygame.font.SysFont(None, 30)
            font_instr = pygame.font.SysFont(None, 30)

        # Piešiame širdeles vietoje teksto
        heart_x_start = SCREEN_WIDTH - 10 - self.heart_image.get_width()
        for i in range(self.lives):
            heart_x = heart_x_start - i * (self.heart_image.get_width() + 5) # 5 yra tarpas tarp širdelių
            screen.blit(self.heart_image, (heart_x, 10))
            
        stars_text_str = f"Žvaigždės: {self.collected_falling_stars}/{self.star_goal}"
        stars_text = font.render(stars_text_str, True, (255, 255, 0))
        screen.blit(stars_text, (10, 10))

        instr_text_str = "Rink žvaigždes!"
        instr_text = font_instr.render(instr_text_str, True, (255, 255, 0))
        screen.blit(
            instr_text,
            (SCREEN_WIDTH // 2 - instr_text.get_width() // 2, 10)
        )


class LevelFactory:
    """Factory class to create different types of levels."""
    def create_level(self, level_type):
        """Creates a level instance based on the type."""
        if level_type == "platform":
            return PlatformLevel()
        elif level_type == "maze":
            return MazeLevel()
        elif level_type == "puzzle":
            return PuzzleLevel()
        print(f"Warning: Unknown level type '{level_type}' requested.")
        return None