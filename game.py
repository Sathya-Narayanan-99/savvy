import pygame
from levels import Level
from menu import Overworld
from ui import UI

class Game:
    def __init__(self, screen):

        self.display_surface = screen
        
        # Audio
        self.level_bg_music = pygame.mixer.Sound("resources/audio/level_music.wav")
        self.level_bg_music.set_volume(0.1)

        self.rum_sound = pygame.mixer.Sound("resources/audio/effects/rum.wav")
        self.rum_sound.set_volume(0.5)

        self.overworld_bg_music = pygame.mixer.Sound("resources/audio/overworld_music.wav")
        self.overworld_bg_music.set_volume(0.1)

        # Overworld Creation
        self.max_level = 0
        self.overworld = Overworld(0, self.max_level, self.display_surface, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(-1)

        # Game Attributes
        self.max_health = 100
        self.cur_health = 100
        self.coin_count = 0
        self.rum = 0

        # UI
        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, self.display_surface, 
        self.create_overworld, self.update_coin_count, self.update_health,
        self.update_rum)
        
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, 
        self.display_surface, self.create_level)
        
        self.status = 'overworld'
        self.level_bg_music.stop()
        self.overworld_bg_music.play(-1)

    def update_coin_count(self, amount):
        self.coin_count += amount

    def update_health(self, amount = 0, type = 'enemy_collision'):

        if type == 'enemy_collision':
            if amount > 0:
                if self.cur_health < self.max_health:
                    self.cur_health += amount
            else:
                self.cur_health += amount
        
        elif type == 'fall':
            
            if self.cur_health > 25:
                self.cur_health = 25
            elif 15 < self.cur_health <= 25:
                self.cur_health = 15
            else:
                self.cur_health = 0
    
    def update_rum(self, type):
        
        if type == 'collect':
            self.rum += 1
        
        elif type == 'use':
            if self.cur_health < 80 and self.rum > 0:
                self.cur_health = 80
                self.rum -= 1
                self.rum_sound.play()

    def check_game_over(self):
        if self.cur_health <=0:
            self.cur_health = 100
            self.coin_count = 0

            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, 
            self.display_surface, self.create_level)
            
            self.status = 'overworld'

            self.level_bg_music.stop()
            self.overworld_bg_music.play(-1)

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.display_health(self.cur_health, self.max_health)
            self.ui.display_coins(self.coin_count)
            self.ui.display_rum(self.rum)
            self.check_game_over()
