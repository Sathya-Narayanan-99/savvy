import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.import_character_asset()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = position)

        # Player Movement
        self.speed = 8
        self.directions = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.jump_speed = -16
    
    def import_character_asset(self):
        character_path = "resources/graphics/character/"
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations['idle']

        self.frame_index += self.animation_speed
        if self.frame_index > len(animation): self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.directions.x = 1
        elif keys[pygame.K_LEFT]:
            self.directions.x = -1
        else:
            self.directions.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def apply_gravity(self):
        self.directions.y += self.gravity
        self.rect.y += self.directions.y

    def jump(self):
        self.directions.y = self.jump_speed

    def update(self):
        self.get_input()
        self.animate()