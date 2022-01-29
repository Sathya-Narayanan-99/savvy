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

        # Player Status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
    
    def import_character_asset(self):
        character_path = "resources/graphics/character/"
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index > len(animation): self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
        
        # Setting the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.directions.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.directions.x = -1
            self.facing_right = False
        else:
            self.directions.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
    
    def get_status(self):
        
        if self.directions.y < 0:
            self.status = 'jump'
        elif self.directions.y > 1:
            self.status = 'fall'
        else:
            if self.directions.x == 0:
                self.status = 'idle'
            else:
                self.status = 'run'

    def apply_gravity(self):
        self.directions.y += self.gravity
        self.rect.y += self.directions.y

    def jump(self):
        self.directions.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()