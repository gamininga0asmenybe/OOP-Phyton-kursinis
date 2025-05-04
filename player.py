import pygame
from config import (
    PLAYER_SPEED,
    PLAYER_GRAVITY,
    PLAYER_JUMP_STRENGTH,
    PLAYER_MAX_FALL_SPEED,
    SCREEN_WIDTH,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, width=None, height=None):
        super().__init__()
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Warning: Could not load image '{image_path}': {e}")
            print("Creating a default red square instead.")
            original_image = pygame.Surface((width or 30, height or 40))
            original_image.fill((255, 0, 0))

        if width is None or height is None:
            self.image = original_image
        else:
            self.image = pygame.transform.scale(original_image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = float(x)
        self.y = float(y)
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = PLAYER_GRAVITY
        self.on_ground = False

    def update(self, keys, platforms):
        self.handle_input(keys)
        self.apply_gravity()
        self.move_and_collide(platforms)

    def handle_input(self, keys):
        self.speed_x = 0
        if keys[pygame.K_LEFT]:
            self.speed_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.speed_x = PLAYER_SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def apply_gravity(self):
        self.speed_y += self.gravity
        if self.speed_y > PLAYER_MAX_FALL_SPEED:
            self.speed_y = PLAYER_MAX_FALL_SPEED

    def move(self):
        self.x += self.speed_x
        self.rect.x = int(self.x)
        self.y += self.speed_y
        self.rect.y = int(self.y)

    def move_and_collide(self, platforms):
        self.x += self.speed_x
        self.rect.x = int(self.x)
        self.check_collision_x(platforms)

        self.y += self.speed_y
        self.rect.y = int(self.y)
        self.check_collision_y(platforms)

    def jump(self):
        self.speed_y = PLAYER_JUMP_STRENGTH
        self.on_ground = False

    def check_collision_x(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.speed_x > 0:
                    self.rect.right = platform.rect.left
                elif self.speed_x < 0:
                    self.rect.left = platform.rect.right
                self.x = float(self.rect.x)
                self.speed_x = 0

    def check_collision_y(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.speed_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.y = float(self.rect.y)
                    self.on_ground = True
                elif self.speed_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.y = float(self.rect.y)
                self.speed_y = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def reset_position(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.rect.topleft = (int(self.x), int(self.y))
        self.speed_x = 0
        self.speed_y = 0
        self.on_ground = False
