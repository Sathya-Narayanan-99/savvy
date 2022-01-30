import pygame
from random import randint
from tiles import AnimatedTile

class Enemy(AnimatedTile):
    def __init__(self, position, size):
        super().__init__(position, size, 'resources/graphics/enemy/run')
        self.rect.y += 20
        self.speed = randint(3, 5)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def reverse_direction(self):
        self.speed *= -1

    def update(self, x_shift):
        super().update(x_shift)
        self.reverse_image()
        self.move()
