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

        # Rum
        self.rum = pygame.image.load("resources/graphics/ui/rum.png").convert_alpha()
        self.rum_rect = self.rum.get_rect(topleft = (49,95))

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

    def display_rum(self, rum_amount):
        rum_amount_surf = self.font.render(str(rum_amount), False, '#33323d')
        rum_amount_rect = rum_amount_surf.get_rect(midleft = (self.rum_rect.right + 4, self.rum_rect.centery + 4))
        self.display_surface.blit(self.rum, self.rum_rect)
        self.display_surface.blit(rum_amount_surf, rum_amount_rect)