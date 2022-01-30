from os import walk
from csv import reader
import pygame
from settings import tile_size

def import_folder(path):
    surface_list = []
    
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
    return terrain_map

def partition_tile_set(path):
    surface = pygame.image.load(path)

    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    partitioned_tile = []

    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size

            new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, tile_size, tile_size))
            partitioned_tile.append(new_surf)

    return partitioned_tile