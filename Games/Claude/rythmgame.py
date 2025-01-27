import pygame
import random
import numpy as np

# Constants
WIDTH, HEIGHT = 400, 800
HIT_POSITION = HEIGHT - 100
SPAWN_INTERVAL = 1000  # Spawn new note every 2 seconds

STATE_RESULTS = 3  # New game state for results screen

APPROACH_TIME = 2.0  # Time in seconds for note to travel from spawn to hit position

# Scoring constants
PERFECT_WINDOW = 10  # ±10ms for perfect hit
GREAT_WINDOW = 20    # ±20ms for great hit
GOOD_WINDOW = 35     # ±35ms for good hit

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

def create_melody():
    # Slower tempo with longer note durations
    base_duration = 0.25  # Quarter note
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
    
    # Combine sections into full song with repetitions
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

def generate_music(melody_func=None):
    notes = {
        'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61,
        'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
        'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
        'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
        'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
        'C6': 1046.50
    }
    
    melody = melody_func() if melody_func else create_melody()
    
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

def generate_hit_sound():
    duration = 0.1
    frequency = 880
    wave1 = generate_square_wave(frequency, duration, 0.2)
    wave2 = generate_square_wave(frequency * 1.5, duration, 0.1)
    combined_wave = wave1 + wave2
    buffer = np.column_stack((combined_wave, combined_wave))
    return pygame.sndarray.make_sound(buffer)

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

class Note(pygame.sprite.Sprite):
    def __init__(self, column, speed, target_time):
        super().__init__()
        self.image = pygame.Surface((90, 20))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = column * 100
        self.rect.y = 0  # Start at top of screen
        self.column = column
        self.speed = speed
        self.target_time = target_time
        self.spawn_time = target_time - (APPROACH_TIME * 1000)  
        self.hit_status = None
        self.total_distance = HIT_POSITION  # Total distance to travel
        
    def update(self, current_time):
        time_since_spawn = current_time - self.spawn_time
        if time_since_spawn >= 0:
            # Calculate position as a percentage of total travel time
            progress = time_since_spawn / (APPROACH_TIME * 1000)
            self.rect.y = progress * self.total_distance
            if self.rect.top > HEIGHT:
                if not self.hit_status:
                    self.hit_status = "MISS"
                self.kill()

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

def evaluate_hit_timing(note, current_time):
    time_diff = abs(current_time - note.target_time)
    if time_diff <= PERFECT_WINDOW:
        return "PERFECT"
    elif time_diff <= GREAT_WINDOW:
        return "GREAT"
    elif time_diff <= GOOD_WINDOW:
        return "GOOD"
    return "MISS"

def draw_results_screen(screen, score_tracker, menu_font):
    # Draw results title
    title_text = menu_font.render("Results", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
    
    # Calculate grade based on accuracy
    accuracy = score_tracker.calculate_accuracy()
    if accuracy >= 95:
        grade = "S"
    elif accuracy >= 90:
        grade = "A"
    elif accuracy >= 80:
        grade = "B"
    elif accuracy >= 70:
        grade = "C"
    else:
        grade = "D"
    
    # Draw grade
    grade_text = pygame.font.Font(None, 72).render(grade, True, WHITE)
    screen.blit(grade_text, (WIDTH // 2 - grade_text.get_width() // 2, 120))
    
    # Draw statistics
    stats = [
        f"Score: {score_tracker.score}",
        f"Max Combo: {score_tracker.max_combo}",
        f"Accuracy: {accuracy:.2f}%",
        f"Perfect: {score_tracker.perfect_hits}",
        f"Great: {score_tracker.great_hits}",
        f"Good: {score_tracker.good_hits}",
        f"Miss: {score_tracker.misses}",
        f"Total Notes: {score_tracker.total_notes}"
    ]
    
    for i, stat in enumerate(stats):
        stat_text = menu_font.render(stat, True, WHITE)
        screen.blit(stat_text, (WIDTH // 2 - stat_text.get_width() // 2, 200 + i * 40))
    
    # Draw "Press Enter to continue" text
    continue_text = menu_font.render("Press Enter to continue", True, WHITE)
    screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT - 100))

def draw_menu(screen, menu_font, difficulties, selected_difficulty, scroll_speed, selected_song_index):
    # Draw title
    title_text = menu_font.render("4K Rhythm Game", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # Draw song selection
    song_text = menu_font.render(f"Song: {SONGS[selected_song_index].name}", True, WHITE)
    screen.blit(song_text, (WIDTH // 2 - song_text.get_width() // 2, 120))
    
    # Draw difficulty and speed settings
    difficulty_text = menu_font.render(f"Difficulty: {difficulties[selected_difficulty]}", True, WHITE)
    screen.blit(difficulty_text, (WIDTH // 2 - difficulty_text.get_width() // 2, 170))
    
    speed_text = menu_font.render(f"Scroll Speed: {scroll_speed}", True, WHITE)
    screen.blit(speed_text, (WIDTH // 2 - speed_text.get_width() // 2, 220))

    # Draw controls
    controls_text = [
        "Controls:",
        "W/S: Change Song",
        "↑↓: Change Difficulty",
        "←→: Adjust Scroll Speed",
        "Enter: Start Game",
        "D F J K: Hit Notes",
        "Esc: Pause Game"
    ]
    for i, text in enumerate(controls_text):
        rendered_text = menu_font.render(text, True, WHITE)
        screen.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, 300 + i * 40))

def draw_pause_menu(screen, menu_font, pause_options, selected_pause_option):
    # Draw pause title
    title_text = menu_font.render("PAUSED", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    # Draw pause options
    for i, option in enumerate(pause_options):
        color = WHITE if i == selected_pause_option else GRAY
        option_text = menu_font.render(option, True, color)
        screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 200 + i * 50))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("4K Rhythm Game")
    clock = pygame.time.Clock()

    # Initialize game variables
    notes = pygame.sprite.Group()
    score_tracker = ScoreTracker()
    hit_sound = generate_hit_sound()
    
    # Menu setup
    menu_font = pygame.font.Font(None, 36)
    difficulties = ["Easy", "Medium", "Hard"]
    selected_difficulty = 0
    scroll_speed = 5
    selected_song_index = 0
    
    # Add scroll speed adjustment to menu
    scroll_speeds = list(range(MIN_SCROLL_SPEED, MAX_SCROLL_SPEED + 1))
    selected_speed_index = 3
    
    # Pause menu options
    pause_options = ["Resume", "Restart", "Main Menu"]
    selected_pause_option = 0
    
    # Game state
    game_state = STATE_MENU
    note_map = None
    waiting_notes = None
    current_song = None
    music = None
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and game_state == STATE_PLAY:
                    game_state = STATE_PAUSE
                    pygame.mixer.pause()
                elif game_state == STATE_MENU:
                    if event.key == pygame.K_w:  # Song selection
                        selected_song_index = (selected_song_index - 1) % len(SONGS)
                    elif event.key == pygame.K_s:
                        selected_song_index = (selected_song_index + 1) % len(SONGS)
                    elif event.key == pygame.K_UP:
                        selected_difficulty = (selected_difficulty - 1) % len(difficulties)
                    elif event.key == pygame.K_DOWN:
                        selected_difficulty = (selected_difficulty + 1) % len(difficulties)
                    elif event.key == pygame.K_LEFT:
                        selected_speed_index = max(0, selected_speed_index - 1)
                        scroll_speed = scroll_speeds[selected_speed_index]
                    elif event.key == pygame.K_RIGHT:
                        selected_speed_index = min(len(scroll_speeds) - 1, selected_speed_index + 1)
                        scroll_speed = scroll_speeds[selected_speed_index]
                    elif event.key == pygame.K_RETURN:
                        # Start new game with selected song
                        current_song = SONGS[selected_song_index]
                        melody = current_song.melody_func()
                        music, song_duration, _ = generate_music(current_song.melody_func)  # Pass the melody function
                        note_map, total_duration = generate_note_map(melody, current_song, difficulties[selected_difficulty])
                        waiting_notes = note_map.copy()
                        game_state = STATE_PLAY
                        notes.empty()
                        score_tracker = ScoreTracker()
                        game_start_time = pygame.time.get_ticks()
                        music.play(0)
                elif game_state == STATE_PAUSE:
                    if event.key == pygame.K_UP:
                        selected_pause_option = (selected_pause_option - 1) % len(pause_options)
                    elif event.key == pygame.K_DOWN:
                        selected_pause_option = (selected_pause_option + 1) % len(pause_options)
                    elif event.key == pygame.K_RETURN:
                        if pause_options[selected_pause_option] == "Resume":
                            game_state = STATE_PLAY
                            pygame.mixer.unpause()
                        elif pause_options[selected_pause_option] == "Restart":
                            melody = current_song.melody_func()
                            note_map, total_duration = generate_note_map(melody, current_song, difficulties[selected_difficulty])
                            waiting_notes = note_map.copy()
                            game_state = STATE_PLAY
                            notes.empty()
                            score_tracker = ScoreTracker()
                            game_start_time = pygame.time.get_ticks()
                            music.play(0)
                        else:  # Main Menu
                            game_state = STATE_MENU
                            pygame.mixer.stop()
                            notes.empty()
                            
                elif game_state == STATE_RESULTS:
                    if event.key == pygame.K_RETURN:
                        game_state = STATE_MENU
                        pygame.mixer.stop()
                        notes.empty()
                        score_tracker = ScoreTracker()
                
                elif game_state == STATE_PLAY and event.key in KEY_MAP:
                    column = KEY_MAP[event.key]
                    current_time = pygame.time.get_ticks() - game_start_time
                    hit_notes = [note for note in notes if note.column == column and 
                               abs(current_time - note.target_time) <= GOOD_WINDOW]
                    if hit_notes:
                        closest_note = min(hit_notes, key=lambda n: abs(current_time - n.target_time))
                        hit_status = evaluate_hit_timing(closest_note, current_time)
                        closest_note.hit_status = hit_status
                        
                        if hit_status != "MISS":
                            score_tracker.combo += 1
                            score_tracker.max_combo = max(score_tracker.max_combo, score_tracker.combo)
                            score_tracker.add_hit(hit_status, score_tracker.combo)
                            hit_sound.play()
                            closest_note.kill()
                        else:
                            score_tracker.combo = 0
                            score_tracker.misses += 1

        screen.fill((0, 0, 0))
        
        if game_state == STATE_MENU:
            draw_menu(screen, menu_font, difficulties, selected_difficulty, scroll_speed, selected_song_index)
        
        elif game_state == STATE_PLAY:
            current_time = pygame.time.get_ticks() - game_start_time
            
            # Check if song is finished
            if current_time >= song_duration * 1000 and not notes and not waiting_notes:
                game_state = STATE_RESULTS
            else:
                # Spawn notes according to the note map
                while waiting_notes and waiting_notes[0][0] - (APPROACH_TIME * 1000) <= current_time:
                    target_time, column = waiting_notes.pop(0)
                    note = Note(column, scroll_speed, target_time)
                    notes.add(note)
                
                # Update and draw notes
                for note in notes:
                    note.update(current_time)
                notes.draw(screen)
                
                # Draw UI elements
                pygame.draw.line(screen, WHITE, (0, HIT_POSITION), (WIDTH, HIT_POSITION), 2)
                score_text = menu_font.render(f"Score: {score_tracker.score}", True, WHITE)
                combo_text = menu_font.render(f"Combo: {score_tracker.combo} Max: {score_tracker.max_combo}", True, WHITE)
                screen.blit(score_text, (10, 10))
                screen.blit(combo_text, (WIDTH - combo_text.get_width() - 10, 10))
        
        elif game_state == STATE_RESULTS:
            draw_results_screen(screen, score_tracker, menu_font)
        
        elif game_state == STATE_PAUSE:
            draw_pause_menu(screen, menu_font, pause_options, selected_pause_option)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()