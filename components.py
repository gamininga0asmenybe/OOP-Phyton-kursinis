import os
import random
import pygame
import colorsys

from config import SCREEN_WIDTH, SCREEN_HEIGHT


class Component(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Platform(Component):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((0, 0, 255))
        self.visible = True


class FallingObstacle(pygame.sprite.Sprite):
    def __init__(self, width=5, height=20, speed=4):
        super().__init__()
        self.width = width
        self.height = height
        self.speed = speed
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.reset_pos()

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_pos()

    def reset_pos(self):
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.width)
        self.rect.y = random.randrange(-300, -self.height)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Portal(Component):
    def __init__(self, x, y, width, height, color_change_speed=0.2):
        super().__init__(x, y, width, height)
        self.hue = 0
        self.saturation = 1.0
        self.value = 1.0
        self.color_change_speed = color_change_speed
        self.last_update_time = pygame.time.get_ticks()
        self._update_color()

    def _update_color(self):
        rgb_color = tuple(
            int(c * 255)
            for c in colorsys.hsv_to_rgb(self.hue / 360.0, self.saturation, self.value)
        )
        self.image.fill(rgb_color)

    def update(self):
        current_time = pygame.time.get_ticks()
        delta_time_seconds = (current_time - self.last_update_time) / 1000.0
        self.last_update_time = current_time
        self.hue = (self.hue + self.color_change_speed * 360 * delta_time_seconds) % 360
        self._update_color()


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, falling=False, speed=3):
        super().__init__()
        star_image_path = os.path.join(os.path.dirname(__file__), "star_image.png")
        try:
            from config import STAR_IMAGE_PATH
            star_image_path = STAR_IMAGE_PATH
        except ImportError:
            pass

        try:
            self.original_image = pygame.image.load(star_image_path).convert_alpha()
        except pygame.error as e:
            print(f"Warning: Could not load star image '{star_image_path}': {e}")
            self.original_image = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(self.original_image, (255, 255, 0), (15, 15), 15)

        self.target_size = (35, 35) # Padidintas dydis
        self.image = pygame.transform.scale(self.original_image, self.target_size)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = random.randint(0, 360)
        self.rotation_speed = random.uniform(0.5, 2.0)
        self.falling = falling
        self.speed = speed if falling else 0

        if self.falling:
            self.reset_pos()

    def reset_pos(self):
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-400, -self.rect.height)

    def update(self):
        self.angle = (self.angle + self.rotation_speed) % 360
        rotated_image = pygame.transform.rotate(
            pygame.transform.scale(self.original_image, self.target_size), self.angle
        )
        old_center = self.rect.center
        self.image = rotated_image
        self.rect = self.image.get_rect(center=old_center)

        if self.falling:
            self.rect.y += self.speed
            if self.rect.top > SCREEN_HEIGHT:
                self.reset_pos()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
