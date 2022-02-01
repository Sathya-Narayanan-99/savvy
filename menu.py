import pygame
import sys
from decorations import Sky
from overworld import Icon
from debug import debug

class Node(pygame.sprite.Sprite):
    def __init__(self, path, pos, icon_speed):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center = pos)

        self.icon_collide_point = pygame.Rect(self.rect.centerx - icon_speed //2, self.rect.centery - icon_speed //2, icon_speed, icon_speed)

class Menu:
    def __init__(self, surface, exit_pause_menu, create_overworld, current_level):
        self.display_surface = surface
        self.sky = Sky(8, 'overworld')
        self.exit_pause_menu = exit_pause_menu
        self.current_option = 0
        self.max_options = 2

        # Overworld
        self.create_overworld = create_overworld
        self.current_level = current_level

        # icon movement
        self.is_moving = False
        self.movement_direction = pygame.math.Vector2(0,0)
        self.speed = 8

        # Sprite
        self.node_sprite = self.setup_node()
        self.setup_icon()

        # timer
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.enable_input_time = 500

    def setup_node(self):
        node_sprite = pygame.sprite.Group()
        
        resume = Node('resources/graphics/menu/resume.png', (250, 300), self.speed)
        node_sprite.add(resume)

        overworld = Node('resources/graphics/menu/overworld.png', (600, 300), self.speed)
        node_sprite.add(overworld)

        quit = Node('resources/graphics/menu/quit.png', (950, 300), self.speed)
        node_sprite.add(quit)

        return node_sprite
    
    def setup_icon(self):
        self.icon_sprite = pygame.sprite.GroupSingle()
        pos = self.node_sprite.sprites()[self.current_option].rect.center
        icon = Icon(pos)
        self.icon_sprite.add(icon)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if not self.is_moving and self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_option < self.max_options:
                self.movement_direction = self.get_movement_data('next')
                self.current_option += 1
                self.is_moving = True

            elif keys[pygame.K_LEFT] and self.current_option > 0:
                self.movement_direction = self.get_movement_data('prev')
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

    def update_icon(self):
        if self.is_moving and self.movement_direction:
            self.icon_sprite.sprite.position += self.speed * self.movement_direction
            
            target_node = self.node_sprite.sprites()[self.current_option]
            if target_node.icon_collide_point.collidepoint(self.icon_sprite.sprite.position):
                self.is_moving = False
                self.movement_direction = pygame.math.Vector2(0,0)

    def get_movement_data(self, direction):
        pos = self.node_sprite.sprites()[self.current_option].rect.center
        start = pygame.math.Vector2(pos)
        
        if direction == 'next':
            pos = self.node_sprite.sprites()[self.current_option + 1].rect.center
        else:
            pos = self.node_sprite.sprites()[self.current_option - 1].rect.center
        end = pygame.math.Vector2(pos)

        return (end - start).normalize()
    
    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.enable_input_time:
                self.allow_input = True

    def run(self):
        self.input_timer()
        self.get_input()
        self.update_icon()
        self.icon_sprite.update()

        self.sky.draw(self.display_surface)
        self.node_sprite.draw(self.display_surface)
        self.icon_sprite.draw(self.display_surface)