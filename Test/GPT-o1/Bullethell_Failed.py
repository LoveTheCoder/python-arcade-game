import pygame
import random
import sys
import math
import os
import shutil

#test

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
SCREEN_HEIGHT = 480  # Changed from 600
FPS = 60
PLAYER_AREA_Y = SCREEN_HEIGHT * (2 / 3)  # Now ~320 pixels
TOP_THIRD_Y_LIMIT = SCREEN_HEIGHT / 3     # Now ~160 pixels
WATERMARK_TEXT = "*Continued Run*"

# Colors
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
BLACK  = (  0,   0,   0)
BLUE   = (  0,   0, 255)
YELLOW = (255, 255,   0)
ORANGE = (255, 165,    0)
PURPLE = (128,   0, 128)
LIGHT_BLUE = (0, 191, 255)

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

# Background Generation and Storage System
backgrounds = {}
backgrounds_dir = 'backgrounds'
if not os.path.exists(backgrounds_dir):
    os.makedirs(backgrounds_dir)

# In the background creation section
backgrounds = {}
for level in range(1, 12):  # Include level 11
    try:
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        if level == 10:
            # Pure white background for level 10
            background.fill(WHITE)
        elif level == 11:
            # Dark background for final phase
            background.fill((30, 30, 30))
        else:
            # Dynamic colors for levels 1-9
            if level % 3 == 0:
                # Blue-ish space
                background.fill((20, 20, 40 + level * 15))
            elif level % 3 == 1:
                # Purple-ish space
                background.fill((40 + level * 10, 0, 40 + level * 10))
            else:
                # Dark red-ish space
                background.fill((40 + level * 10, 20, 30))

            # Add stars with different sizes
            for _ in range(100):
                x = random.randint(0, SCREEN_WIDTH - 1)
                y = random.randint(0, SCREEN_HEIGHT - 1)
                size = random.randint(1, 3)
                brightness = random.randint(180, 255)
                pygame.draw.circle(background, (brightness, brightness, brightness), (x, y), size)

            # Add random planets (2-3 per level)
            for _ in range(random.randint(2, 3)):
                planet_x = random.randint(50, SCREEN_WIDTH - 50)
                planet_y = random.randint(50, SCREEN_HEIGHT - 50)
                planet_size = random.randint(20, 40)
                planet_color = (
                    random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(100, 255)
                )
                # Draw planet
                pygame.draw.circle(background, planet_color, (planet_x, planet_y), planet_size)
                # Add some darker shading to give depth
                pygame.draw.circle(background, 
                    (max(planet_color[0] - 50, 0),
                     max(planet_color[1] - 50, 0),
                     max(planet_color[2] - 50, 0)),
                    (planet_x - planet_size//4, planet_y - planet_size//4), 
                    planet_size//2)

        backgrounds[level] = background
        save_image(background, os.path.join(ASSETS_DIR, 'backgrounds', f'background_level_{level}.png'))
            
    except Exception as e:
        print(f"Error creating background for level {level}: {e}")
        # Fallback background if creation fails
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        if level == 10:
            background.fill(WHITE)
        elif level == 11:
            background.fill((30, 30, 30))
        else:
            background.fill((20 + level * 10, 20 + level * 5, 40 + level * 10))
        backgrounds[level] = background

# Setup Display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Hell Game")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 36)

# Load Backgrounds
backgrounds = {}
for level in range(1, 12):  # Changed range to include level 11
    try:
        backgrounds[level] = pygame.image.load(os.path.join(ASSETS_DIR, 'backgrounds', f'background_level_{level}.png')).convert()
        backgrounds[level] = pygame.transform.scale(backgrounds[level], (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        if level == 10:
            # White background for level 10
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            background.fill(WHITE)
            backgrounds[level] = background
        elif level == 11:
            # Dark gray background for final phase
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            background.fill((30, 30, 30))
            backgrounds[level] = background
        else:
            backgrounds[level] = BLACK  # Fallback to black if image not found
            
try:
    menu_background_image = pygame.image.load(os.path.join(ASSETS_DIR, 'backgrounds', 'menu_background.png')).convert()
    menu_background_image = pygame.transform.scale(menu_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception as e:
    print("Error loading menu background:", e)
    menu_background_image = None
    
def generate_cyberpunk_background(width, height):
    background = pygame.Surface((width, height))
    # Create a vertical gradient from dark blue to near-black
    for y in range(height):
        # Interpolate between two colors (dark blue and nearly black)
        r = 0
        g = 0
        b = max(0, 35 - int(35 * (y/height)))
        pygame.draw.line(background, (r, g, b), (0, y), (width, y))
    
    # Add a subtle color overlay for extra neon vibe
    overlay = pygame.Surface((width, height))
    overlay.fill((10, 0, 30))
    overlay.set_alpha(40)
    background.blit(overlay, (0, 0))
    
    # Draw a scattering of stars
    for _ in range(250):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        star_color = random.choice([(255,255,255), (210,210,255), (255,200,200)])
        pygame.draw.circle(background, star_color, (x, y), random.choice([1, 2]))
    
    
    return background

# Generate and store the background in a global variable
menu_background_image = generate_cyberpunk_background(SCREEN_WIDTH, SCREEN_HEIGHT)

def draw_menu_background(screen):
    # Blit the generated background image
    screen.blit(menu_background_image, (0, 0))

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
    'burst_homing': pygame.Surface((60, 60)),
    'spiral': pygame.Surface((60, 60)),
    'circle': pygame.Surface((60, 60)),
    'aimed': pygame.Surface((60, 60)),
    'random': pygame.Surface((60, 60)),
    'mass_acceleration': pygame.Surface((60, 60)),
    'final_phase': pygame.Surface((60, 60))  # Add final phase image
}

# Initialize all boss images
for pattern in boss_images:
    boss_images[pattern].fill(RED if pattern != 'final_phase' else BLACK)  # Final phase boss is black
    if level == 10 and pattern == 'mass_acceleration':
        boss_images[pattern].fill(BLACK)  # Level 10 boss is black
    pygame.draw.circle(boss_images[pattern], WHITE if pattern == 'final_phase' else RED, 
                      (30, 30), 30)  # Outer circle
    pygame.draw.circle(boss_images[pattern], BLACK if pattern == 'final_phase' else WHITE, 
                      (30, 30), 20)  # Inner circle

for key in boss_images:
    boss_images[key] = pygame.transform.scale(boss_images[key], (100, 80))

# Sprite Groups
all_sprites   = pygame.sprite.Group()
bullets       = pygame.sprite.Group()
bosses        = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemies       = pygame.sprite.Group()
power_points  = pygame.sprite.Group()
points        = pygame.sprite.Group()

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
    10: 'mass_acceleration',  # First face
    11: 'final_phase'        # Second face
}

# For displaying text (change color based on level)
def get_text_color(level):
    if level == 10:
        return BLACK
    return WHITE

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
        self.lives = 3
        self.score = 0  # Add score attribute

        # Power-up variables
        self.power_level = 1  # Ranges from 0 to 10
        self.pp_collected = 0
        self.pp_needed = 5  # Number of pp needed for next power-up

        self.continued_run = False  # Add this line

        if level == 10:
            pygame.draw.circle(player_image, BLACK, (15, 15), 15)  # Black circle
            pygame.draw.circle(player_image, BLACK, (15, 15), 3)   # Black hitbox

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

            angles = []
            positions = []

            if self.power_level == 1:
                # Power level 1: one bullet straight up
                angles.append(0)
                positions.append(self.rect.centerx)
            elif self.power_level == 2:
                # Power level 2: two bullets straight up, offset positions
                angles.extend([0, 0])
                offset = 5  # pixels to offset from center
                positions.extend([self.rect.centerx - offset, self.rect.centerx + offset])
            else:
                if self.power_level % 2 == 0:
                    # Even power levels: two bullets straight up
                    angles.extend([0, 0])
                    positions.extend([self.rect.centerx - 5, self.rect.centerx + 5])
                    bullets_remaining = self.power_level - 2
                else:
                    # Odd power levels: one bullet straight up
                    angles.append(0)
                    positions.append(self.rect.centerx)
                    bullets_remaining = self.power_level - 1

                # Distribute remaining bullets symmetrically around 0 degrees
                if bullets_remaining > 0:
                    num_pairs = bullets_remaining // 2
                    spread_angle = 45  # Total spread angle to one side

                    for i in range(1, num_pairs + 1):
                        offset_angle = (spread_angle / (num_pairs + 1)) * i
                        angles.append(-offset_angle)
                        positions.append(self.rect.centerx)
                        angles.append(offset_angle)
                        positions.append(self.rect.centerx)

            # Create bullets based on calculated angles and positions
            for i, angle in enumerate(angles):
                radians = math.radians(angle)
                speed = 12  # Bullet speed

                # Calculate velocity components
                speedx = speed * math.sin(radians)
                speedy = -speed * math.cos(radians)

                # Use the offset positions
                x = positions[i]

                bullet = Bullet(
                    x,
                    self.rect.top,
                    self.power_level,
                    speedx=speedx,
                    speedy=speedy
                )
                all_sprites.add(bullet)
                bullets.add(bullet)

    def power_up(self):
        if self.power_level < 10:
            self.power_level += 1
            self.pp_collected = 0
            # Increase pp_needed for next level
            self.pp_needed += 5  # Each level requires 5 more pp than the previous

# Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, power_level, speedx=0, speedy=-12):
        super(Bullet, self).__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
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
        if level == 10:
            self.image.fill(BLACK)  # Black bullets for level 10
        else:
            self.image.fill(YELLOW)  # Original color for other levels
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = speedx
        self.speedy = speedy
        self.accel_x = accel_x
        self.accel_y = accel_y
        self.damage = 25
        self.grazed = False  # New attribute to track if bullet has been grazed

    def update(self):
        self.speedx += self.accel_x
        self.speedy += self.accel_y
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Remove the bullet if it goes off-screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        if self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0:
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

# Point Class
class Point(pygame.sprite.Sprite):
    def __init__(self, x, y, value):
        super(Point, self).__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(LIGHT_BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = 2  # Falls slightly faster than power points
        self.value = value

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
            self.image = enemy_images[pattern].copy()  # Create a copy of the original image
        
        # Only make enemies black in level 10
        if level == 10:
            self.image.fill(BLACK)
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

        if level == 10:
            self.image.fill(BLACK)  # Make enemy black for level 10

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
        
        # Always drop points
        point = Point(self.rect.centerx, self.rect.centery, 1000)  # 1000 points per enemy
        all_sprites.add(point)
        points.add(point)
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

        self.is_second_phase = level == 11
        self.health = 2000 * (1.5 ** (level - 1))
        if self.is_second_phase:
            self.mass_accel_interval = 150  # Slower bullet spawn for second phase

        if level == 10:
            self.image.fill(BLACK)  # Make boss black for level 10

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
        if self.pattern in ['mass_acceleration', 'final_phase']:
            if now - self.last_mass_accel_shot > self.mass_accel_interval:
                self.last_mass_accel_shot = now
                num_bullets = 5 if self.is_second_phase else 3  # Spawn more bullets in second phase
                bullet_size = 15
                
                # Add side spawns for second phase
                spawn_points = [(random.randint(0, SCREEN_WIDTH), random.randint(0, int(TOP_THIRD_Y_LIMIT)))]
                if self.is_second_phase:
                    spawn_points.extend([
                        (0, random.randint(0, SCREEN_HEIGHT)),         # Left side spawn
                        (SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT))  # Right side spawn
                    ])

                for spawn_point in spawn_points:
                    for _ in range(num_bullets):
                        fx, fy = spawn_point
                        speedx = 0  # Initialize speedx
                        speedy = 0  # Initialize speedy
                        
                        if self.is_second_phase:
                            if fx == 0:  # Left side
                                speedx = 6  # Move right
                                speedy = 0
                            elif fx == SCREEN_WIDTH:  # Right side
                                speedx = -6  # Move left
                                speedy = 0
                            else:  # Top spawns
                                angle_variation = random.uniform(-0.2, 0.2)
                                speedx = math.sin(angle_variation) * 2
                                speedy = 4 + abs(math.cos(angle_variation)) * 2
                        else:
                            # Normal pattern for first phase
                            angle_variation = random.uniform(-0.2, 0.2)
                            speedx = math.sin(angle_variation) * 2
                            speedy = 4 + abs(math.cos(angle_variation)) * 2
                        
                        accel_y = 0 if self.is_second_phase and (fx == 0 or fx == SCREEN_WIDTH) else 0.05
                        
                        bullet = EnemyBullet(fx, fy, speedx, speedy, size=bullet_size, accel_x=0, accel_y=accel_y)
                        all_sprites.add(bullet)
                        enemy_bullets.add(bullet)

    def draw_health_bar(self, surface):
        # Modify health bar colors for level 10
        bar_color = BLACK if level == 10 else RED
        outline_color = BLACK if level == 10 else WHITE
        # Draw health bar above the boss
        bar_length = 100
        bar_height = 10
        fill = (self.health / self.max_health) * bar_length
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 15, fill, bar_height)
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 15, bar_length, bar_height)
        pygame.draw.rect(surface, bar_color, fill_rect)
        pygame.draw.rect(surface, outline_color, outline_rect, 1)

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
        
        # Drop lots of points for boss kill
        for _ in range(10):  # Drop multiple point items
            x = self.rect.centerx + random.randint(-50, 50)
            y = self.rect.centery + random.randint(-30, 30)
            point = Point(x, y, 10000)  # 10000 points per point item
            all_sprites.add(point)
            points.add(point)

# Functions to display messages
def display_game_over():
    # Draw static menu background with overlay
    draw_menu_background(screen)
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Draw central cyberpunk-style message
    title = font.render("GAME OVER", True, (255, 20, 147))
    score_text = font.render(f"Final Score: {player.score:,}", True, WHITE)
    instr_text = font.render("Press R to Restart, C to Continue, M for Menu", True, (0, 255, 255))
    
    title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))
    
    screen.blit(title, title_rect)
    screen.blit(score_text, score_rect)
    screen.blit(instr_text, instr_rect)
    pygame.display.flip()

def display_game_won():
    # Draw static menu background with a neon overlay
    draw_menu_background(screen)
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((10, 10, 40))
    screen.blit(overlay, (0, 0))
    
    title_text = font.render("CONGRATULATIONS!", True, (0, 255, 255))
    score_text = font.render(f"Final Score: {player.score:,}", True, WHITE)
    
    if player.continued_run:
        status_text = font.render("*Continued Run*", True, RED)
    else:
        status_text = font.render("Legitimate Clear!", True, GREEN)
        
    instr_text = font.render("Press R to Play Again, M for Menu", True, (255, 105, 180))
    
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20))
    status_rect = status_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
    instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80))
    
    screen.blit(title_text, title_rect)
    screen.blit(score_text, score_rect)
    screen.blit(status_text, status_rect)
    screen.blit(instr_text, instr_rect)
    pygame.display.flip()

def display_level_completion(level):
    # Draw static menu background with overlay
    draw_menu_background(screen)
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((20, 20, 40))
    screen.blit(overlay, (0, 0))
    
    level_text = font.render(f"Level {level} Complete!", True, (0, 255, 255))
    score_text = font.render(f"Current Score: {player.score:,}", True, WHITE)
    
    level_rect = level_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
    
    screen.blit(level_text, level_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()
    pygame.time.delay(2000)

# Function to Reset the Game
def reset_game(continue_game=False):
    global level, boss_spawned, boss_active, game_over, level_complete, game_won
    global wave_number, waves_per_level, wave_start_time, level_start_time

    if not continue_game:
        # Full reset
        level = 1
        boss_spawned = False
        boss_active = False
        wave_number = 0
        waves_per_level = 3 + (level // 2)
        wave_start_time = pygame.time.get_ticks()
        level_start_time = pygame.time.get_ticks()

        # Clear all sprites and recreate player
        all_sprites.empty()
        bullets.empty()
        enemy_bullets.empty()
        enemies.empty()
        bosses.empty()
        power_points.empty()
        points.empty()
        
        # Reset player
        player.lives = 3
        player.power_level = 1
        player.continued_run = False
        player.score = 0
        
        # Create new player image with original colors
        player.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(player.image, BLUE, (15, 15), 15)  # Blue circle
        pygame.draw.circle(player.image, RED, (15, 15), 3)    # Red hitbox
        
        player.rect.centerx = SCREEN_WIDTH / 2
        player.rect.bottom = SCREEN_HEIGHT - 50
        all_sprites.add(player)
    else:
        # Continue from current state
        player.lives = 3
        player.continued_run = True
    
    # Always reset score
    player.score = 0
    game_over = False
    level_complete = False
    game_won = False

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
    global boss_active, boss_spawned
    pattern = boss_patterns.get(level, 'mass_acceleration')
    if level == 11:  # Force final phase pattern for level 11
        pattern = 'final_phase'
    boss = Boss(level, pattern)
    all_sprites.add(boss)
    bosses.add(boss)
    boss_active = True
    boss_spawned = True

# Create Player
player = Player()
all_sprites.add(player)

# Add score display to the HUD
def draw_hud():
    text_color = get_text_color(level)
    lives_text = font.render(f'Lives: {player.lives}', True, text_color)
    level_text = font.render(f'Level: {level}', True, text_color)
    power_text = font.render(f'Power: {player.power_level}', True, text_color)
    score_text = font.render(f'Score: {player.score:,}', True, text_color)  # Add comma formatting
    
    screen.blit(lives_text, (10, 10))
    screen.blit(level_text, (10, 50))
    screen.blit(power_text, (10, 90))
    screen.blit(score_text, (10, 130))  # Add score display
    
    # Add watermark if continued run
    if player.continued_run:
        watermark = font.render(WATERMARK_TEXT, True, RED)
        screen.blit(watermark, (SCREEN_WIDTH - watermark.get_width() - 10, 10))
        
def start_menu(screen, font, clock):
    options = ["Start Game", "Return to Main Menu"]
    selected = 0
    # Use a larger neon font for the title
    title_font = pygame.font.SysFont("Arial", 72, bold=True)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected]
        # Draw static menu background
        draw_menu_background(screen)
        
        # Add a semi-transparent overlay for a cyberpunk effect
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((10, 10, 40))
        screen.blit(overlay, (0,0))
        
        # Draw neon title
        title_text = title_font.render("BULLET HELL", True, (0, 255, 255))
        glow = title_font.render("BULLET HELL", True, (255, 20, 147))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(glow, (title_rect.x - 2, title_rect.y - 2))
        screen.blit(title_text, title_rect)
        
        # Draw menu options
        for i, option in enumerate(options):
            color = (0, 255, 255) if i == selected else (200, 200, 200)
            option_text = font.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
            screen.blit(option_text, option_rect)
            
        # Draw instruction line with neon accent
        instr_text = font.render("Use UP/DOWN & ENTER", True, (255, 105, 180))
        instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(instr_text, instr_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

class BulletHellGame:
    def __init__(self):
        # Initialize game attributes
        self.running = True
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bullet Hell")
        self.clock = pygame.time.Clock()
        
        # Initialize game objects and variables
        self.init_game()

    def init_game(self):
        global player, all_sprites, bullets, enemy_bullets, enemies, bosses, power_points, points
        global level, boss_spawned, boss_active, game_over, level_complete, game_won
        global wave_number, wave_start_time, level_start_time
        
        # Initialize all game variables and create sprites here
        # (Copy existing initialization code)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def run(self):
        while True:
            menu_choice = start_menu(self.screen, font, self.clock)
            if menu_choice == "Return to Main Menu":
                return  # Return control back to main.py
            reset_game(False)  # Reset game state before a new session
            self.running = True
            self.game_loop()  # Run one game session
            
    def game_loop(self):
        global game_over, boss_spawned, boss_active, level_complete, level, game_won
        global wave_number, wave_start_time, level_start_time
        wave_start_time = pygame.time.get_ticks()
        level_start_time = pygame.time.get_ticks()
        while self.running:
            self.clock.tick(FPS)
            now = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if game_over:
                        if event.key == pygame.K_m:
                            self.running = False  # Exit to start menu
                        elif event.key == pygame.K_r:
                            reset_game(False)
                        elif event.key == pygame.K_c:
                            reset_game(True)
            if not game_over:
                # Enemy spawning logic
                waves_per_level = 3 + (level // 2)
                if not boss_spawned and not level_complete:
                    if wave_number < waves_per_level:
                        if now - wave_start_time > wave_duration:
                            wave_number += 1
                            spawn_enemy_wave()
                        elif len(enemies) == 0:
                            wave_number += 1
                            spawn_enemy_wave()
                    else:
                        if len(enemies) == 0:
                            spawn_boss()
                        elif now - level_start_time > level_duration:
                            for enemy in enemies:
                                enemy.kill()
                            spawn_boss()
                elif boss_spawned and boss_active:
                    max_enemies_during_boss = min(2 + level, 10)
                    enemy_spawn_chance = max(0.005, 0.02 - level * 0.001)
                    if len(enemies) < max_enemies_during_boss and random.random() < enemy_spawn_chance:
                        enemy_pattern = random.choice(['aimed', 'random', 'circle'])
                        enemy = Enemy(level, enemy_pattern)
                        all_sprites.add(enemy)
                        enemies.add(enemy)
                    if not bosses:
                        boss_active = False
                        level_complete = True

                # Update sprites and handle collisions/score as before
                all_sprites.update()
                
                waves_per_level = 3 + (level // 2)

                if not boss_spawned and not level_complete:
                    if wave_number < waves_per_level:
                        if now - wave_start_time > wave_duration:
                            wave_number += 1
                            spawn_enemy_wave()
                        elif len(enemies) == 0:
                            wave_number += 1
                            spawn_enemy_wave()
                    else:
                        if len(enemies) == 0:
                            spawn_boss()
                        elif now - level_start_time > level_duration:
                            for enemy in enemies:
                                enemy.kill()
                            spawn_boss()
                elif boss_spawned and boss_active:
                    max_enemies_during_boss = min(2 + level, 10)
                    enemy_spawn_chance = max(0.005, 0.02 - level * 0.001)
                    if len(enemies) < max_enemies_during_boss and random.random() < enemy_spawn_chance:
                        enemy_pattern = random.choice(['aimed', 'random', 'circle'])
                        enemy = Enemy(level, enemy_pattern)
                        all_sprites.add(enemy)
                        enemies.add(enemy)
                    if not bosses:
                        boss_active = False
                        level_complete = True

                enemy_hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
                for enemy, bullet_list in enemy_hits.items():
                    for bullet in bullet_list:
                        enemy.hp -= bullet.damage
                        if enemy.hp <= 0:
                            enemy.die()

                boss_hits = pygame.sprite.groupcollide(bosses, bullets, False, True)
                for boss, bullet_list in boss_hits.items():
                    for bullet in bullet_list:
                        boss.health -= bullet.damage
                        if boss.health <= 0:
                            boss.die()

                player_hitbox = player.rect.center

                hit = False
                for bullet in enemy_bullets:
                    if bullet.rect.collidepoint(player_hitbox):
                        bullet.kill()
                        hit = True
                if hit:
                    player.lives -= 1
                    if player.lives <= 0:
                        game_over = True

                collide = False
                for enemy in enemies:
                    if enemy.rect.collidepoint(player_hitbox):
                        enemy.kill()
                        collide = True
                if collide:
                    player.lives -= 1
                    if player.lives <= 0:
                        game_over = True

                pp_hits = pygame.sprite.spritecollide(player, power_points, True)
                for pp in pp_hits:
                    player.pp_collected += 1
                    if player.pp_collected >= player.pp_needed:
                        player.power_up()

                for bullet in enemy_bullets:
                    if not bullet.grazed:
                        if bullet.rect.colliderect(player.rect):
                            if not bullet.rect.collidepoint(player.rect.center):
                                bullet.grazed = True
                                point = Point(bullet.rect.centerx, bullet.rect.centery, 5000)
                                all_sprites.add(point)
                                points.add(point)

                points_collected = pygame.sprite.spritecollide(player, points, True)
                for point in points_collected:
                    player.score += point.value

                if level_complete:
                    if level == 10:
                        level = 11
                        level_complete = False
                        boss_spawned = False
                        boss_active = False
                        spawn_boss()
                    elif level >= max_levels:
                        game_won = True
                        game_over = True
                    else:
                        level += 1
                        level_complete = False
                        boss_spawned = False
                        boss_active = False
                        wave_number = 0
                        waves_per_level = 3 + (level // 2)
                        level_start_time = pygame.time.get_ticks()
                        display_level_completion(level - 1)

                # Drawing code
                if isinstance(backgrounds.get(level, BLACK), pygame.Surface):
                    self.screen.blit(backgrounds[level], (0, 0))
                else:
                    self.screen.fill(backgrounds[level])
                all_sprites.draw(self.screen)
                pygame.draw.circle(self.screen, RED, player.rect.center, 3)
                for boss in bosses:
                    boss.draw_health_bar(self.screen)
                draw_hud()
                pygame.display.flip()
            else:
                if game_won:
                    display_game_won()
                else:
                    display_game_over()
        # End of game_loop returns to run() to show the start menu again

# Main Game Loop
# ...existing code above remains unchanged...

# Main Game Loop
def main():
    global game_over, boss_spawned, boss_active, level_complete, level, game_won
    global wave_number, wave_start_time, level_start_time
    running = True
    wave_start_time = pygame.time.get_ticks()
    level_start_time = pygame.time.get_ticks()
    while running:
        clock.tick(FPS)
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_m:
                    running = False  # Break out to return to the start menu
                elif game_won:
                    if event.key == pygame.K_r:
                        reset_game(False)
                else:
                    if event.key == pygame.K_r:
                        reset_game(False)
                    elif event.key == pygame.K_c:
                        reset_game(True)
        if not game_over:
            all_sprites.update()

            waves_per_level = 3 + (level // 2)

            if not boss_spawned and not level_complete:
                if wave_number < waves_per_level:
                    if now - wave_start_time > wave_duration:
                        wave_number += 1
                        spawn_enemy_wave()
                    elif len(enemies) == 0:
                        wave_number += 1
                        spawn_enemy_wave()
                else:
                    if len(enemies) == 0:
                        spawn_boss()
                    elif now - level_start_time > level_duration:
                        for enemy in enemies:
                            enemy.kill()
                        spawn_boss()
            elif boss_spawned and boss_active:
                max_enemies_during_boss = min(2 + level, 10)
                enemy_spawn_chance = max(0.005, 0.02 - level * 0.001)
                if len(enemies) < max_enemies_during_boss and random.random() < enemy_spawn_chance:
                    enemy_pattern = random.choice(['aimed', 'random', 'circle'])
                    enemy = Enemy(level, enemy_pattern)
                    all_sprites.add(enemy)
                    enemies.add(enemy)
                if not bosses:
                    boss_active = False
                    level_complete = True

            enemy_hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
            for enemy, bullet_list in enemy_hits.items():
                for bullet in bullet_list:
                    enemy.hp -= bullet.damage
                    if enemy.hp <= 0:
                        enemy.die()

            boss_hits = pygame.sprite.groupcollide(bosses, bullets, False, True)
            for boss, bullet_list in boss_hits.items():
                for bullet in bullet_list:
                    boss.health -= bullet.damage
                    if boss.health <= 0:
                        boss.die()

            player_hitbox = player.rect.center

            hit = False
            for bullet in enemy_bullets:
                if bullet.rect.collidepoint(player_hitbox):
                    bullet.kill()
                    hit = True
            if hit:
                player.lives -= 1
                if player.lives <= 0:
                    game_over = True

            collide = False
            for enemy in enemies:
                if enemy.rect.collidepoint(player_hitbox):
                    enemy.kill()
                    collide = True
            if collide:
                player.lives -= 1
                if player.lives <= 0:
                    game_over = True

            pp_hits = pygame.sprite.spritecollide(player, power_points, True)
            for pp in pp_hits:
                player.pp_collected += 1
                if player.pp_collected >= player.pp_needed:
                    player.power_up()

            for bullet in enemy_bullets:
                if not bullet.grazed:
                    if bullet.rect.colliderect(player.rect):
                        if not bullet.rect.collidepoint(player.rect.center):
                            bullet.grazed = True
                            point = Point(bullet.rect.centerx, bullet.rect.centery, 5000)
                            all_sprites.add(point)
                            points.add(point)

            points_collected = pygame.sprite.spritecollide(player, points, True)
            for point in points_collected:
                player.score += point.value

            if level_complete:
                if level == 10:
                    level = 11
                    level_complete = False
                    boss_spawned = False
                    boss_active = False
                    spawn_boss()
                elif level >= max_levels:
                    game_won = True
                    game_over = True
                else:
                    level += 1
                    level_complete = False
                    boss_spawned = False
                    boss_active = False
                    wave_number = 0
                    waves_per_level = 3 + (level // 2)
                    level_start_time = pygame.time.get_ticks()
                    display_level_completion(level - 1)

            if isinstance(backgrounds.get(level, BLACK), pygame.Surface):
                screen.blit(backgrounds[level], (0, 0))
            else:
                screen.fill(backgrounds[level])
            all_sprites.draw(screen)
            pygame.draw.circle(screen, RED, player.rect.center, 3)
            for boss in bosses:
                boss.draw_health_bar(screen)
            draw_hud()
            pygame.display.flip()
        else:
            if game_won:
                display_game_won()
            else:
                display_game_over()
    return  # Removed sys.exit() to allow proper return to the start menu

if __name__ == "__main__":
    main()
    
    #test 2