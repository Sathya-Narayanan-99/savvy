import pygame
from game_data import levels

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, is_available):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        self.rect = self.image.get_rect(center = pos)
        
        if is_available:
            self.image.fill('red')
        else:
            self.image.fill('grey')

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)

class Overworld:
    def __init__(self, start_level, max_level, surface):

        # Setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level

        # sprites
        self.setup_nodes()
        self.setup_icon()
    
    def setup_nodes(self):
        self.nodes_sprite = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):

            if index < self.max_level:
                sprite = Node(node_data['node_pos'], True)
            else:
                sprite = Node(node_data['node_pos'], False)
            
            self.nodes_sprite.add(sprite)

    def draw_paths(self):
        points = [node['node_pos'] for index, node in enumerate(levels.values()) if index < self.max_level]
        pygame.draw.lines(self.display_surface, 'red', False, points, 6)

    def setup_icon(self):
        self.icon_sprite = pygame.sprite.GroupSingle()
        position = self.nodes_sprite.sprites()[self.current_level].rect.center
        sprite = Icon(position)
        self.icon_sprite.add(sprite)

    def run(self):
        self.nodes_sprite.draw(self.display_surface)
        self.draw_paths()
        self.icon_sprite.draw(self.display_surface)