import pygame
from pygame import surface

# Tile sprite class
class Tile(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        # Image of the tile
        self.image = pygame.Surface((size, size))
        # Filling the tile colour
        self.image.fill('grey')
        # Getting the rect of the tile image
        self.rect = self.image.get_rect(topleft = position)
    
    # Method that shifts the tile along the x-axis to simulate world movement
    def update(self, x_shift):
        self.rect.x += x_shift


class StaticTile(Tile):
    def __init__(self, position, size, surface):
        super().__init__(position, size)
        self.image = surface

class Crate(StaticTile):
    def __init__(self, position, size):
        surface = pygame.image.load("resources/graphics/terrain/crate.png").convert_alpha()
        super().__init__(position, size, surface)
        new_pos = (position[0], position[1] + size)
        self.rect = self.image.get_rect(bottomleft = new_pos)