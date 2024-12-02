import pygame
import random
import time
import os

# Define the paths
base_path = os.path.dirname(os.path.abspath(__file__))
assets_path = os.path.join(base_path, 'assets')
songs_path = os.path.join(assets_path, 'songs')
skin_path = os.path.join(assets_path, 'skin')

# Create the directories
os.makedirs(songs_path, exist_ok=True)
os.makedirs(skin_path,  exist_ok=True)

print("Folders created successfully.")

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Columns and keys
COLUMNS = 4
COLUMN_WIDTHS = [65, 65, 65, 65]
COLUMN_START = 310
KEYS = [pygame.K_a, pygame.K_s, pygame.K_k, pygame.K_l]

# Note settings
NOTE_WIDTHS = COLUMN_WIDTHS
NOTE_HEIGHT = 20
NOTE_SPEED = 5
HIT_POSITION = 456  # Extracted from (old)skin.ini

# Load song
song_path = os.path.join(songs_path, 'song.mp3')
pygame.mixer.music.load(song_path)
pygame.mixer.music.play()

# Load graphics
note_images = [
    pygame.image.load(os.path.join(skin_path, 'Skin 1', 'Notes4K', 'RedLeft.png')),
    pygame.image.load(os.path.join(skin_path, 'Skin 1', 'Notes4K', 'BlueDown.png')),
    pygame.image.load(os.path.join(skin_path, 'Skin 1', 'Notes4K', 'BlueUp.png')),
    pygame.image.load(os.path.join(skin_path, 'Skin 1', 'Notes4K', 'RedRight.png'))
]

# Maintain aspect ratio for note images
note_images = [pygame.transform.scale(img, (NOTE_WIDTHS[i], int(img.get_height() * (NOTE_WIDTHS[i] / img.get_width())))) for i, img in enumerate(note_images)]

key_images = [
    pygame.image.load(os.path.join(skin_path, 'Skin 1', 'Keys4K', 'Left.png')),
    pygame.image.load(os.path.join(skin_path, 'Skin 1', 'Keys4K', 'Down.png')),
    pygame.image.load(os.path.join(skin_path, 'Skin 1', 'Keys4K', 'Up.png')),
    pygame.image.load(os.path.join(skin_path, 'Skin 1', 'Keys4K', 'Right.png'))
]

key_pressed_images = [
    pygame.image.load(os.path.join(skin_path, 'Skin 1', 'Keys4K', 'LeftPressed.png')),
    pygame.image.load(os.path.join(skin_path, 'Skin 1', 'Keys4K', 'DownPressed.png')),
    pygame.image.load(os.path.join(skin_path, 'Skin 1', 'Keys4K', 'UpPressed.png')),
    pygame.image.load(os.path.join(skin_path, 'Skin 1', 'Keys4K', 'RightPressed.png'))
]

# Maintain aspect ratio for key images
key_images = [pygame.transform.scale(img, (NOTE_WIDTHS[i], int(img.get_height() * (NOTE_WIDTHS[i] / img.get_width())))) for i, img in enumerate(key_images)]
key_pressed_images = [pygame.transform.scale(img, (NOTE_WIDTHS[i], int(img.get_height() * (NOTE_WIDTHS[i] / img.get_width())))) for i, img in enumerate(key_pressed_images)]

# Load hit sounds
hit_sounds = [
    pygame.mixer.Sound(os.path.join(skin_path, 'Skin 1', 'drum-hitclap.wav')),
    pygame.mixer.Sound(os.path.join(skin_path, 'Skin 1', 'drum-hitfinish.wav')),
    pygame.mixer.Sound(os.path.join(skin_path, 'Skin 1', 'drum-hitnormal.wav')),
    pygame.mixer.Sound(os.path.join(skin_path, 'Skin 1', 'drum-hitwhistle.wav'))
]

# Game variables
notes = []
score = 0
total_notes = 0
hit_notes = 0
combo = 0

# Font
font = pygame.font.Font(None, 36)

def create_note():
    column = random.randint(0, COLUMNS - 1)
    note = pygame.Rect(COLUMN_START + sum(NOTE_WIDTHS[:column]), 0, NOTE_WIDTHS[column], NOTE_HEIGHT)
    notes.append((note, column))

def draw_notes():
    for note, column in notes:
        screen.blit(note_images[column], note)

def draw_keys():
    keys = pygame.key.get_pressed()
    for i, img in enumerate(key_images):
        if keys[KEYS[i]]:
            screen.blit(key_pressed_images[i], (COLUMN_START + sum(NOTE_WIDTHS[:i]), HIT_POSITION))
        else:
            screen.blit(img, (COLUMN_START + sum(NOTE_WIDTHS[:i]), HIT_POSITION))

def draw_lines():
    for i in range(COLUMNS + 1):
        x = COLUMN_START + sum(NOTE_WIDTHS[:i])
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))

def update_notes():
    global score, hit_notes, total_notes, combo
    for note, column in notes:
        note.y += NOTE_SPEED
        if note.y > HEIGHT:
            notes.remove((note, column))
            total_notes += 1
            combo = 0

def check_hits():
    global score, hit_notes, total_notes, combo
    keys = pygame.key.get_pressed()
    for note, column in notes:
        if keys[KEYS[column]] and note.colliderect(pygame.Rect(COLUMN_START + sum(NOTE_WIDTHS[:column]), HIT_POSITION, NOTE_WIDTHS[column], NOTE_HEIGHT)):
            notes.remove((note, column))
            score += 100
            hit_notes += 1
            total_notes += 1
            combo += 1
            hit_sounds[column].play()
            break

def draw_score():
    accuracy = (hit_notes / total_notes) * 100 if total_notes > 0 else 0
    score_text = font.render(f"Score: {score}", True, WHITE)
    accuracy_text = font.render(f"Accuracy: {accuracy:.2f}%", True, WHITE)
    combo_text = font.render(f"Combo: {combo}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(accuracy_text, (10, 50))
    screen.blit(combo_text, (WIDTH // 2 - combo_text.get_width() // 2, 10))

# Main game loop
running = True
clock = pygame.time.Clock()
last_note_time = time.time()

while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create notes at intervals
    if time.time() - last_note_time > 0.5:
        create_note()
        last_note_time = time.time()

    update_notes()
    check_hits()
    draw_notes()
    draw_keys()
    draw_lines()
    draw_score()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()