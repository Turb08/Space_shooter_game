import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Shooter")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player's ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")) , (WIDTH, HEIGHT))

def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 40)
    clock = pygame.time.Clock()

    def draw_window():
        WIN.blit(BG, (0, 0))

        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))

        WIN.blit(level_label, (10, 10))
        WIN.blit(lives_label, (WIDTH - lives_label.get_width() - 10, 10))
        WIN.blit(YELLOW_SPACE_SHIP, (350, 500))
        pygame.display.update()

    while run:
        clock.tick(FPS)
        draw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

main()