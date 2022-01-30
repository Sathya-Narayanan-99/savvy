import pygame
from support import import_folder


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

class AnimatedTile(Tile):
    def __init__(self, position, size, path):
        super().__init__(position, size)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.animation_speed = 0.15

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        
        self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        super().update(x_shift)
        self.animate()

class Coin(AnimatedTile):
    def __init__(self, position, size, path):
        super().__init__(position, size, path)
        new_pos = (position[0] + size // 2, position[1] + size // 2 )
        self.rect = self.image.get_rect(center = new_pos)

class Palm(AnimatedTile):
    def __init__(self, position, size, path):
        super().__init__(position, size, path)
        
        if path == 'resources/graphics/terrain/palm_small':
            position = (position[0], position[1] - 38)
        elif path == 'resources/graphics/terrain/palm_large':
            position = (position[0], position[1] - 70)
        elif path == 'resources/graphics/terrain/palm_bg':
            position = (position[0], position[1] - 60)
        
        self.rect.topleft = position