import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Shooter")

# Enemy ship images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player's ship image
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Enemy and player laser images
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background image
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")) , (WIDTH, HEIGHT))

# Laser class to represent the lasers shot by ships
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, velocity):
        self.y += velocity
    
    # Method to find out if the laser is off the screen
    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)
    
    # Method to check for collision with another object
    def collision(self, obj):
        return collide(self, obj)

# Ship abstract class
class Ship:
    COOLDOWN = 20  # Cooldown time for shooting lasers

    # Constructor for the Ship class
    # Initializing the ship's position, health, and image
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    # Method to draw the ship on the window
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, velocity, obj):
        # Move each laser and check for collisions with the given object
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    # Method to handle the cooldown of the ship's laser
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # Method to shoot a laser from the ship
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # Method to get the ship's width and height 
    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()

# Player class inheriting from Ship
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER

        #mask for pixel perfect collision detection
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, velocity, objs):
        # Move each laser and check for collisions with the given objects
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    # Method to draw the player ship and healthbar on the window
    def draw(self, window):
        super().draw(window)
        # Draw the health bar below the ship
        self.healthbar(window)

    # Method to draw the player health bar
    def healthbar(self, window):
        # Draw the health bar on the window
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))

class Enemy(Ship):
    # A dictionary to map colors to their respective ship and laser images
    COLOR_MAPS = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        # Initializing the enemy ship and laser images based on the color
        self.ship_img, self.laser_img = self.COLOR_MAPS[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        # Move the enemy ship downwards by the given velocity
        self.y += velocity

     # Method to shoot a laser from the enemy ship
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-25, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    # Check if the two objects collide using their masks
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 40)
    lost_font = pygame.font.SysFont("comicsans", 60)


    enemies = []
    wave_length = 5
    enemy_velocity = 1
    laser_velocity = 4


    # Player movement speed per frame rate
    player_velocity = 5

    # Initializing the player at the given position
    player = Player(WIDTH//2 - 50, HEIGHT - 120)

    # Clock to control the frame rate
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    # Function to draw the game window
    def draw_window():
        WIN.blit(BG, (0, 0))
        # Displaying the level and lives on the window
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - lives_label.get_width() - 10, 10))

        # Drawing each enemy ship on the window
        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        # If the player has lost, display the game over screen
        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))

        pygame.display.update()

    while run:
        # Frame rate limits
        clock.tick(FPS)

        draw_window()

        # Check if the player'a lives or health is less than or equal to 0
        if lives <= 0 or player.health <= 0:
            lost = True
            # Increment the lost count to track how long the player has been in the lost state
            lost_count += 1
        
        if lost:
            # If the lost count exceeds 3 seconds (60fps: 1second x 3), quit the game
            if lost_count > FPS * 3: 
                run = False
            else:
                continue # Skip the rest of the loop if lost

        if len(enemies) == 0:
            # Everytime the enemies list empties, a level incrases
            level += 1
            # Everytime a level incrases, the wave length increases
            wave_length += 5

            for i in range(wave_length):
                # Randomly generating enemy ships at the top of the screen
                enemy_x = random.randrange(50, WIDTH - 100)
                enemy_y = random.randrange(-1500, -100)
                enemy_color = random.choice(["red", "green", "blue"])
                enemy = Enemy(enemy_x, enemy_y, enemy_color)
                enemies.append(enemy)

        # Quit game if the exit button is clicked 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_velocity > 0: 
            player.x -= player_velocity
        # Check boundaries for player movement
        if keys[pygame.K_RIGHT] and player.x + player_velocity + player.get_width() < WIDTH:
            player.x += player_velocity
        if keys[pygame.K_UP] and player.y - player_velocity > 0:
            player.y -= player_velocity
        # Check boundaries for player movement
        if keys[pygame.K_DOWN] and player.y + player_velocity + player.get_height() + 20 < HEIGHT:
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player)

            if random.randrange(0, 2 * FPS) == 1:
                enemy.shoot()

            # remove enemy ship and reduce player health if they collide
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            # # Check for collision with the player ship
            # if player.mask.overlap(enemy.mask, (enemy.x - player.x, enemy.y - player.y)):
            #     enemies.remove(enemy)
            #     if player.health <= 0:
            #         lives -= 1
            #         player.health = player.max_health
            #         if lives <= 0:
            #             lost = True
            # If the enemy ship goes out of bounds, remove it from the list
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        player.move_lasers(-laser_velocity, enemies)

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 40)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press Mouse Button to Begin :)", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Check if the mouse button is clicked to start the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    quit()

main_menu()