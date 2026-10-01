import pygame
from core.game_manager import GameManager

WIDTH, HEIGHT = 1100, 700

def main():
    pygame.init()
    pygame.display.set_caption("PixelForge — Build. Play. Challenge.")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    manager = GameManager(screen, clock)
    manager.run()

    pygame.quit()

if __name__ == "__main__":
    main()
