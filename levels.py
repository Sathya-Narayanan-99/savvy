import pygame
from pygame import sprite
from tiles import Tile, StaticTile, Crate, Coin, Palm
from player import Player
from enemy import Enemy
from settings import tile_size, screen_width, screen_height
from particles import Particles
from decorations import Sky, Water, Cloud
from support import import_csv_layout, partition_tile_set

class Level:
    def __init__(self, level_data, surface):
        # Screen where all the sprites in the level should be drawn
        self.display_surface = surface
        
        # Map of the level as a list
        self.setup_level(level_data)


        # Integer that is used with the tile class to simulate the amount
        # of the world movement
        self.world_shift = -3

        # x position when a collision occurs horizontally
        self.current_x = 0
        
        # Player
        player_layout = import_csv_layout(level_data['player'])
        self.player_sprite = pygame.sprite.GroupSingle()
        self.goal_sprite = pygame.sprite.GroupSingle()
        self.player_setup(player_layout) 

        # Terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        
        # Grass
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # Crate
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprite = self.create_tile_group(crate_layout, 'crates')

        # Coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprite = self.create_tile_group(coin_layout, 'coins')

        # Fg_palms
        fg_palm_layout = import_csv_layout(level_data['fg_palms'])
        self.fg_palm_sprite = self.create_tile_group(fg_palm_layout, 'fg_palms')

        # Bg_palms
        bg_palm_layout = import_csv_layout(level_data['bg_palms'])
        self.bg_palm_sprite = self.create_tile_group(bg_palm_layout, 'bg_palms')

        # Enemies
        enemies_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprite = self.create_tile_group(enemies_layout, 'enemies')

        # Constraints
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraints_sprite = self.create_tile_group(constraints_layout, 'constraints')

        # Decorations
        self.sky = Sky(7)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width)
        self.cloud = Cloud(400 , level_width, 20)

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

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                
                x = col_index * tile_size
                y = row_index * tile_size

                if val == '0':
                    pass # player goes here
                if val == '1':
                    hat_surface = pygame.image.load('resources/graphics/character/hat.png')
                    sprite = StaticTile((x,y), tile_size, hat_surface)
                    self.goal_sprite.add(sprite)

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

                    if type == 'coins':
                        if val == '0': 
                            sprite = Coin((x,y), tile_size, 'resources/graphics/coins/gold')
                        elif val == '1':
                            sprite = Coin((x,y), tile_size, 'resources/graphics/coins/silver')
                    
                    if type == 'fg_palms':
                        if val == '0':
                            sprite = Palm((x, y), tile_size, 'resources/graphics/terrain/palm_small')
                        elif val == '1':
                            sprite = Palm((x, y), tile_size, 'resources/graphics/terrain/palm_large')

                    if type == 'bg_palms':
                        sprite = Palm((x, y), tile_size, 'resources/graphics/terrain/palm_bg')

                    if type == 'enemies':
                        sprite = Enemy((x, y), tile_size)

                    if type == 'constraints':
                        sprite = Tile((x, y), tile_size)

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

    def enemy_collision(self):
        for enemy in self.enemies_sprite.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints_sprite, False):
                enemy.reverse_direction()

    def run(self):

        # Dust
        #self.dust_sprite.update(self.world_shift)
        #self.dust_sprite.draw(self.display_surface)

        # Level
        #self.tiles.update(self.world_shift)
        #self.tiles.draw(self.display_surface)
        #self.scroll_x()

        # Sky
        self.sky.draw(self.display_surface)
        self.cloud.draw(self.display_surface, self.world_shift)
        
        # Bg_palms
        self.bg_palm_sprite.update(self.world_shift)
        self.bg_palm_sprite.draw(self.display_surface)

        # Fg_palms
        self.fg_palm_sprite.update(self.world_shift)
        self.fg_palm_sprite.draw(self.display_surface)

        # Enemy
        self.enemies_sprite.update(self.world_shift)
        self.constraints_sprite.update(self.world_shift)
        self.enemy_collision()
        self.enemies_sprite.draw(self.display_surface)

        # Terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # Crate
        self.crate_sprite.update(self.world_shift)
        self.crate_sprite.draw(self.display_surface)

        # Grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # Coins
        self.coin_sprite.update(self.world_shift)
        self.coin_sprite.draw(self.display_surface)

        # Player
        self.goal_sprite.update(self.world_shift)
        self.goal_sprite.draw(self.display_surface)

        # Water
        self.water.draw(self.display_surface, self.world_shift)

        # Player
        # self.player.update()
        # self.horizontal_movement_collision()
        # self.get_player_on_ground()
        # self.vertical_movement_collision()
        # self.create_fall_particle()
        # self.player.draw(self.display_surface)
        