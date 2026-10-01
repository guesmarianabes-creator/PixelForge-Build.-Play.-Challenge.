import pygame
from ui.hud import font, TEXT, MUTED, button

class BaseGame:
    def draw_title(self, screen, title, subtitle=""):
        title_img = font(32, True).render(title, True, TEXT)
        screen.blit(title_img, (50, 30))
        if subtitle:
            sub = font(15).render(subtitle, True, MUTED)
            screen.blit(sub, (53, 72))

    def draw_back(self, screen):
        rect = pygame.Rect(50, 620, 180, 48)
        button(screen, rect, "← MENU")
        return rect
