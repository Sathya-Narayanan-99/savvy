import pygame
import sys
from game_data import levels, menus
from decorations import Sky
from support import import_folder
from random import randint

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, is_available, icon_speed, path):
        super().__init__()
        
        self.frames = import_folder(path)
        self.frame_index = 0
        self.animation_speed = 0.15

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.is_available = is_available

        self.icon_detection_zone = pygame.Rect(self.rect.centerx - icon_speed //2, self.rect.centery - icon_speed //2, icon_speed, icon_speed)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.is_available:
            self.animate()
        else:
            tint_image = self.image.copy()
            tint_image.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_image, (0,0))

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.position = pos
        self.image = pygame.image.load('resources/graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.position

class Star(pygame.sprite.Sprite):
    def __init__(self, pos, is_available):
        super().__init__()
        self.frames = import_folder('resources/graphics/star')
        self.is_available = is_available

        if self.is_available:
            self.frame_index = randint(0, len(self.frames) - 1)
        else:
            self.frame_index = 0

        self.animation_speed = 0.15

        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(topleft = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.is_available:
            self.animate()
        else:
            tint_image = self.image.copy()
            tint_image.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_image, (0,0))

class Menu:
    def __init__(self, surface):
        
        # Setup
        self.display_surface = surface

        # icon movement
        self.is_moving = False
        self.movement_direction = pygame.math.Vector2(0,0)
        self.speed = 8

        # sprites
        self.sky = Sky(8, 'overworld')

        # timer
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.enable_input_time = 500

    def draw_paths(self, max_nodes, location):
        if location == 'overworld':
            if max_nodes > 0:
                points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= max_nodes]
                pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)
        else:
            points = [node['node_pos'] for node in menus.values()]
            pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)

    def setup_icon(self, node_sprite_list, current_node):
        self.icon_sprite = pygame.sprite.GroupSingle()
        position = node_sprite_list[current_node].rect.center
        sprite = Icon(position)
        self.icon_sprite.add(sprite)

    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.enable_input_time:
                self.allow_input = True

    def get_movement_data(self, node_list, current_node, direction):
        pos = node_list[current_node].rect.center
        start = pygame.math.Vector2(pos)
        
        if direction == 'next':
            pos = node_list[current_node + 1].rect.center
        else:
            pos = node_list[current_node - 1].rect.center
        end = pygame.math.Vector2(pos)

        return (end - start).normalize()

    def update_icon(self, node_list, current_node):
        if self.is_moving and self.movement_direction:
            self.icon_sprite.sprite.position += self.movement_direction * self.speed
            target_node = node_list[current_node]

            if target_node.icon_detection_zone.collidepoint(self.icon_sprite.sprite.position):
                self.is_moving = False
                self.movement_direction = pygame.math.Vector2(0,0)

class Overworld(Menu):
    def __init__(self, start_level, max_level, surface, create_level):
        super().__init__(surface)
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        # Sprites
        self.nodes_sprite = self.setup_nodes()
        super().setup_icon(self.nodes_sprite.sprites(), self.current_level)
        self.star_sprite = self.setup_star()

    def setup_nodes(self):
        nodes_sprite = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            path = node_data['node_graphics']
            if index <= self.max_level:
                sprite = Node(node_data['node_pos'], True, self.speed, path)
            else:
                sprite = Node(node_data['node_pos'], False, self.speed, path)
            
            nodes_sprite.add(sprite)
        
        return nodes_sprite

    def setup_star(self):
        star_sprite = pygame.sprite.Group()

        for level in range(self.max_level + 1):
            star_amount = levels[level]['star_amount']

            for i in range(5):

                if i < star_amount:
                    is_available = True
                else:
                    is_available = False

                if i == 0:
                    node = self.nodes_sprite.sprites()[level]
                    pos = (node.rect.bottomleft[0] + 5, node.rect.bottomleft[1] - 10)
                else:
                    pos = (pos[0] + 40, pos[1])
                
                star = Star(pos, is_available)
                
                star_sprite.add(star)

        return star_sprite

    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if not self.is_moving and self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.movement_direction = self.get_movement_data(self.nodes_sprite.sprites(), 
                self.current_level,'next')
                
                self.current_level += 1
                self.is_moving = True

            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.movement_direction = super().get_movement_data(self.nodes_sprite.sprites(), 
                self.current_level,'prev')

                self.current_level -= 1
                self.is_moving = True

            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def run(self):
        super().input_timer()
        self.get_input()
        self.nodes_sprite.update()
        super().update_icon(self.nodes_sprite.sprites(), self.current_level)
        self.icon_sprite.update()
        self.star_sprite.update()
        
        self.sky.draw(self.display_surface)
        super().draw_paths(self.max_level, 'overworld')
        self.nodes_sprite.draw(self.display_surface)
        self.icon_sprite.draw(self.display_surface)
        self.star_sprite.draw(self.display_surface)

class PauseMenu(Menu):
    def __init__(self, surface, exit_pause_menu, create_overworld, current_level):
        super().__init__(surface)
        self.exit_pause_menu = exit_pause_menu
        self.current_option = 0
        self.max_options = 2

        # Overworld
        self.create_overworld = create_overworld
        self.current_level = current_level
        
        # Sprite
        self.node_sprite = self.setup_node()
        super().setup_icon(self.node_sprite.sprites(), self.current_option)

    def setup_node(self):
        node_sprite = pygame.sprite.Group()
        
        for node_data in menus.values():
            path = node_data['node_graphics']
            pos = node_data['node_pos']

            sprite = Node(pos, True, self.speed, path)
            node_sprite.add(sprite)

        return node_sprite

    def get_input(self):
        keys = pygame.key.get_pressed()

        if not self.is_moving and self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_option < self.max_options:
                self.movement_direction = self.get_movement_data(self.node_sprite.sprites(),
                self.current_option, 'next')
                self.current_option += 1
                self.is_moving = True

            elif keys[pygame.K_LEFT] and self.current_option > 0:
                self.movement_direction = self.get_movement_data(self.node_sprite.sprites(),
                self.current_option, 'prev')
                self.current_option -= 1
                self.is_moving = True

            if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                
                if self.current_option == 0:
                    self.exit_pause_menu()
                elif self.current_option == 1:
                    self.create_overworld(self.current_level, self.current_level)
                else:
                    pygame.quit()
                    sys.exit()

    def run(self):
        super().input_timer()
        self.get_input()
        super().update_icon(self.node_sprite.sprites(), self.current_option)
        self.icon_sprite.update()
        self.node_sprite.update()

        self.sky.draw(self.display_surface)
        super().draw_paths(self.max_options, 'pause_menu')
        self.node_sprite.draw(self.display_surface)
        self.icon_sprite.draw(self.display_surface)