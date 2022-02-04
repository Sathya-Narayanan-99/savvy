import pygame
from support import import_folder
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, position, surface, create_jump_particles, update_health):
        super().__init__()
        self.import_character_asset()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = position)
        self.display_surface = surface

        # Health management
        self.update_health = update_health
        self.is_invincible = False
        self.invincibility_duration = 2000
        self.hurt_time = 0

        # Dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.create_jump_particles = create_jump_particles

        # Player Movement
        self.speed = 8
        self.directions = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(self.rect.topleft, (40, self.rect.height))

        # Player Status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # Audio
        self.jump_sound = pygame.mixer.Sound("resources/audio/effects/jump.wav")
        self.jump_sound.set_volume(0.1)

        self.hit_sound = pygame.mixer.Sound("resources/audio/effects/hit.wav")
        self.hit_sound.set_volume(0.1)
    
    def import_character_asset(self):
        character_path = "resources/graphics/character/"
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder("resources/graphics/character/dust_particles/run")

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index > len(animation): self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft

        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.is_invincible:
            self.image.set_alpha(self.get_alpha_value())
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        

    def animate_dust_run(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            
            dust_particle = self.dust_run_particles[0]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle, pos)
            else:
                flipped_dust_particles = pygame.transform.flip(dust_particle, True, False)
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                self.display_surface.blit(flipped_dust_particles, pos)

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
            self.create_jump_particles(self.rect.midbottom)

            if not pygame.mixer.get_busy():
                self.jump_sound.play()
    
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
        self.collision_rect.y += self.directions.y

    def apply_damage(self):
        if not self.is_invincible:
            self.update_health(-10)
            self.hit_sound.play()
            self.is_invincible = True
            self.hurt_time = pygame.time.get_ticks()
    
    def invincibility_timer(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.hurt_time >= self.invincibility_duration:
            self.is_invincible = False
    
    def get_alpha_value(self):
        wave = sin(pygame.time.get_ticks())
        if wave >= 0: return 255
        else: return 0

    def jump(self):
        self.directions.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.animate_dust_run()
        self.invincibility_timer()