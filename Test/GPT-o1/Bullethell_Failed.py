import pygame
import random
import sys
import math
import os
import shutil

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# ====== Define Directories ======
# Get the directory where the current script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the assets directory to be under 'assets' within the script's directory
assets_dir = os.path.join(script_dir, 'assets')

# Define sprites, backgrounds, and sounds directories
sprites_dir = os.path.join(assets_dir, 'sprites')
backgrounds_dir = os.path.join(assets_dir, 'backgrounds')
sounds_dir = os.path.join(assets_dir, 'sounds')
effects_dir = os.path.join(sounds_dir, 'effects')
music_dir = os.path.join(sounds_dir, 'music')

# Ensure the assets directories exist
os.makedirs(sprites_dir, exist_ok=True)
os.makedirs(backgrounds_dir, exist_ok=True)
os.makedirs(effects_dir, exist_ok=True)
os.makedirs(music_dir, exist_ok=True)

# ====== Constants ======
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_AREA_Y = SCREEN_HEIGHT * (2 / 3)
TOP_THIRD_Y_LIMIT = SCREEN_HEIGHT / 3

# ====== Colors ======
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
BLACK  = (  0,   0,   0)
BLUE   = (  0,   0, 255)
YELLOW = (255, 255,   0)
ORANGE = (255, 165,    0)
PURPLE = (128,   0, 128)

# ====== Helper Functions ======
def save_image(surface, path):
    pygame.image.save(surface, path)
    print(f"Saved {path}")

# ====== Load Sounds ======
# Define sound file paths
shoot_sound_path = os.path.join(effects_dir, 'shoot.wav')
player_hit_sound_path = os.path.join(effects_dir, 'player_hit.wav')
enemy_hit_sound_path = os.path.join(effects_dir, 'enemy_hit.wav')
bgm_path = os.path.join(music_dir, 'background_music.mp3')

# Load sound effects
try:
    shoot_sound = pygame.mixer.Sound(shoot_sound_path)
    shoot_sound.set_volume(0.5)
except FileNotFoundError:
    shoot_sound = None
    print(f"Warning: Shoot sound '{shoot_sound_path}' not found.")

try:
    player_hit_sound = pygame.mixer.Sound(player_hit_sound_path)
    player_hit_sound.set_volume(0.5)
except FileNotFoundError:
    player_hit_sound = None
    print(f"Warning: Player hit sound '{player_hit_sound_path}' not found.")

try:
    enemy_hit_sound = pygame.mixer.Sound(enemy_hit_sound_path)
    enemy_hit_sound.set_volume(0.5)
except FileNotFoundError:
    enemy_hit_sound = None
    print(f"Warning: Enemy hit sound '{enemy_hit_sound_path}' not found.")

# Load and play background music
if os.path.exists(bgm_path):
    pygame.mixer.music.load(bgm_path)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)  # -1 for infinite loop
else:
    print(f"Warning: Background music '{bgm_path}' not found.")

# ====== Setup Display ======
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Hell Game")
clock = pygame.time.Clock()

# ====== Font ======
font = pygame.font.SysFont(None, 36)

# ====== Asset Creation ======
# Create Player Image
player_path = os.path.join(sprites_dir, 'player.png')
try:
    player_image = pygame.image.load(player_path).convert_alpha()
    player_image = pygame.transform.scale(player_image, (30, 30))
except FileNotFoundError:
    player_image = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(player_image, BLUE, (15, 15), 15)  # Player body
    pygame.draw.circle(player_image, RED, (15, 15), 3)    # Hitbox
    save_image(player_image, player_path)

# Create Enemy Images with Fallback
enemy_patterns = ['aimed', 'random', 'circle']
enemy_images = {}
for pattern in enemy_patterns:
    path = os.path.join(sprites_dir, f'enemy_{pattern}.png')
    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
    else:
        # Create a placeholder image
        image = pygame.Surface((30, 30), pygame.SRCALPHA)
        if pattern == 'aimed':
            pygame.draw.polygon(image, GREEN, [(15, 0), (30, 30), (0, 30)])
        elif pattern == 'random':
            pygame.draw.rect(image, GREEN, image.get_rect())
            pygame.draw.circle(image, BLACK, (15, 15), 5)
        elif pattern == 'circle':
            pygame.draw.circle(image, (0, 200, 0), (15, 15), 15)
            pygame.draw.circle(image, BLACK, (15, 15), 5)
        save_image(image, path)
    enemy_images[pattern] = pygame.transform.scale(image, (30, 30))

# Create Boss Images with Fallback
boss_patterns_list = ['burst_homing', 'spiral', 'circle', 'aimed', 'random', 'mass_acceleration']
boss_images = {}
for pattern in boss_patterns_list:
    path = os.path.join(sprites_dir, f'boss_{pattern}.png')
    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
    else:
        # Create a placeholder image
        image = pygame.Surface((100, 80), pygame.SRCALPHA)
        if pattern == 'burst_homing':
            pygame.draw.polygon(image, ORANGE, [(50, 0), (100, 80), (0, 80)])
        elif pattern == 'spiral':
            pygame.draw.arc(image, (255, 100, 0), (10, 10, 80, 60), 0, math.pi, 5)
        elif pattern == 'circle':
            pygame.draw.circle(image, ORANGE, (50, 40), 40)
            pygame.draw.circle(image, BLACK, (50, 40), 10)
        elif pattern == 'aimed':
            pygame.draw.polygon(image, ORANGE, [(50, 10), (90, 70), (10, 70)])
        elif pattern == 'random':
            pygame.draw.rect(image, (255, 140, 0), image.get_rect())
            pygame.draw.circle(image, BLACK, (50, 40), 15)
        elif pattern == 'mass_acceleration':
            pygame.draw.rect(image, (255, 215, 0), image.get_rect())
            pygame.draw.line(image, BLACK, (0, 40), (100, 40), 5)
        save_image(image, path)
    boss_images[pattern] = pygame.transform.scale(image, (100, 80))

# Create Backgrounds for Levels with Fallback
backgrounds = {}
for level in range(1, 11):
    path = os.path.join(backgrounds_dir, f'background_level_{level}.png')
    if os.path.exists(path):
        background = pygame.image.load(path).convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Create different background patterns based on level
        if level % 2 == 0:
            background.fill((min(20 * level, 255), min(30 * level, 255), min(40 * level, 255)))
        else:
            background.fill((min(40 * level, 255), min(20 * level, 255), min(30 * level, 255)))
        # Add stars or simple patterns
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH - 1)
            y = random.randint(0, SCREEN_HEIGHT - 1)
            pygame.draw.circle(background, WHITE, (x, y), 1)
        save_image(background, path)
    backgrounds[level] = background

# ====== Sprite Groups ======
all_sprites   = pygame.sprite.Group()
bullets       = pygame.sprite.Group()
bosses        = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemies       = pygame.sprite.Group()
power_points  = pygame.sprite.Group()

# ====== Game Variables ======
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

# ====== Player Class ======
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
        self.power_level = 0  # Ranges from 0 to 10
        self.pp_collected = 0
        self.pp_needed = 5  # Number of pp needed for next power-up

    def update(self):
        self.speedx = 0
        self.speedy = 0
        key_state = pygame.key.get_pressed()
        
        # Check if SHIFT key is held down to decrease speed
        if key_state[pygame.K_LSHIFT] or key_state[pygame.K_RSHIFT]:
            move_speed = self.base_speed / 2  # Reduce speed by half
        else:
            move_speed = self.base_speed
        
        if key_state[pygame.K_LEFT]:
            self.speedx = -move_speed
        if key_state[pygame.K_RIGHT]:
            self.speedx = move_speed
        if key_state[pygame.K_UP]:
            self.speedy = -move_speed
        if key_state[pygame.K_DOWN]:
            self.speedy = move_speed
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < PLAYER_AREA_Y - (SCREEN_HEIGHT / 3):
            self.rect.top = PLAYER_AREA_Y - (SCREEN_HEIGHT / 3)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Shooting with 'Z' key instead of SPACE
        if key_state[pygame.K_z]:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - getattr(self, 'last_shot', 0) > 250:
            self.last_shot = now
            # Fire bullets based on power level
            if self.power_level >= 10:
                # Max power level - 10 bullets with tilts
                angles = [-22.5, -15, -7.5, 0, 7.5, 15, 22.5, -22.5, -15, -7.5]
            elif self.power_level >= 8:
                # Power level 8-9 - 8 bullets with tilts
                angles = [-20, -10, 0, 10, 20, -20, -10, 10]
            elif self.power_level >= 6:
                # Power level 6-7 - 6 bullets with tilts
                angles = [-15, -7.5, 0, 7.5, 15, 0]
            elif self.power_level >= 4:
                # Power level 4-5 - 4 bullets with slight tilts
                angles = [-10, -5, 5, 10]
            elif self.power_level >= 2:
                # Power level 2-3 - 2 bullets with slight tilt
                angles = [-5, 5]
            else:
                # Power level 0-1 - single bullet
                angles = [0]

            for angle in angles:
                # Convert angle to radians
                rad = math.radians(angle)
                # Calculate bullet velocity
                bullet_speed = -12
                speedx = bullet_speed * math.sin(rad)
                speedy = bullet_speed * math.cos(rad)
                bullet = Bullet(self.rect.centerx, self.rect.top, speedx, speedy)
                all_sprites.add(bullet)
                bullets.add(bullet)
                # Play shoot sound
                if shoot_sound:
                    shoot_sound.play()

    def power_up(self):
        if self.power_level < 10:
            self.power_level += 1
            self.pp_collected = 0

# ====== Bullet Class ======
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, owner='player'):
        super(Bullet, self).__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedx = speedx
        self.speedy = speedy
        self.owner = owner  # 'player', 'enemy', 'boss'
        self.damage = 1

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Remove the bullet if it goes off-screen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# ====== Enemy Bullet Class ======
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy):
        super(EnemyBullet, self).__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedx = speedx
        self.speedy = speedy
        self.damage = 1

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Remove the bullet if it goes off-screen
        if self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# ====== Boss Bullet Class ======
class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, size=10, color=RED):
        super(BossBullet, self).__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.speedx = speedx
        self.speedy = speedy
        self.damage = 2  # Boss bullets deal more damage

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Remove the bullet if it goes off-screen
        if (self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0 or
            self.rect.right < 0 or self.rect.left > SCREEN_WIDTH):
            self.kill()

# ====== Enemy Class ======
class Enemy(pygame.sprite.Sprite):
    def __init__(self, level, pattern):
        super(Enemy, self).__init__()
        self.image = enemy_images.get(pattern, pygame.Surface((30, 30)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, PLAYER_AREA_Y - self.rect.height)
        # Allow movement both up and down
        self.speedy = random.choice([-2, 2]) + level * 0.5
        self.speedx = random.randint(-3, 3)
        self.hp = 3 + level  # Example HP scaling with level
        self.pattern = pattern
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000  # milliseconds

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Keep enemy within top two-thirds of the screen
        if self.rect.top < TOP_THIRD_Y_LIMIT:
            self.rect.top = TOP_THIRD_Y_LIMIT
            self.speedy = abs(self.speedy)  # Move down
        elif self.rect.bottom > PLAYER_AREA_Y:
            self.rect.bottom = PLAYER_AREA_Y
            self.speedy = -abs(self.speedy)  # Move up

        # Bounce off the sides
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speedx *= -1

        # Shooting based on pattern
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot()

        # Remove if off-screen vertically
        if self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0:
            self.kill()

    def shoot(self):
        if self.pattern == 'aimed':
            # Aim towards the player
            player_pos = player.rect.center
            enemy_pos = self.rect.center
            dx = player_pos[0] - enemy_pos[0]
            dy = player_pos[1] - enemy_pos[1]
            angle = math.atan2(dy, dx)
            speed = 5
            speedx = speed * math.cos(angle)
            speedy = speed * math.sin(angle)
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, speedx, speedy)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
        elif self.pattern == 'random':
            # Shoot in random direction
            angle = random.uniform(0, 2 * math.pi)
            speed = 5
            speedx = speed * math.cos(angle)
            speedy = speed * math.sin(angle)
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, speedx, speedy)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
        elif self.pattern == 'circle':
            # Shoot bullets in a circular pattern
            for i in range(8):
                angle = math.radians(i * 45)
                speed = 4
                speedx = speed * math.cos(angle)
                speedy = speed * math.sin(angle)
                bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, speedx, speedy)
                all_sprites.add(bullet)
                enemy_bullets.add(bullet)

    def die(self):
        if enemy_hit_sound:
            enemy_hit_sound.play()
        self.kill()

# ====== Boss Class ======
class Boss(pygame.sprite.Sprite):
    def __init__(self, level, pattern):
        super(Boss, self).__init__()
        self.image = boss_images.get(pattern, pygame.Surface((100, 80)))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.y = TOP_THIRD_Y_LIMIT  # Ensure boss is within top third
        self.health = 50 + level * 10  # Example health scaling
        self.pattern = pattern
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1500  # milliseconds
        # Allow movement both up and down within top third
        self.speedy = random.choice([-1, 1]) * 2

    def update(self):
        # Example boss movement pattern
        self.rect.x += math.sin(pygame.time.get_ticks() / 500) * 2
        self.rect.y += self.speedy

        # Keep boss within the top third of the screen
        if self.rect.top < 0:
            self.rect.top = 0
            self.speedy = abs(self.speedy)  # Move down
        elif self.rect.bottom > TOP_THIRD_Y_LIMIT:
            self.rect.bottom = TOP_THIRD_Y_LIMIT
            self.speedy = -abs(self.speedy)  # Move up

        # Shooting based on pattern
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot()

    def shoot(self):
        if self.pattern in ['aimed', 'burst_homing']:
            # Aim towards the player and shoot multiple bullets spread out
            player_pos = player.rect.center
            boss_pos = self.rect.center
            dx = player_pos[0] - boss_pos[0]
            dy = player_pos[1] - boss_pos[1]
            base_angle = math.atan2(dy, dx)
            spread = math.radians(30)  # 30 degrees spread
            num_bullets = 5  # Number of bullets to shoot simultaneously

            for i in range(num_bullets):
                angle = base_angle + spread * (i - num_bullets // 2) / num_bullets
                speed = 4
                speedx = speed * math.cos(angle)
                speedy = speed * math.sin(angle)
                bullet = BossBullet(self.rect.centerx, self.rect.bottom, speedx, speedy, size=12, color=ORANGE)
                all_sprites.add(bullet)
                enemy_bullets.add(bullet)

        elif self.pattern == 'random':
            # Shoot multiple bullets in random directions spread out
            num_bullets = 8
            for i in range(num_bullets):
                angle = random.uniform(0, 2 * math.pi)
                speed = 4
                speedx = speed * math.cos(angle)
                speedy = speed * math.sin(angle)
                bullet = BossBullet(self.rect.centerx, self.rect.bottom, speedx, speedy, size=12, color=PURPLE)
                all_sprites.add(bullet)
                enemy_bullets.add(bullet)

        elif self.pattern == 'circle':
            # Shoot bullets in a circular pattern from multiple points within top third
            num_bullets = 12
            spread = 360 / num_bullets
            for i in range(num_bullets):
                angle = math.radians(i * spread)
                speed = 3
                speedx = speed * math.cos(angle)
                speedy = speed * math.sin(angle)
                spawn_x = self.rect.centerx + random.randint(-30, 30)
                spawn_y = self.rect.bottom + random.randint(-10, 10)
                bullet = BossBullet(spawn_x, spawn_y, speedx, speedy, size=12, color=YELLOW)
                all_sprites.add(bullet)
                enemy_bullets.add(bullet)

        elif self.pattern == 'mass_acceleration':
            # Shoot multiple accelerating bullets towards the player
            num_bullets = 6
            for i in range(num_bullets):
                player_pos = player.rect.center
                boss_pos = self.rect.center
                dx = player_pos[0] - boss_pos[0] + random.randint(-50, 50)
                dy = player_pos[1] - boss_pos[1] + random.randint(-50, 50)
                angle = math.atan2(dy, dx)
                speed = 6
                speedx = speed * math.cos(angle)
                speedy = speed * math.sin(angle)
                bullet = BossBullet(self.rect.centerx, self.rect.bottom, speedx, speedy, size=14, color=RED)
                all_sprites.add(bullet)
                enemy_bullets.add(bullet)

    def die(self):
        if enemy_hit_sound:
            enemy_hit_sound.play()
        self.kill()

    def draw_health_bar(self, surface):
        ratio = self.health / (50 + level * 10)
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 10, 100, 5))
        pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 10, 100 * ratio, 5))

# ====== Functions to Display Messages ======
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

# ====== Function to Reset the Game ======
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

# ====== Function to Spawn Enemy Wave ======
def spawn_enemy_wave():
    global wave_start_time
    enemy_pattern = random.choice(['aimed', 'random', 'circle'])
    num_enemies = 2 + (level - 1) * 2
    for _ in range(num_enemies):
        enemy = Enemy(level, enemy_pattern)
        all_sprites.add(enemy)
        enemies.add(enemy)
    wave_start_time = pygame.time.get_ticks()

# ====== Function to Spawn Boss ======
def spawn_boss():
    global boss_spawned, boss_active
    pattern = boss_patterns.get(level, 'aimed')
    boss = Boss(level, pattern)
    all_sprites.add(boss)
    bosses.add(boss)
    boss_spawned = True
    boss_active = True

# ====== Create Player ======
player = Player()
all_sprites.add(player)

# ====== Load Backgrounds ======
for level_num in range(1, 11):
    try:
        backgrounds[level_num] = pygame.image.load(os.path.join(backgrounds_dir, f'background_level_{level_num}.png')).convert()
        backgrounds[level_num] = pygame.transform.scale(backgrounds[level_num], (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        backgrounds[level_num] = BLACK  # Fallback to black if image not found

# ====== Load Enemy Images ======
# Enemy Images are already loaded in enemy_images dictionary during asset creation

# ====== Load Boss Images ======
# Boss Images are already loaded in boss_images dictionary during asset creation

# ====== Main Game Loop ======
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

        # Enemy bullets hit player (using point collision)
        hit = False
        for bullet in enemy_bullets:
            if bullet.rect.collidepoint(player.rect.center):
                bullet.kill()
                hit = True
        if hit:
            player.lives -= 1
            if player.lives <= 0:
                game_over = True
            # Play player hit sound
            if player_hit_sound:
                player_hit_sound.play()

        # Enemies collide with player (using point collision)
        collide = False
        for enemy in enemies:
            if enemy.rect.collidepoint(player.rect.center):
                enemy.kill()
                collide = True
        if collide:
            player.lives -= 1
            if player.lives <= 0:
                game_over = True
            # Play player hit sound
            if player_hit_sound:
                player_hit_sound.play()

        # Power-ups collected by player
        pp_hits = pygame.sprite.spritecollide(player, power_points, True, pygame.sprite.collide_rect)
        for pp in pp_hits:
            player.pp_collected += 1
            if player.pp_collected >= player.pp_needed:
                player.power_up()

        # Level completion logic
        if level_complete:
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

        # Draw Player Hitbox (Small Red Point at Center)
        player_hitbox = player.rect.center
        pygame.draw.circle(screen, RED, player_hitbox, 3)

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

# ====== Delete All Sprites and Backgrounds After Game Window Closes ======
try:
    shutil.rmtree(sprites_dir)
    print(f"Deleted sprites directory: {sprites_dir}")
except Exception as e:
    print(f"Error deleting sprites directory: {e}")

try:
    shutil.rmtree(backgrounds_dir)
    print(f"Deleted backgrounds directory: {backgrounds_dir}")
except Exception as e:
    print(f"Error deleting backgrounds directory: {e}")

try:
    shutil.rmtree(sounds_dir)
    print(f"Deleted sounds directory: {sounds_dir}")
except Exception as e:
    print(f"Error deleting sounds directory: {e}")

pygame.quit()
sys.exit()