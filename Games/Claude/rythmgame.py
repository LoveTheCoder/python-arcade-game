from typing import Dict, List, Optional
import pygame
import random
import numpy as np
import json

running = True

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return default_config()

def default_config():
    return {
        'scroll_speed': 5,
        'difficulty': 1,
        'volume': 1.0,
        'key_bindings': {
            'left': pygame.K_d,
            'down': pygame.K_f,
            'up': pygame.K_j,
            'right': pygame.K_k
        }
    }

# Constants
WIDTH, HEIGHT = 400, 800
HIT_POSITION = HEIGHT - 100
SPAWN_INTERVAL = 1000  # Spawn new note every 2 seconds

STATE_RESULTS = 3  # New game state for results screen

APPROACH_TIME = 2.0  # Time in seconds for note to travel from spawn to hit position

# Scoring constants
PERFECT_WINDOW = 50  # ±50ms for perfect hit
GREAT_WINDOW = 100   # ±100ms for great hit
GOOD_WINDOW = 150    # ±150ms for good hit

# Hit scores
PERFECT_SCORE = 1000
GREAT_SCORE = 700
GOOD_SCORE = 300
MISS_SCORE = 0

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Key mapping
KEY_MAP = {
    pygame.K_d: 0,
    pygame.K_f: 1,
    pygame.K_j: 2,
    pygame.K_k: 3
}

def generate_square_wave(frequency, duration, amplitude=0.3, duty_cycle=0.5):
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples, False)
    wave = (np.sin(2 * np.pi * frequency * t) > -duty_cycle) * 2 - 1
    return (wave * amplitude * 32767).astype(np.int16)

def create_section(notes, pattern, durations, base_octave=4):
    return [(f"{note}{base_octave + octave}", dur) 
            for note, octave, dur in zip(pattern, durations[0], durations[1])]

def generate_music(melody):
    """Generate music from melody pattern"""
    notes = {
        'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61,
        'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
        'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
        'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
        'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
        'C6': 1046.50
    }
    
    # Bass line with steady rhythm
    base_duration = melody[0][1]  # Use first note's duration as reference
    half_note = base_duration * 2
    bass_pattern = [
        ('C3', half_note), ('G3', half_note), 
        ('A3', half_note), ('E3', half_note),
        ('F3', half_note), ('C3', half_note), 
        ('G3', half_note), ('C3', half_note)
    ]
    
    # Repeat bass pattern to match melody length
    total_melody_duration = sum(duration for _, duration in melody)
    bass_pattern_duration = sum(duration for _, duration in bass_pattern)
    num_repeats = int(total_melody_duration / bass_pattern_duration) + 1
    bass_line = bass_pattern * num_repeats
    
    sample_rate = 44100
    total_duration = sum(duration for _, duration in melody)
    buffer_size = int(total_duration * sample_rate)
    buffer = np.zeros((buffer_size, 2), dtype=np.int16)
    
    # Add melody
    current_time = 0
    for note, duration in melody:
        freq = notes[note]
        wave = generate_square_wave(freq, duration, amplitude=0.15)
        end_time = min(current_time + len(wave), buffer_size)
        if end_time > current_time:
            buffer[current_time:end_time] += np.column_stack((wave[:end_time-current_time], wave[:end_time-current_time]))
        current_time = end_time
    
    # Add bass with lower amplitude
    current_time = 0
    for note, duration in bass_line:
        if current_time >= buffer_size:
            break
        freq = notes[note]
        wave = generate_square_wave(freq, duration, amplitude=0.1, duty_cycle=0.3)
        end_time = min(current_time + len(wave), buffer_size)
        if end_time > current_time:
            buffer[current_time:end_time] += np.column_stack((wave[:end_time-current_time], wave[:end_time-current_time]))
        current_time = end_time
    
    # Normalize to prevent clipping
    buffer = (buffer * 0.8).astype(np.int16)
    
    return pygame.sndarray.make_sound(buffer), total_duration, melody


class Song:
    def __init__(self, name, bpm, base_duration, melody_func):
        self.name = name
        self.bpm = bpm
        self.base_duration = base_duration
        self.melody_func = melody_func

def create_slow_melody():
    base_duration = 0.25  # Quarter note at 120 BPM
    half_note = base_duration * 2
    quarter_note = base_duration
    eighth_note = base_duration / 2
    
    # Main theme - melodic and clear
    main_theme = [
        ('E4', quarter_note), ('G4', quarter_note), ('A4', half_note),
        ('C5', quarter_note), ('B4', quarter_note), ('A4', half_note),
        ('G4', quarter_note), ('E4', quarter_note), ('G4', half_note),
        ('A4', quarter_note), ('C5', quarter_note), ('B4', half_note),
    ]
    
    # Verse with moderate pace
    verse = [
        ('E4', eighth_note), ('G4', eighth_note), ('A4', quarter_note),
        ('B4', eighth_note), ('A4', eighth_note), ('G4', quarter_note),
        ('E5', eighth_note), ('D5', eighth_note), ('C5', quarter_note),
        ('A4', eighth_note), ('G4', eighth_note), ('E4', quarter_note),
        ('A4', quarter_note), ('B4', quarter_note), ('C5', half_note),
    ]
    
    # Chorus with clear rhythm
    chorus = [
        ('C5', quarter_note), ('E5', quarter_note), ('G5', half_note),
        ('F5', quarter_note), ('E5', quarter_note), ('D5', half_note),
        ('E5', quarter_note), ('D5', quarter_note), ('C5', half_note),
        ('B4', quarter_note), ('C5', quarter_note), ('D5', half_note),
    ]
    
    # Bridge section
    bridge = [
        ('E5', eighth_note), ('D5', eighth_note), ('C5', quarter_note),
        ('B4', eighth_note), ('A4', eighth_note), ('G4', quarter_note),
        ('A4', eighth_note), ('B4', eighth_note), ('C5', quarter_note),
        ('D5', eighth_note), ('E5', eighth_note), ('F5', quarter_note),
        ('E5', half_note), ('G5', half_note),
    ]
    
    # Finale
    finale = [
        ('C5', quarter_note), ('E5', quarter_note), ('G5', half_note),
        ('F5', quarter_note), ('D5', quarter_note), ('B4', half_note),
        ('C5', quarter_note), ('E5', quarter_note), ('G5', half_note),
        ('C6', quarter_note), ('G5', quarter_note), ('C5', half_note * 2),
    ]
    
    # Combine sections into full song
    melody = (
        main_theme * 2 +  # Introduce the main theme
        verse +          # First verse
        chorus +         # First chorus
        verse +          # Second verse
        chorus +         # Second chorus
        bridge +         # Bridge section
        chorus * 2 +     # Double chorus
        finale          # Epic ending
    )
    return melody

def create_fast_melody():
    base_duration = 0.125  # Eighth note at 180 BPM
    half_note = base_duration * 4
    quarter_note = base_duration * 2
    eighth_note = base_duration
    
    # Fast-paced energetic melody
    main_theme = [
        ('E4', eighth_note), ('G4', eighth_note), ('A4', quarter_note),
        ('C5', eighth_note), ('B4', eighth_note), ('A4', quarter_note),
        ('G4', eighth_note), ('E4', eighth_note), ('G4', quarter_note),
        ('A4', eighth_note), ('C5', eighth_note), ('B4', quarter_note),
    ]
    
    verse = [
        ('C5', eighth_note), ('E5', eighth_note), ('G5', eighth_note), ('A5', eighth_note),
        ('G5', eighth_note), ('E5', eighth_note), ('C5', quarter_note),
        ('B4', eighth_note), ('D5', eighth_note), ('F5', eighth_note), ('G5', eighth_note),
        ('F5', eighth_note), ('D5', eighth_note), ('B4', quarter_note),
    ]
    
    chorus = [
        ('A5', eighth_note), ('G5', eighth_note), ('E5', eighth_note), ('C5', eighth_note),
        ('D5', eighth_note), ('E5', eighth_note), ('F5', quarter_note),
        ('E5', eighth_note), ('D5', eighth_note), ('C5', eighth_note), ('B4', eighth_note),
        ('C5', quarter_note), ('G4', quarter_note),
    ]
    
    melody = main_theme * 2 + verse * 2 + chorus * 2
    return melody

def create_waltz_melody():
    base_duration = 0.2  # For 3/4 time at 140 BPM
    measure = base_duration * 3
    
    # Waltz rhythm (ONE-two-three pattern)
    theme = [
        ('C4', base_duration), ('E4', base_duration), ('G4', base_duration),
        ('G4', base_duration), ('C5', base_duration), ('E5', base_duration),
        ('E5', base_duration), ('C5', base_duration), ('G4', base_duration),
        ('G4', base_duration), ('E4', base_duration), ('C4', base_duration),
    ]
    
    variation = [
        ('F4', base_duration), ('A4', base_duration), ('C5', base_duration),
        ('C5', base_duration), ('F5', base_duration), ('A5', base_duration),
        ('G5', base_duration), ('E5', base_duration), ('C5', base_duration),
        ('C4', base_duration), ('E4', base_duration), ('G4', base_duration),
    ]
    
    melody = theme * 2 + variation * 2 + theme * 2
    return melody

# Define available songs
SONGS = [
    Song("Slow Melody", 120, 0.25, create_slow_melody),
    Song("Fast Beats", 180, 0.125, create_fast_melody),
    Song("Waltz Time", 140, 0.2, create_waltz_melody),
]

def generate_hit_sound(frequency=880, duration=0.1, amplitude=0.2):
    """
    Generate a hit sound with customizable parameters
    """
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples, False)
    wave = (np.sin(2 * np.pi * frequency * t) > -0.5) * 2 - 1
    wave = wave * amplitude * 32767
    return pygame.sndarray.make_sound(np.column_stack((wave, wave)).astype(np.int16))

def generate_hit_sounds():
    sounds = {
        'PERFECT': generate_hit_sound(880),  # Higher pitch for perfect
        'GREAT': generate_hit_sound(660),
        'GOOD': generate_hit_sound(440),
        'MISS': generate_hit_sound(220, 0.1)  # Lower pitch for miss
    }
    return sounds

# Main game states
STATE_MENU = 0
STATE_PLAY = 1
STATE_PAUSE = 2

# [Previous imports remain the same]

# Modified Constants
WIDTH, HEIGHT = 400, 800
HIT_POSITION = HEIGHT - 100
MIN_SCROLL_SPEED = 2
MAX_SCROLL_SPEED = 10

MUSIC_START_DELAY = 2000  # 2 seconds

class Note(pygame.sprite.Sprite):
    def __init__(self, column, speed, target_time):
        super().__init__()
        self.image = pygame.Surface((90, 20))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = column * 100
        self.rect.y = 0  # Start at top of screen
        self.column = column
        self.speed = speed * 2
        self.target_time = target_time
        self.spawn_time = target_time - (APPROACH_TIME * 1000)
        self.hit_status = None
        
    def update(self, current_time):
        time_since_spawn = current_time - self.spawn_time
        if time_since_spawn >= 0:
            # Calculate position based on time and speed
            progress = time_since_spawn / (APPROACH_TIME * 1000)
            self.rect.y = progress * HIT_POSITION
            if self.rect.top > HEIGHT and not self.hit_status:
                self.hit_status = "MISS"
                return "MISS"
        return None

def generate_note_map(melody, song, difficulty):
    note_map = []
    current_time = 0
    
    # Adjust timing based on song's BPM
    if difficulty == "Easy":
        note_chance = 0.6
        min_interval = 60 / song.bpm  # One beat
    elif difficulty == "Medium":
        note_chance = 0.8
        min_interval = 30 / song.bpm  # Half beat
    else:  # Hard
        note_chance = 1.0
        min_interval = 15 / song.bpm  # Quarter beat
    
    last_spawn_time = -min_interval
    
    for note, duration in melody:
        ms_time = int(current_time * 1000)
        
        if (current_time - last_spawn_time) >= min_interval and random.random() < note_chance:
            note_name = note[0]
            column_map = {
                'C': 0, 'D': 1, 'E': 2, 'F': 3,
                'G': 0, 'A': 1, 'B': 2
            }
            column = column_map[note_name]
            
            # Target time is when the note should be hit (on the beat)
            target_time = ms_time
            note_map.append((target_time, column))
            last_spawn_time = current_time
            
        current_time += duration
    
    return note_map, current_time * 1000

class ScoreTracker:
    def __init__(self):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.perfect_hits = 0
        self.great_hits = 0
        self.good_hits = 0
        self.misses = 0
        self.total_notes = 0
        
    def calculate_accuracy(self):
        if self.total_notes == 0:
            return 0
        weighted_hits = (self.perfect_hits * 100 + self.great_hits * 85 + self.good_hits * 50) / self.total_notes
        return weighted_hits
        
    def add_hit(self, hit_type, combo):
        if hit_type == "PERFECT":
            base_score = PERFECT_SCORE
            self.perfect_hits += 1
        elif hit_type == "GREAT":
            base_score = GREAT_SCORE
            self.great_hits += 1
        elif hit_type == "GOOD":
            base_score = GOOD_SCORE
            self.good_hits += 1
        else:  # MISS
            self.misses += 1
            return
            
        self.score += base_score * combo
        self.total_notes += 1
        
    def reset(self):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.perfect_hits = 0
        self.great_hits = 0
        self.good_hits = 0
        self.misses = 0
        self.total_notes = 0
        
class ResourceManager:
    def __init__(self):
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}
        
    def load_game_sounds(self):
        self.sounds['hit'] = generate_hit_sound()
        self.sounds['perfect'] = generate_hit_sound()  # Can modify frequency/duration
        self.sounds['great'] = generate_hit_sound()
        self.sounds['good'] = generate_hit_sound()
        
class GameState:
    def __init__(self, resources: ResourceManager):
        self.resources = resources
        self.current_state = STATE_MENU
        self.previous_state = None
        self.score_tracker = ScoreTracker()
        self.notes = pygame.sprite.Group()
        self.waiting_notes = []
        self.game_start_time = 0
        self.current_song = None
        
        # Menu state
        self.difficulties = ["Easy", "Medium", "Hard"]
        self.selected_difficulty = 0
        self.scroll_speed = 5
        self.selected_song_index = 0
        self.selected_menu_item = 0  # 0=song, 1=difficulty, 2=speed
        self.pause_options = ["Resume", "Restart", "Exit to Menu"]
        self.selected_pause_option = 0
        self.music_position = 0  # Track music position for pausing
        self.music_start_timer = 0  # Track when to start music
        self.song_finished = False  # Track if song is complete

def create_melody():
    """
    Default melody creation if no specific melody function is provided
    """
    return create_slow_melody()  # Use slow melody as default

def update(game_state, notes, waiting_notes, scroll_speed, score_tracker, current_time, song_duration):
    """Updates game logic"""
    
    if game_state.current_state == STATE_PLAY:
        # Update notes
        for note in notes.sprites():
            result = note.update(current_time) 
            if result == "MISS":
                score_tracker.combo = 0
                score_tracker.misses += 1
                note.kill()
                
        # Spawn new notes if available
        if waiting_notes:
            while waiting_notes and waiting_notes[0][0] - (APPROACH_TIME * 1000) <= current_time:
                target_time, column = waiting_notes.pop(0)
                new_note = Note(column, scroll_speed, target_time)
                notes.add(new_note)
            
        # Check if song finished
        if current_time >= song_duration * 1000 and not notes and not waiting_notes:
            game_state.current_state = STATE_RESULTS
            
    return game_state.current_state

def render(screen, game_state, notes, score_tracker, menu_font):
    """Renders game graphics"""
    screen.fill((0, 0, 0))
    
    if game_state.current_state == STATE_PLAY:
        # Draw gameplay elements
        if notes:
            notes.draw(screen)
        
        # Draw hit line
        pygame.draw.line(screen, WHITE, (0, HIT_POSITION), (WIDTH, HIT_POSITION), 2)
        
        # Draw score at top left
        score_text = menu_font.render(f"Score: {score_tracker.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw combo in center
        if score_tracker.combo > 0:
            combo_text = menu_font.render(str(score_tracker.combo), True, WHITE)
            combo_pos = (WIDTH//2 - combo_text.get_width()//2, HEIGHT//2 - 50)
            screen.blit(combo_text, combo_pos)
        
        # Calculate and show accuracy percentage
        if score_tracker.total_notes > 0:
            accuracy = ((score_tracker.perfect_hits * 100 + 
                        score_tracker.great_hits * 75 + 
                        score_tracker.good_hits * 50) / 
                       (score_tracker.total_notes * 100)) * 100
            acc_text = menu_font.render(f"{accuracy:.1f}%", True, WHITE)
            screen.blit(acc_text, (WIDTH - acc_text.get_width() - 10, 10))

def handle_menu_input(event, game_state):
    """Add this function above main()"""
    if event.key == pygame.K_UP:
        if game_state.selected_menu_item == 0:
            game_state.selected_song_index = (game_state.selected_song_index - 1) % len(SONGS)
        elif game_state.selected_menu_item == 1:
            game_state.selected_difficulty = (game_state.selected_difficulty - 1) % len(game_state.difficulties)
    elif event.key == pygame.K_DOWN:
        if game_state.selected_menu_item == 0:
            game_state.selected_song_index = (game_state.selected_song_index + 1) % len(SONGS)
        elif game_state.selected_menu_item == 1:
            game_state.selected_difficulty = (game_state.selected_difficulty + 1) % len(game_state.difficulties)
    elif event.key == pygame.K_LEFT and game_state.selected_menu_item == 2:
        game_state.scroll_speed = max(MIN_SCROLL_SPEED, game_state.scroll_speed - 1)
    elif event.key == pygame.K_RIGHT and game_state.selected_menu_item == 2:
        game_state.scroll_speed = min(MAX_SCROLL_SPEED, game_state.scroll_speed + 1)
    elif event.key == pygame.K_TAB:
        game_state.selected_menu_item = (game_state.selected_menu_item + 1) % 3

# First, create a helper function to handle song start (add this before main()):
def start_song(game_state):
    """Helper function to start/restart songs with consistent behavior"""
    game_state.notes.empty()
    game_state.score_tracker.reset()
    game_state.waiting_notes = generate_note_map(
        game_state.current_song.melody_func(),
        game_state.current_song,
        game_state.difficulties[game_state.selected_difficulty]
    )[0]
    game_state.game_start_time = pygame.time.get_ticks() + MUSIC_START_DELAY
    game_state.music_start_timer = pygame.time.get_ticks() + MUSIC_START_DELAY
    game_state.current_state = STATE_PLAY

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("4K Rhythm Game")
    clock = pygame.time.Clock()
    
    resources = ResourceManager()
    resources.load_game_sounds()
    game_state = GameState(resources)
    menu_font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if game_state.current_state == STATE_MENU:
                    if event.key == pygame.K_RETURN:
                        # Load song first
                        game_state.current_song = SONGS[game_state.selected_song_index]
                        melody = game_state.current_song.melody_func()
                        game_state.music, duration, _ = generate_music(melody)
                        # Start song with same behavior as restart
                        start_song(game_state)
                    else:
                        handle_menu_input(event, game_state)
                
                elif game_state.current_state == STATE_PLAY:
                    if event.key == pygame.K_ESCAPE:
                        game_state.current_state = STATE_PAUSE
                        game_state.music.stop()  # Use Sound object methods
                    elif event.key in KEY_MAP:
                        handle_note_hit(event.key, game_state, game_state.notes, game_state.score_tracker)
                
                elif game_state.current_state == STATE_PAUSE:
                    if event.key == pygame.K_ESCAPE:
                        game_state.current_state = STATE_PLAY
                        game_state.music.play(start=game_state.music_position/1000.0)  # Resume from saved position
                    elif event.key == pygame.K_UP:
                        game_state.selected_pause_option = (game_state.selected_pause_option - 1) % len(game_state.pause_options)
                    elif event.key == pygame.K_DOWN:
                        game_state.selected_pause_option = (game_state.selected_pause_option + 1) % len(game_state.pause_options)
                    elif event.key == pygame.K_RETURN:
                        if game_state.selected_pause_option == 0:  # Resume
                            game_state.current_state = STATE_PLAY
                            game_state.music.play(start=game_state.music_position/1000.0)
                        elif game_state.selected_pause_option == 1:  # Restart
                            start_song(game_state)
                        elif game_state.selected_pause_option == 2:  # Exit to Menu
                            game_state.current_state = STATE_MENU
                            game_state.notes.empty()
                            game_state.score_tracker.reset()
                            game_state.music.stop()
        
        # Update game state
        if game_state.current_state == STATE_PLAY:
            current_time = pygame.time.get_ticks() - game_state.game_start_time
            
            # Handle music start delay
            if game_state.music_start_timer and pygame.time.get_ticks() >= game_state.music_start_timer:
                game_state.music.play()
                game_state.music_start_timer = 0
            
            # Spawn new notes
            while game_state.waiting_notes and game_state.waiting_notes[0][0] - (APPROACH_TIME * 1000) <= current_time:
                target_time, column = game_state.waiting_notes.pop(0)
                new_note = Note(column, game_state.scroll_speed, target_time)
                game_state.notes.add(new_note)
            
            # Update existing notes
            for note in game_state.notes:
                result = note.update(current_time)
                if result == "MISS":
                    game_state.score_tracker.combo = 0
                    game_state.score_tracker.misses += 1
                    note.kill()
            
            # Check for song completion
            if (not game_state.waiting_notes and 
                not game_state.notes and 
                not game_state.music_start_timer and 
                current_time >= duration * 1000):
                game_state.current_state = STATE_RESULTS
                game_state.song_finished = True
        
        elif game_state.current_state == STATE_RESULTS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_state.selected_pause_option == 0:  # Replay
                        game_state.notes.empty()
                        game_state.score_tracker.reset()
                        game_state.waiting_notes = generate_note_map(
                            game_state.current_song.melody_func(),
                            game_state.current_song,
                            game_state.difficulties[game_state.selected_difficulty]
                        )[0]
                        game_state.game_start_time = pygame.time.get_ticks() + MUSIC_START_DELAY
                        game_state.music_start_timer = pygame.time.get_ticks() + MUSIC_START_DELAY
                        game_state.current_state = STATE_PLAY
                    else:  # Back to menu
                        game_state.current_state = STATE_MENU
                        game_state.song_finished = False

        # Render current state
        screen.fill((0, 0, 0))
        
        if game_state.current_state == STATE_MENU:
            draw_menu(screen, menu_font, game_state.difficulties, 
                     game_state.selected_difficulty, game_state.scroll_speed, 
                     game_state.selected_song_index)
        
        elif game_state.current_state == STATE_PLAY:
            render(screen, game_state, game_state.notes, game_state.score_tracker, menu_font)
        
        elif game_state.current_state == STATE_PAUSE:
            draw_pause_menu(screen, menu_font, game_state.pause_options, 
                          game_state.selected_pause_option)
        
        elif game_state.current_state == STATE_RESULTS:
            draw_results_screen(screen, game_state.score_tracker, menu_font)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def draw_menu(screen, font, difficulties, selected_difficulty, scroll_speed, selected_song_index):
    """Draw the main menu screen"""
    # Title
    title = font.render("Rhythm Game", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    # Song selection
    for i, song in enumerate(SONGS):
        color = WHITE if i == selected_song_index else GRAY
        text = font.render(song.name, True, color)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 200 + i*40))
    
    # Difficulty
    diff_text = font.render(f"Difficulty: {difficulties[selected_difficulty]}", True, WHITE)
    screen.blit(diff_text, (WIDTH//2 - diff_text.get_width()//2, 400))
    
    # Speed
    speed_text = font.render(f"Scroll Speed: {scroll_speed}", True, WHITE)
    screen.blit(speed_text, (WIDTH//2 - speed_text.get_width()//2, 450))
    
    # Instructions
    inst_text = font.render("Press ENTER to start", True, WHITE)
    screen.blit(inst_text, (WIDTH//2 - inst_text.get_width()//2, 550))

def draw_pause_menu(screen, font, options, selected_option):
    """Draw the pause menu screen"""
    # Darkened overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    # Pause title
    title = font.render("PAUSED", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
    
    # Options
    for i, option in enumerate(options):
        color = WHITE if i == selected_option else GRAY
        text = font.render(option, True, color)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 300 + i*50))

def draw_results(screen, font, score_tracker):
    """Draw the results screen"""
    # Results title
    title = font.render("Results", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    # Score breakdown
    stats = [
        f"Score: {score_tracker.total_score}",
        f"Max Combo: {score_tracker.max_combo}",
        f"Perfect: {score_tracker.perfects}",
        f"Great: {score_tracker.greats}",
        f"Good: {score_tracker.goods}",
        f"Miss: {score_tracker.misses}"
    ]
    
    for i, stat in enumerate(stats):
        text = font.render(stat, True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 200 + i*50))

def handle_note_hit(key, game_state, notes, score_tracker):
    """Handle note hit detection and scoring"""
    if key not in KEY_MAP:
        return
        
    column = KEY_MAP[key]
    current_time = pygame.time.get_ticks() - game_state.game_start_time
    
    # Find closest note in column
    column_notes = [note for note in notes if note.column == column]
    if not column_notes:
        return
        
    closest_note = min(column_notes, 
                      key=lambda n: abs(current_time - n.target_time))
    time_diff = abs(current_time - closest_note.target_time)
    
    # Determine hit quality
    if time_diff <= PERFECT_WINDOW:
        score = PERFECT_SCORE
        hit_type = "PERFECT"
    elif time_diff <= GREAT_WINDOW:
        score = GREAT_SCORE
        hit_type = "GREAT"
    elif time_diff <= GOOD_WINDOW:
        score = GOOD_SCORE
        hit_type = "GOOD"
    else:
        score = MISS_SCORE
        hit_type = "MISS"
    
    # Update score and combo
    if hit_type != "MISS":
        score_tracker.combo += 1
        score_tracker.max_combo = max(score_tracker.max_combo, score_tracker.combo)
        score_tracker.add_hit(hit_type, score)
        game_state.resources.sounds['hit'].play()
        closest_note.kill()
    else:
        score_tracker.combo = 0
        score_tracker.misses += 1

def draw_results_screen(screen, score_tracker, font):
    """Renders the results screen showing final score and statistics"""
    # Background overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(200)
    screen.blit(overlay, (0, 0))
    
    # Title
    title = font.render("Results", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    # Calculate final accuracy
    if score_tracker.total_notes > 0:
        accuracy = ((score_tracker.perfect_hits * 100 + 
                    score_tracker.great_hits * 75 + 
                    score_tracker.good_hits * 50) / 
                   (score_tracker.total_notes * 100)) * 100
    else:
        accuracy = 0
    
    # Stats to display
    stats = [
        f"Final Score: {score_tracker.score}",
        f"Max Combo: {score_tracker.max_combo}",
        f"Accuracy: {accuracy:.1f}%",
        "",
        f"Perfect: {score_tracker.perfect_hits} ({(score_tracker.perfect_hits/score_tracker.total_notes*100):.1f}%)" if score_tracker.total_notes > 0 else "Perfect: 0",
        f"Great: {score_tracker.great_hits} ({(score_tracker.great_hits/score_tracker.total_notes*100):.1f}%)" if score_tracker.total_notes > 0 else "Great: 0",
        f"Good: {score_tracker.good_hits} ({(score_tracker.good_hits/score_tracker.total_notes*100):.1f}%)" if score_tracker.total_notes > 0 else "Good: 0",
        f"Miss: {score_tracker.misses} ({(score_tracker.misses/score_tracker.total_notes*100):.1f}%)" if score_tracker.total_notes > 0 else "Miss: 0"
    ]
    
    # Draw stats
    for i, stat in enumerate(stats):
        text = font.render(stat, True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 200 + i*40))
    
    # Continue prompt
    prompt = font.render("Press Enter to continue", True, WHITE)
    screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT - 100))

if __name__ == "__main__":
    main()