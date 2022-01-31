import pygame, sys
from settings import *
from levels import Level
from overworld import Overworld
from ui import UI

class Game:
    def __init__(self):
        
        # Overworld Creation
        self.max_level = 0
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'

        # Game Attributes
        self.max_health = 100
        self.cur_health = 100
        self.coin_count = 0

        # UI
        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.update_coin_count, self.update_health)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def update_coin_count(self, amount):
        self.coin_count += amount

    def update_health(self, amount):
        self.cur_health -= amount

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.display_health(self.cur_health, self.max_health)
            self.ui.display_coins(self.coin_count)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
#level = Level(level_content, screen)

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill("grey")
    game.run()

    pygame.display.update()
    clock.tick(60)