import pygame

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