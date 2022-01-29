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
        
        # Iteration through the level list to get its x and y position
        for row_index, row in enumerate(layout):
            for cell_index, cell in enumerate(row):
                
                # Multiplying the positions to scale it with respect to the size of the tile
                x = cell_index * tile_size
                y = row_index * tile_size

                # Condition to check if current cell consists a tile
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                
                # Condition to check if current cell consists player
                elif cell == 'P':
                    player = Player((x, y))
                    self.player.add(player)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.directions.x

        # Condition to move the world left side instead of the player when the 
        # player reaches 25% of the screen to the left
        if player_x < (screen_width * 0.25) and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        # Condition to move the world right side instead of the player when the 
        # player reaches 75% of the screen to the right
        elif player_x > (screen_width * 0.75) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        # Condition to move the player and not the world
        else:
            self.world_shift = 0
            player.speed = 8

    # Function that implements horizontal movement of the player and
    # horizontal collision of the player with the tiles
    def horizontal_movement_collision(self):
        player = self.player.sprite
        
        # Moves the player horizontally based on the player's direction
        player.rect.x += player.directions.x * player.speed

        # Iterating through all the tiles sprite to check for collision
        for sprite in self.tiles.sprites():
            
            # Condition to check for collision
            if sprite.rect.colliderect(player.rect):
                
                # If the player collides to the right of the tile change the
                # player's left position to tile's right position
                if player.directions.x < 0:
                    player.rect.left = sprite.rect.right
                # If the player collides to the left of the tile change the
                # player's right position to tile's left position
                elif player.directions.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.directions.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.directions.y = 0
                elif player.directions.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.directions.y = 0

    def run(self):

        # Level
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        
        # Player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        