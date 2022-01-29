import pygame
from tiles import Tile
from player import Player
from settings import tile_size, screen_width

class Level:
    def __init__(self, level_data, surface):
        # Screen where all the sprites in the level should be drawn
        self.display_surface = surface
        
        # Map of the level as a list
        self.setup_level(level_data)
        
        # Integer that is used with the tile class to simulate the amount
        # of the world movement
        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for cell_index, cell in enumerate(row):
                
                x = cell_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                
                elif cell == 'P':
                    player = Player((x, y))
                    self.player.add(player)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.directions.x

        if player_x < (screen_width * 0.25) and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width * 0.75) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def run(self):

        # Level
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        
        # Player
        self.player.update()
        self.player.draw(self.display_surface)
        self.scroll_x()