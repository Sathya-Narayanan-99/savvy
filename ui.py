import pygame

class UI:
    def __init__(self, surface):
        self.display_surface = surface

        # Health
        self.health_bar = pygame.image.load('resources/graphics/ui/health_bar.png').convert_alpha()
        self.health_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        # Coins
        self.coin = pygame.image.load("resources/graphics/ui/coin.png").convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (50,61))
        self.font = pygame.font.Font('resources/graphics/ui/ARCADEPI.TTF', 30)

    def display_health(self, cur_health, max_health):
        cur_health_ratio = cur_health / max_health
        cur_width = self.bar_max_width * cur_health_ratio
        health_bar_amount = pygame.Rect(self.health_bar_topleft, (cur_width, self.bar_height))

        self.display_surface.blit(self.health_bar, (20, 10))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_amount)

    def display_coins(self, coin_amount):
        coin_amount_surf = self.font.render(str(coin_amount), False, '#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(self.coin, self.coin_rect)
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)