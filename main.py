import pygame, sys
from settings import *
from levels import Level
from game_data import level_content
from overworld import Overworld

class Game:
    def __init__(self):
        self.max_level = 3
        self.overworld = Overworld(1, self.max_level, screen)

    def run(self):
        self.overworld.run()

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_content, screen)

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill("black")
    game.run()

    pygame.display.update()
    clock.tick(60)