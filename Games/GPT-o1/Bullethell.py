import pygame
import random
import sys
import math
import os
import shutil

# Get the directory of the current Python file
current_dir = os.path.dirname(os.path.realpath(__file__))

# Define assets directory path inside GPT-o1 folder
ASSETS_DIR = os.path.join(current_dir, 'assets')

# Create assets directory if it doesn't exist
os.makedirs(ASSETS_DIR, exist_ok=True)

# Define directories using ASSETS_DIR
sprites_dir = os.path.join(ASSETS_DIR, 'sprites')
backgrounds_dir = os.path.join(ASSETS_DIR, 'backgrounds')

# Create directories if they don't exist
os.makedirs(sprites_dir, exist_ok=True)
os.makedirs(backgrounds_dir, exist_ok=True)

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_AREA_Y = SCREEN_HEIGHT * (2 / 3)
TOP_THIRD_Y_LIMIT = SCREEN_HEIGHT / 3

# Colors
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
BLACK  = (  0,   0,   0)
BLUE   = (  0,   0, 255)
YELLOW = (255, 255,   0)
ORANGE = (255, 165,    0)
PURPLE = (128,   0, 128)

# Helper function to save images
def save_image(surface, path):
    pygame.image.save(surface, path)
    print(f"Saved {path}")

# Helper function to clean assets directory
def clean_assets():
    if os.path.exists(ASSETS_DIR):
        shutil.rmtree(ASSETS_DIR)
    os.makedirs(ASSETS_DIR, exist_ok=True)

# Create Player Image
player_path = os.path.join(sprites_dir, 'player.png')
player_image = pygame.Surface((30, 30), pygame.SRCALPHA)
player_image.fill((0, 0, 0, 0))  # Transparent background
pygame.draw.circle(player_image, BLUE, (15, 15), 15)  # Blue circle
pygame.draw.circle(player_image, RED, (15, 15), 3)    # Red dot at center (hitbox)
save_image(player_image, player_path)

# Enemy Patterns
enemy_patterns = ['aimed', 'random', 'circle']
for pattern in enemy_patterns:
    path = os.path.join(sprites_dir, f'enemy_{pattern}.png')
    enemy_image = pygame.Surface((30, 30), pygame.SRCALPHA)
    if pattern == 'aimed':
        pygame.draw.polygon(enemy_image, GREEN, [(15, 0), (30, 30), (0, 30)])
    elif pattern == 'random':
        pygame.draw.rect(enemy_image, (0, 255, 0), enemy_image.get_rect())
        pygame.draw.circle(enemy_image, BLACK, (15, 15), 5)
    elif pattern == 'circle':
        pygame.draw.circle(enemy_image, (0, 200, 0), (15, 15), 15)
        pygame.draw.circle(enemy_image, BLACK, (15, 15), 5)
    save_image(enemy_image, path)

# Boss Patterns
boss_patterns = ['burst_homing', 'spiral', 'circle', 'aimed', 'random', 'mass_acceleration']
for pattern in boss_patterns:
    path = os.path.join(sprites_dir, f'boss_{pattern}.png')
    boss_image = pygame.Surface((100, 80), pygame.SRCALPHA)
    if pattern == 'burst_homing':
        pygame.draw.polygon(boss_image, ORANGE, [(50, 0), (100, 80), (0, 80)])
    elif pattern == 'spiral':
        pygame.draw.arc(boss_image, (255, 100, 0), (10, 10, 80, 60), 0, 3.14, 5)
    elif pattern == 'circle':
        pygame.draw.circle(boss_image, (255, 165, 0), (50, 40), 40)
        pygame.draw.circle(boss_image, BLACK, (50, 40), 10)
    elif pattern == 'aimed':
        pygame.draw.polygon(boss_image, ORANGE, [(50, 10), (90, 70), (10, 70)])
    elif pattern == 'random':
        pygame.draw.rect(boss_image, (255, 140, 0), boss_image.get_rect())
        pygame.draw.circle(boss_image, BLACK, (50, 40), 15)
    elif pattern == 'mass_acceleration':
        pygame.draw.rect(boss_image, (255, 215, 0), boss_image.get_rect())
        pygame.draw.line(boss_image, BLACK, (0, 40), (100, 40), 5)
    save_image(boss_image, path)

# Backgrounds for Levels
for level in range(1, 11):
    path = os.path.join(backgrounds_dir, f'background_level_{level}.png')
    background = pygame.Surface((800, 600))
    # Create different background patterns based on level
    if level % 2 == 0:
        background.fill((min(20 * level, 255), min(30 * level, 255), min(40 * level, 255)))
    else:
        background.fill((min(40 * level, 255), min(20 * level, 255), min(30 * level, 255)))
    # Add stars or simple patterns
    for _ in range(50):
        x = random.randint(0, 799)
        y = random.randint(0, 599)
        pygame.draw.circle(background, WHITE, (x, y), 1)
    save_image(background, path)

# Setup Display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Hell Game")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 36)

# Load Backgrounds
backgrounds = {}
for level in range(1, 11):
    try:
        backgrounds[level] = pygame.image.load(os.path.join(ASSETS_DIR, 'backgrounds', f'background_level_{level}.png')).convert()
        backgrounds[level] = pygame.transform.scale(backgrounds[level], (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        backgrounds[level] = BLACK  # Fallback to black if image not found

# Load Player Image
try:
    player_image = pygame.image.load(os.path.join(ASSETS_DIR, 'sprites', 'player.png')).convert_alpha()
    player_image = pygame.transform.scale(player_image, (30, 30))
except:
    player_image = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(player_image, BLUE, (15, 15), 15)

# Load Enemy Images based on pattern
enemy_images = {
    'aimed': pygame.image.load(os.path.join(ASSETS_DIR, 'sprites', 'enemy_aimed.png')).convert_alpha(),
    'random': pygame.image.load(os.path.join(ASSETS_DIR, 'sprites', 'enemy_random.png')).convert_alpha(),
    'circle': pygame.image.load(os.path.join(ASSETS_DIR, 'sprites', 'enemy_circle.png')).convert_alpha()
}
for key in enemy_images:
    enemy_images[key] = pygame.transform.scale(enemy_images[key], (30, 30))

# Load Boss Images
boss_images = {
    'burst_homing': pygame.image.load(os.path.join(ASSETS_DIR, 'sprites', 'boss_burst_homing.png')).convert_alpha(),
    'spiral': pygame.image.load(os.path.join(ASSETS_DIR, 'sprites', 'boss_spiral.png')).convert_alpha(),
    'circle': pygame.image.load(os.path.join(ASSETS_DIR, 'sprites', 'boss_circle.png')).convert_alpha(),
    'aimed': pygame.image.load(os.path.join(ASSETS_DIR, 'sprites', 'boss_aimed.png')).convert_alpha(),
    'random': pygame.image.load(os.path.join(ASSETS_DIR, 'sprites', 'boss_random.png')).convert_alpha(),
    'mass_acceleration': pygame.image.load(os.path.join(ASSETS_DIR, 'sprites', 'boss_mass_acceleration.png')).convert_alpha()
}
for key in boss_images:
    boss_images[key] = pygame.transform.scale(boss_images[key], (100, 80))

# Sprite Groups
all_sprites   = pygame.sprite.Group()
bullets       = pygame.sprite.Group()
bosses        = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemies       = pygame.sprite.Group()
power_points  = pygame.sprite.Group()

# Game Variables
level = 1
max_levels = 10
boss_spawned = False
boss_active = False
game_over = False
level_complete = False
game_won = False
wave_number = 0
waves_per_level = 3 + (level // 2)  # Increase waves per level over time

wave_duration = 15000  # 15 seconds per wave
level_duration = 60000  # 60 seconds per level

wave_start_time = pygame.time.get_ticks()  # Initialize wave start time
level_start_time = pygame.time.get_ticks()

# Boss Patterns per Level
boss_patterns = {
    1: 'burst_homing',
    2: 'spiral',
    3: 'circle',
    4: 'spiral',
    5: 'aimed',
    6: 'random',
    7: 'circle',
    8: 'spiral',
    9: 'circle',
    10: 'mass_acceleration'  # New pattern for the last boss
}

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 50
        self.speedx = 0
        self.speedy = 0
        self.base_speed = 5  # Base movement speed
        self.lives = 9999

        # Power-up variables
        self.power_level = 0  # Ranges from 0 to 5
        self.pp_collected = 0
        self.pp_needed = 5  # Number of pp needed for next power-up

    def update(self):
        self.speedx = 0
        self.speedy = 0
        key_state = pygame.key.get_pressed()
        
        # Check if SHIFT key is held down to decrease speed
        if key_state[pygame.K_LSHIFT] or key_state[pygame.K_RSHIFT]:
            self.base_speed = 2  # Example reduced speed
        else:
            self.base_speed = 5  # Reset to base speed
        
        if key_state[pygame.K_LEFT]:
            self.speedx = -self.base_speed
        if key_state[pygame.K_RIGHT]:
            self.speedx = self.base_speed
        if key_state[pygame.K_UP]:
            self.speedy = -self.base_speed
        if key_state[pygame.K_DOWN]:
            self.speedy = self.base_speed
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Shooting
        if key_state[pygame.K_z]:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - getattr(self, 'last_shot', 0) > 250:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top, self.power_level)
            all_sprites.add(bullet)
            bullets.add(bullet)

    def power_up(self):
        if self.power_level < 5:
            self.power_level += 1

# Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, power_level, speedx=0, speedy=-12):
        super(Bullet, self).__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom  = y
        self.speedx = speedx
        self.speedy = speedy
        # Increase damage with power level
        self.damage = 50 + (power_level * 10)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
            self.rect.right < 0 or self.rect.left > SCREEN_WIDTH):
            self.kill()

# Enemy Bullet Class
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, size=7, accel_x=0, accel_y=0):
        super(EnemyBullet, self).__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = speedx
        self.speedy = speedy
        self.accel_x = accel_x
        self.accel_y = accel_y
        self.damage = 25

    def update(self):
        self.speedx += self.accel_x
        self.speedy += self.accel_y
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0 or
            self.rect.left > SCREEN_WIDTH or self.rect.right > SCREEN_WIDTH):
            self.kill()

# PowerPoint Class
class PowerPoint(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(PowerPoint, self).__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = 1  # Falls slowly downwards

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, level, pattern):
        super(Enemy, self).__init__()
        self.image = enemy_images.get(pattern, pygame.Surface((30, 30)))
        if isinstance(self.image, pygame.Surface):
            self.image = enemy_images[pattern]
        self.rect = self.image.get_rect()
        self.speed = 2 + level * 0.2
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = max(1000, 2000 - level * 100)
        self.hp = 100 + level * 50
        self.alive = True
        self.pattern = pattern

        # Spawn positions only in the top two-thirds of the screen
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-self.rect.height, int(PLAYER_AREA_Y / 2) - self.rect.height)

        # Movement variables
        self.speed_change_time = pygame.time.get_ticks()
        self.speed_change_interval = random.randint(1000, 3000)
        self.base_speed = self.speed
        self.speedx = random.choice([self.base_speed, -self.base_speed, 0])
        self.speedy = random.choice([self.base_speed, -self.base_speed, 0])

    def update(self):
        now = pygame.time.get_ticks()

        # Change speed at intervals
        if now - self.speed_change_time > self.speed_change_interval:
            self.speed_change_time = now
            self.speed_change_interval = random.randint(1000, 3000)
            # Randomly choose new speeds or stop
            self.speedx = random.choice([self.base_speed, -self.base_speed, 0])
            self.speedy = random.choice([self.base_speed, -self.base_speed, 0])

        # Move enemy
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Keep enemy within the upper two-thirds of the screen
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx *= -1
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.speedx *= -1
        if self.rect.top < 0:
            self.rect.top = 0
            self.speedy *= -1
        if self.rect.bottom > PLAYER_AREA_Y:
            self.rect.bottom = PLAYER_AREA_Y
            self.speedy *= -1

        # Enemy shooting logic
        if self.alive:
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                if self.pattern == 'aimed':
                    # Shoot directly at the player
                    dx = player.rect.centerx - self.rect.centerx
                    dy = player.rect.centery - self.rect.centery
                    distance = math.hypot(dx, dy)
                    if distance == 0:
                        distance = 1
                    speedx = (dx / distance) * 5
                    speedy = (dy / distance) * 5
                    bullet = EnemyBullet(self.rect.centerx, self.rect.centery, speedx, speedy)
                    all_sprites.add(bullet)
                    enemy_bullets.add(bullet)
                elif self.pattern == 'random':
                    # Shoot in a random direction
                    angle = random.uniform(0, 2 * math.pi)
                    speedx = math.cos(angle) * 4
                    speedy = math.sin(angle) * 4
                    bullet = EnemyBullet(self.rect.centerx, self.rect.centery, speedx, speedy)
                    all_sprites.add(bullet)
                    enemy_bullets.add(bullet)
                elif self.pattern == 'circle':
                    # Shoot bullets in all directions
                    num_bullets = 8
                    for i in range(num_bullets):
                        angle = (2 * math.pi / num_bullets) * i
                        speedx = math.cos(angle) * 3
                        speedy = math.sin(angle) * 3
                        bullet = EnemyBullet(self.rect.centerx, self.rect.centery, speedx, speedy)
                        all_sprites.add(bullet)
                        enemy_bullets.add(bullet)

    def die(self):
        # Drop power-point upon death
        if random.random() < 0.5:  # 50% chance to drop pp
            pp = PowerPoint(self.rect.centerx, self.rect.centery)
            all_sprites.add(pp)
            power_points.add(pp)
        self.kill()

# Boss Class
class Boss(pygame.sprite.Sprite):
    def __init__(self, level, pattern):
        super(Boss, self).__init__()
        self.level = level
        self.pattern = pattern
        self.image = boss_images.get(pattern, pygame.Surface((100, 80)))
        if isinstance(self.image, pygame.Surface):
            self.image = boss_images[pattern]
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.top = 50  # Positioned within top third

        # Increased health scaling based on level
        self.health = 2000 * (1.5 ** (level - 1))
        self.max_health = self.health

        # Movement attributes
        self.speedx = 2
        self.speedy = 1

        # Shooting attributes
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 2000  # Constant interval of 2 seconds
        self.mass_accel_interval = 100  # Spawn every 100 ms
        self.last_mass_accel_shot = pygame.time.get_ticks()

    def update(self):
        # Movement logic
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Bounce off the edges within top third
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speedx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= TOP_THIRD_Y_LIMIT:
            self.speedy *= -1

        # Shooting logic
        self.shoot()

        # Special attack logic
        self.special_attack()

    def shoot(self):
        now = pygame.time.get_ticks()
        if self.pattern != 'mass_acceleration':
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                # Generate spread out firing points within the top two-thirds area
                num_firing_points = 5  # More spread out
                firing_points = []
                margin = 50
                for _ in range(num_firing_points):
                    fx = random.randint(margin, SCREEN_WIDTH - margin)
                    fy = random.randint(0, int(TOP_THIRD_Y_LIMIT / 2))
                    firing_points.append((fx, fy))

                bullet_size = 15  # Larger bullets for bosses

                if self.pattern == 'burst_homing':
                    # Homing bullets shot simultaneously from spread points
                    for point in firing_points:
                        dx = player.rect.centerx - point[0]
                        dy = player.rect.centery - point[1]
                        distance = math.hypot(dx, dy)
                        if distance == 0:
                            distance = 1
                        speedx = (dx / distance) * 5
                        speedy = (dy / distance) * 5
                        bullet = EnemyBullet(point[0], point[1], speedx, speedy, size=bullet_size)
                        all_sprites.add(bullet)
                        enemy_bullets.add(bullet)
                elif self.pattern == 'spiral':
                    # Spiral bullet pattern from spread points
                    num_bullets = 12
                    for point in firing_points:
                        for i in range(num_bullets):
                            angle = (2 * math.pi / num_bullets) * i + (now % 360) * (math.pi / 180)
                            speedx = math.cos(angle) * 3
                            speedy = math.sin(angle) * 3
                            bullet = EnemyBullet(point[0], point[1], speedx, speedy, size=bullet_size)
                            all_sprites.add(bullet)
                            enemy_bullets.add(bullet)
                elif self.pattern == 'circle':
                    # Circular bullet pattern from spread points
                    num_bullets = 16
                    for point in firing_points:
                        for i in range(num_bullets):
                            angle = (2 * math.pi / num_bullets) * i
                            speedx = math.cos(angle) * 2
                            speedy = math.sin(angle) * 2
                            bullet = EnemyBullet(point[0], point[1], speedx, speedy, size=bullet_size)
                            all_sprites.add(bullet)
                            enemy_bullets.add(bullet)
                elif self.pattern == 'aimed':
                    # Boss aims directly at the player from spread points
                    for point in firing_points:
                        dx = player.rect.centerx - point[0]
                        dy = player.rect.centery - point[1]
                        distance = math.hypot(dx, dy)
                        if distance == 0:
                            distance = 1
                        speedx = (dx / distance) * 5
                        speedy = (dy / distance) * 5
                        bullet = EnemyBullet(point[0], point[1], speedx, speedy, size=bullet_size)
                        all_sprites.add(bullet)
                        enemy_bullets.add(bullet)
                elif self.pattern == 'random':
                    # Boss shoots bullets in random directions from spread points
                    num_random_bullets = 5
                    for point in firing_points:
                        for _ in range(num_random_bullets):
                            angle = random.uniform(0, 2 * math.pi)
                            speedx = math.cos(angle) * 4
                            speedy = math.sin(angle) * 4
                            bullet = EnemyBullet(point[0], point[1], speedx, speedy, size=bullet_size)
                            all_sprites.add(bullet)
                            enemy_bullets.add(bullet)

    def special_attack(self):
        now = pygame.time.get_ticks()
        if self.pattern == 'mass_acceleration':
            if now - self.last_mass_accel_shot > self.mass_accel_interval:
                self.last_mass_accel_shot = now
                # Spawn bullets from random positions in the top third
                num_bullets = 3  # Number of bullets to spawn each interval
                bullet_size = 15
                for _ in range(num_bullets):
                    fx = random.randint(0, SCREEN_WIDTH)
                    fy = random.randint(0, int(TOP_THIRD_Y_LIMIT))
                    angle_variation = random.uniform(-0.2, 0.2)  # Radians
                    speedx = math.sin(angle_variation) * 2
                    speedy = 4 + abs(math.cos(angle_variation)) * 2  # Initial speed with slight downward angle
                    accel_y = 0.05  # Downward acceleration
                    bullet = EnemyBullet(fx, fy, speedx, speedy, size=bullet_size, accel_x=0, accel_y=accel_y)
                    all_sprites.add(bullet)
                    enemy_bullets.add(bullet)

    def draw_health_bar(self, surface):
        # Draw health bar above the boss
        bar_length = 100
        bar_height = 10
        fill = (self.health / self.max_health) * bar_length
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 15, fill, bar_height)
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 15, bar_length, bar_height)
        pygame.draw.rect(surface, RED, fill_rect)
        pygame.draw.rect(surface, WHITE, outline_rect, 1)

    def die(self):
        self.kill()
        # Clear all bullets and power-points upon boss death
        for bullet in bullets:
            bullet.kill()
        for bullet in enemy_bullets:
            bullet.kill()
        for pp in power_points:
            pp.kill()
        # Despawn all remaining enemies
        for enemy in enemies:
            enemy.kill()

# Functions to display messages
def display_game_over():
    screen.fill(BLACK)
    text = font.render("Game Over! Press R to Restart", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def display_game_won():
    screen.fill(BLACK)
    text = font.render("You Won! Congratulations!", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def display_level_completion(level):
    screen.fill(BLACK)
    text = font.render(f"Level {level} Complete!", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)

# Function to Reset the Game
def reset_game():
    global level, boss_spawned, boss_active, game_over, level_complete, game_won
    global wave_number, waves_per_level, wave_start_time, level_start_time

    level = 1
    boss_spawned = False
    boss_active = False
    game_over = False
    level_complete = False
    game_won = False
    wave_number = 0
    waves_per_level = 3 + (level // 2)
    wave_start_time = pygame.time.get_ticks()
    level_start_time = pygame.time.get_ticks()

    all_sprites.empty()
    bullets.empty()
    enemy_bullets.empty()
    enemies.empty()
    bosses.empty()
    power_points.empty()
    player.lives = 3
    player.power_level = 0
    player.pp_collected = 0
    player.rect.centerx = SCREEN_WIDTH / 2
    player.rect.bottom = SCREEN_HEIGHT - 50
    all_sprites.add(player)

# Function to Spawn Enemy Wave
def spawn_enemy_wave():
    global wave_start_time
    enemy_pattern = random.choice(['aimed', 'random', 'circle'])
    num_enemies = 2 + (level - 1) * 2
    for _ in range(num_enemies):
        enemy = Enemy(level, enemy_pattern)
        all_sprites.add(enemy)
        enemies.add(enemy)
    wave_start_time = pygame.time.get_ticks()

# Function to Spawn Boss
def spawn_boss():
    global boss_spawned, boss_active
    pattern = boss_patterns.get(level, 'aimed')
    boss = Boss(level, pattern)
    all_sprites.add(boss)
    bosses.add(boss)
    boss_spawned = True
    boss_active = True

# Create Player
player = Player()
all_sprites.add(player)

# Main Game Loop
running = True
wave_start_time = pygame.time.get_ticks()
level_start_time = pygame.time.get_ticks()

while running:
    clock.tick(FPS)
    now = pygame.time.get_ticks()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                reset_game()

    if not game_over:
        # Update all sprites
        all_sprites.update()

        # Enemy wave and boss spawning logic
        waves_per_level = 3 + (level // 2)  # Increase waves per level over time

        if not boss_spawned and not level_complete:
            if wave_number < waves_per_level:
                # Check if wave duration has passed
                if now - wave_start_time > wave_duration:
                    wave_number += 1
                    spawn_enemy_wave()
                elif len(enemies) == 0:
                    # All enemies in current wave defeated, spawn next wave
                    wave_number += 1
                    spawn_enemy_wave()
            else:
                # All waves completed
                if len(enemies) == 0:
                    # Spawn boss
                    spawn_boss()
                elif now - level_start_time > level_duration:
                    # Level timeout reached, despawn enemies and spawn boss
                    for enemy in enemies:
                        enemy.kill()
                    spawn_boss()
        elif boss_spawned and boss_active:
            # During boss fight, spawn additional enemies with cap
            max_enemies_during_boss = min(2 + level, 10)  # Increase cap faster
            enemy_spawn_chance = max(0.005, 0.02 - level * 0.001)
            if len(enemies) < max_enemies_during_boss and random.random() < enemy_spawn_chance:
                enemy_pattern = random.choice(['aimed', 'random', 'circle'])
                enemy = Enemy(level, enemy_pattern)
                all_sprites.add(enemy)
                enemies.add(enemy)

            # When boss is defeated, remove remaining enemies
            if not bosses:
                boss_active = False
                level_complete = True  # Level completed when boss is defeated

        # Collision detection
        # Player bullets hit enemies
        enemy_hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for enemy, bullet_list in enemy_hits.items():
            for bullet in bullet_list:
                enemy.hp -= bullet.damage
                if enemy.hp <= 0:
                    enemy.die()

        # Player bullets hit bosses
        boss_hits = pygame.sprite.groupcollide(bosses, bullets, False, True)
        for boss, bullet_list in boss_hits.items():
            for bullet in bullet_list:
                boss.health -= bullet.damage
                if boss.health <= 0:
                    boss.die()

        # Modify collision detection to use only the player's hitbox (red dot)
        player_hitbox = player.rect.center

        # Enemy bullets hit player
        hit = False
        for bullet in enemy_bullets:
            if bullet.rect.collidepoint(player_hitbox):
                bullet.kill()
                hit = True
        if hit:
            player.lives -= 1
            if player.lives <= 0:
                game_over = True

        # Enemies collide with player
        collide = False
        for enemy in enemies:
            if enemy.rect.collidepoint(player_hitbox):
                enemy.kill()
                collide = True
        if collide:
            player.lives -= 1
            if player.lives <= 0:
                game_over = True

        # Power-ups collected by player
        pp_hits = pygame.sprite.spritecollide(player, power_points, True, pygame.sprite.collide_rect)
        for pp in pp_hits:
            player.pp_collected += 1
            if player.pp_collected >= player.pp_needed:
                player.power_up()

        # Level completion logic
        if level_complete:
            # Bullets and enemies are already cleared in boss die() method
            # Clear any remaining power-ups
            for pp in power_points:
                pp.kill()
            display_level_completion(level)
            level += 1
            if level > max_levels:
                game_over = True
                game_won = True
            else:
                level_complete = False
                boss_spawned = False
                boss_active = False
                wave_number = 0
                wave_start_time = now
                level_start_time = now

        # Drawing
        if isinstance(backgrounds.get(level, BLACK), pygame.Surface):
            screen.blit(backgrounds[level], (0, 0))
        else:
            screen.fill(backgrounds[level])

        all_sprites.draw(screen)

        # Draw Player Hitbox
        pygame.draw.circle(screen, RED, player.rect.center, 3)

        # Remove the line at the two-thirds mark

        # Draw Health Bars
        for boss in bosses:
            boss.draw_health_bar(screen)

        # Display Lives, Level, and Power Level
        lives_text = font.render(f'Lives: {player.lives}', True, WHITE)
        level_text = font.render(f'Level: {level}', True, WHITE)
        power_text = font.render(f'Power: {player.power_level}', True, WHITE)
        screen.blit(lives_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(power_text, (10, 90))

        pygame.display.flip()

    else:
        # Display Game Over or Game Won Message
        if game_won:
            display_game_won()
        else:
            display_game_over()

# Clean up assets before exiting
clean_assets()

pygame.quit()
sys.exit()