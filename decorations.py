import pygame
from pygame import sprite
from settings import vertical_tile_count, screen_width, tile_size
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint

class Sky:
    def __init__(self, horizon, style = 'level'):
        self.top = pygame.image.load('resources/graphics/decoration/sky/sky_top.png').convert()
        self.middle = pygame.image.load('resources/graphics/decoration/sky/sky_middle.png').convert()
        self.bottom = pygame.image.load('resources/graphics/decoration/sky/sky_bottom.png').convert()
        self.horizon = horizon
        self.style = style

        # Screen
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))

        if self.style == 'overworld':
            palm_surfaces = import_folder('resources/graphics/overworld/palms')
            self.palms = []

            for surface in [choice(palm_surfaces) for image in range(10)]:
                x = randint(0, screen_width)
                y = self.horizon * tile_size + randint(50, 100)
                rect = surface.get_rect(midbottom = (x,y))
                self.palms.append((surface, rect))

            cloud_surfaces = import_folder('resources/graphics/overworld/clouds')
            self.clouds = []

            for surface in [choice(cloud_surfaces) for image in range(10)]:
                x = randint(0, screen_width)
                y = self.horizon * tile_size - randint(50, 500)
                rect = surface.get_rect(midbottom = (x,y))
                self.clouds.append((surface, rect))
                
    def draw(self, surface):
        for row in range(vertical_tile_count):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))

        if self.style == 'overworld':
            for palm in self.palms:
                surface.blit(palm[0], palm[1])
            
            for cloud in self.clouds:
                surface.blit(cloud[0], cloud[1])

class Water:
    def __init__(self, top, level_width):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = (level_width + screen_width * 2) // water_tile_width
        self.water_sprite = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile((x, y), 192, 'resources/graphics/decoration/water')
            self.water_sprite.add(sprite)
            
    def draw(self, surface, x_shift):
        self.water_sprite.update(x_shift)
        self.water_sprite.draw(surface)

class Cloud:
    def __init__(self, horizon, level_width, cloud_number):
        cloud_surf_list = import_folder('resources/graphics/decoration/clouds')
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile((x, y), 0, cloud)
            self.cloud_sprites.add(sprite)
    
    def draw(self, surface, x_shift):
        self.cloud_sprites.update(x_shift)
        self.cloud_sprites.draw(surface)