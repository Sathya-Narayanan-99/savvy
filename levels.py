import pygame
from tiles import Tile, StaticTile, Crate
from player import Player
from settings import tile_size, screen_width
from particles import Particles
from support import import_csv_layout, partition_tile_set

class Level:
    def __init__(self, level_data, surface):
        # Screen where all the sprites in the level should be drawn
        self.display_surface = surface
        
        # Map of the level as a list
        self.setup_level(level_data)
        
        # Terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        
        # Grass
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # Crate
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprite = self.create_tile_group(crate_layout, 'crates')

        # Integer that is used with the tile class to simulate the amount
        # of the world movement
        self.world_shift = -5

        # x position when a collision occurs horizontally
        self.current_x = 0

        # Dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    def create_jump_particles(self, pos):
        
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        
        jump_particle_sprite = Particles(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def create_fall_particle(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite:
            pos = self.player.sprite.rect.midbottom
            
            if self.player.sprite.facing_right:
                pos -= pygame.math.Vector2(10, 15)
            else:
                pos += pygame.math.Vector2(10, -15)
            
            fall_dust_particle = Particles(pos, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':

                        terrain_tile_list = partition_tile_set("resources/graphics/terrain/terrain_tiles.png")
                        tile_surface = terrain_tile_list[int(val)]
                        
                        sprite = StaticTile((x, y), tile_size, tile_surface)

                    if type == 'grass':

                        grass_tile_list = partition_tile_set("resources/graphics/decoration/grass/grass.png")
                        tile_surface = grass_tile_list[int(val)]

                        sprite = StaticTile((x, y), tile_size, tile_surface)

                    if type == 'crates':

                        sprite = Crate((x, y), tile_size)
                    
                    sprite_group.add(sprite)

        return sprite_group

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
                    player = Player((x, y), self.display_surface, self.create_jump_particles)
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
                    player.on_left = True
                    self.current_x = player.rect.left

                # If the player collides to the left of the tile change the
                # player's right position to tile's left position
                elif player.directions.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        
        if player.on_left and (player.rect.left < self.current_x or player.directions.x >= 0):
            player.on_left = False
        
        if player.on_right and (player.rect.right > self.current_x or player.directions.x <= 0):
            player.on_right = False

    # Function that implements vertical movement of the player and
    # vertical collision of the player with the tiles
    def vertical_movement_collision(self):
        player = self.player.sprite
        
        player.apply_gravity()
        
        # Iterating through all the tiles sprite to check for collision
        for sprite in self.tiles.sprites():
            
            # Condition to check for collision
            if sprite.rect.colliderect(player.rect):
                
                # If the player collides to the top of the tile change the
                # player's bottom position to tile's top position
                if player.directions.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.directions.y = 0
                    player.on_ground = True

                # If the player collides to the bottom of the tile change the
                # player's top position to tile's top position
                elif player.directions.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.directions.y = 0
                    player.on_ceiling = False

        if player.on_ground and player.directions.y < 0 or player.directions.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.directions.y > 0:
            player.on_celing = False

    def run(self):

        # Dust
        #self.dust_sprite.update(self.world_shift)
        #self.dust_sprite.draw(self.display_surface)

        # Level
        #self.tiles.update(self.world_shift)
        #self.tiles.draw(self.display_surface)
        #self.scroll_x()
        
        # Terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # Grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # Crate
        self.crate_sprite.update(self.world_shift)
        self.crate_sprite.draw(self.display_surface)

        # Player
        # self.player.update()
        # self.horizontal_movement_collision()
        # self.get_player_on_ground()
        # self.vertical_movement_collision()
        # self.create_fall_particle()
        # self.player.draw(self.display_surface)
        