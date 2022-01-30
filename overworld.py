import pygame
from game_data import levels

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, is_available, icon_speed):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        self.rect = self.image.get_rect(center = pos)

        self.icon_detection_zone = pygame.Rect(self.rect.centerx - icon_speed //2, self.rect.centery - icon_speed //2, icon_speed, icon_speed)
        
        if is_available:
            self.image.fill('red')
        else:
            self.image.fill('grey')

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.position = pos
        self.image = pygame.Surface((20,20))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.position

class Overworld:
    def __init__(self, start_level, max_level, surface):

        # Setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level

        # icon movement
        self.is_moving = False
        self.movement_direction = pygame.math.Vector2(0,0)
        self.speed = 8

        # sprites
        self.setup_nodes()
        self.setup_icon()
    
    def setup_nodes(self):
        self.nodes_sprite = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):

            if index < self.max_level:
                sprite = Node(node_data['node_pos'], True, self.speed)
            else:
                sprite = Node(node_data['node_pos'], False, self.speed)
            
            self.nodes_sprite.add(sprite)

    def draw_paths(self):
        points = [node['node_pos'] for index, node in enumerate(levels.values()) if index < self.max_level]
        pygame.draw.lines(self.display_surface, 'red', False, points, 6)

    def setup_icon(self):
        self.icon_sprite = pygame.sprite.GroupSingle()
        position = self.nodes_sprite.sprites()[self.current_level].rect.center
        sprite = Icon(position)
        self.icon_sprite.add(sprite)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if not self.is_moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level - 1:
                self.movement_direction = self.get_movement_data('next')
                self.current_level += 1
                self.is_moving = True

            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.movement_direction = self.get_movement_data('prev')
                self.current_level -= 1
                self.is_moving = True
    
    def get_movement_data(self, direction):
        pos = self.nodes_sprite.sprites()[self.current_level].rect.center
        start = pygame.math.Vector2(pos)
        
        if direction == 'next':
            pos = self.nodes_sprite.sprites()[self.current_level + 1].rect.center
        else:
            pos = self.nodes_sprite.sprites()[self.current_level - 1].rect.center
        end = pygame.math.Vector2(pos)

        return (end - start).normalize()

    def update_icon(self):
        if self.is_moving and self.movement_direction:
            self.icon_sprite.sprite.position += self.movement_direction * self.speed
            target_node = self.nodes_sprite.sprites()[self.current_level]

            if target_node.icon_detection_zone.collidepoint(self.icon_sprite.sprite.position):
                self.is_moving = False
                self.movement_direction = pygame.math.Vector2(0,0)

    def run(self):
        self.get_input()
        self.nodes_sprite.draw(self.display_surface)
        self.icon_sprite.update()
        self.draw_paths()
        self.update_icon()
        self.icon_sprite.draw(self.display_surface)