import pygame
from pygame.constants import K_RIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = position)

        # Player Movement
        self.speed = 8
        self.directions = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.jump_speed = -16
    
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.directions.x = 1
        elif keys[pygame.K_LEFT]:
            self.directions.x = -1
        else:
            self.directions.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def apply_gravity(self):
        self.directions.y += self.gravity
        self.rect.y += self.directions.y

    def jump(self):
        self.directions.y = self.jump_speed

    def update(self):
        self.get_input()
        self.rect.x += self.directions.x * self.speed
        self.apply_gravity()