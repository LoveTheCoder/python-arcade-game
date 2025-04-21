import pygame
import sys
import os
import random
import math
from .character import Character
from .ai_opponent import AIOpponent

# Add Game States
STATE_START_MENU = 0
STATE_LEVEL_SELECT = 1
STATE_ATTACK_LIST = 2
STATE_GAME_RUNNING = 3
STATE_PAUSED = 4
STATE_GAME_OVER_WIN = 5  # New state
STATE_GAME_OVER_LOSE = 6  # New state

# --- Background Generation Function ---
def generate_level_background(level, width, height, floor_level):
    """Generates a unique background surface for the given level."""
    background = pygame.Surface((width, height))
    sky_height = floor_level
    ground_height = height - floor_level

    # --- Sky ---
    if level == 0:  # Practice Room Sky
        background.fill((180, 180, 180), (0, 0, width, sky_height))  # Light grey sky/ceiling
        # Grid lines on the sky/ceiling
        for x in range(0, width, 50):
            pygame.draw.line(background, (150, 150, 150), (x, 0), (x, sky_height), 1)
        for y in range(0, sky_height, 50):
            pygame.draw.line(background, (150, 150, 150), (0, y), (width, y), 1)
    elif level == 1:  # Grassy Field (Day)
        # Blue gradient sky
        for y in range(sky_height):
            color = (135 - int(y / sky_height * 80), 206 - int(y / sky_height * 60), 250 - int(y / sky_height * 40))
            pygame.draw.line(background, color, (0, y), (width, y))
        # Simple Sun
        pygame.draw.circle(background, (255, 255, 0), (width - 80, 60), 40)
        # Simple Clouds
        for _ in range(3):
            cx, cy, cr = random.randint(50, width - 50), random.randint(50, sky_height - 80), random.randint(20, 50)
            pygame.draw.circle(background, (255, 255, 255), (cx, cy), cr)
            pygame.draw.circle(background, (240, 240, 240), (cx + int(cr * 0.6), cy + int(cr * 0.1)), int(cr * 0.8))

    elif level == 2:  # City Rooftop (Day)
        # Light blue sky
        background.fill((170, 210, 240), (0, 0, width, sky_height))
        # Distant buildings (simple rectangles)
        for i in range(15):
            b_width = random.randint(40, 100)
            b_height = random.randint(50, sky_height - 50)
            b_x = random.randint(-20, width - b_width + 20)
            b_y = sky_height - b_height
            b_color = random.randint(80, 150)
            pygame.draw.rect(background, (b_color, b_color, b_color + 10), (b_x, b_y, b_width, b_height))
            # Simple windows
            for wx in range(b_x + 5, b_x + b_width - 5, 15):
                for wy in range(b_y + 5, b_y + b_height - 5, 15):
                    pygame.draw.rect(background, (200, 200, 220), (wx, wy, 5, 8))

    elif level == 3:  # Desert
        # Pale blue sky, slight gradient
        for y in range(sky_height):
            color = (180 - int(y / sky_height * 30), 210 - int(y / sky_height * 20), 230)
            pygame.draw.line(background, color, (0, y), (width, y))
        # Sun
        pygame.draw.circle(background, (255, 240, 180), (width // 2, 70), 50)

    elif level == 4:  # Snowy Mountain
        # Light grey/blue sky
        for y in range(sky_height):
            color = (190 + int(y / sky_height * 20), 200 + int(y / sky_height * 20), 210 + int(y / sky_height * 30))
            pygame.draw.line(background, color, (0, y), (width, y))
        # Mountain peaks
        peaks = [(0, sky_height - 50), (100, 150), (200, sky_height - 80), (300, 100), (450, sky_height - 30), (600, 120), (700, sky_height - 100), (width, 150)]
        pygame.draw.polygon(background, (180, 180, 190), peaks)  # Darker base
        snow_peaks = [(p[0], p[1] - random.randint(10, 40)) for p in peaks[1:-1]]  # Slightly offset snow caps
        snow_peaks = [peaks[0]] + snow_peaks + [peaks[-1]]
        pygame.draw.polygon(background, (240, 240, 250), snow_peaks)  # Snow caps

    elif level == 5:  # Forest
        # Dark green/blue sky (filtered through canopy)
        for y in range(sky_height):
            color = (20 - int(y / sky_height * 15), 60 - int(y / sky_height * 40), 40 - int(y / sky_height * 30))
            pygame.draw.line(background, color, (0, y), (width, y))
        # Simple tree trunks in distance
        for i in range(10):
            t_x = random.randint(0, width)
            t_h = random.randint(sky_height // 2, sky_height)
            t_w = random.randint(10, 30)
            t_color = random.randint(40, 80)
            pygame.draw.rect(background, (t_color, t_color - 10, t_color - 20), (t_x, sky_height - t_h, t_w, t_h))

    elif level == 6:  # Volcano
        # Dark red/orange gradient sky
        for y in range(sky_height):
            r = 100 - int(y / sky_height * 80)
            g = 40 - int(y / sky_height * 30)
            b = 10
            pygame.draw.line(background, (r, g, b), (0, y), (width, y))
        # Volcano cone
        volcano_base_y = sky_height - 20
        volcano_points = [(width * 0.2, volcano_base_y), (width * 0.5, 100), (width * 0.8, volcano_base_y)]
        pygame.draw.polygon(background, (50, 40, 40), volcano_points)
        # Lava glow at top
        pygame.draw.circle(background, (255, 100, 0), (width * 0.5, 110), 30)
        pygame.draw.circle(background, (255, 180, 0), (width * 0.5, 110), 15)

    elif level == 7:  # Beach
        # Blue sky
        for y in range(sky_height // 2):
            color = (100 + int(y / (sky_height // 2) * 50), 180 + int(y / (sky_height // 2) * 50), 255)
            pygame.draw.line(background, color, (0, y), (width, y))
        # Ocean gradient
        for y in range(sky_height // 2, sky_height):
            color = (0, 150 - int((y - sky_height // 2) / (sky_height // 2) * 80), 200 - int((y - sky_height // 2) / (sky_height // 2) * 80))
            pygame.draw.line(background, color, (0, y), (width, y))
        # Sun
        pygame.draw.circle(background, (255, 255, 100), (100, 80), 40)

    elif level == 8:  # City Rooftop (Night)
        # Dark blue/purple gradient sky
        for y in range(sky_height):
            color = (30 - int(y / sky_height * 20), 20 - int(y / sky_height * 15), 60 - int(y / sky_height * 30))
            pygame.draw.line(background, color, (0, y), (width, y))
        # Moon
        pygame.draw.circle(background, (240, 240, 220), (width - 100, 70), 35)
        # Distant buildings (dark silhouettes)
        for i in range(15):
            b_width = random.randint(40, 120)
            b_height = random.randint(60, sky_height - 40)
            b_x = random.randint(-20, width - b_width + 20)
            b_y = sky_height - b_height
            b_color = random.randint(20, 50)
            pygame.draw.rect(background, (b_color, b_color, b_color + 5), (b_x, b_y, b_width, b_height))
            # Yellow windows
            for _ in range(int(b_width * b_height / 400)):  # Random number of windows
                wx = b_x + random.randint(5, b_width - 10)
                wy = b_y + random.randint(5, b_height - 15)
                if random.random() < 0.7:  # Chance window is lit
                    pygame.draw.rect(background, (255, 255, 100), (wx, wy, 5, 8))

    elif level == 9:  # Space Station Interior
        # Fill with metallic grey
        background.fill((100, 105, 110))
        # Panel lines
        for x in range(0, width, 80):
            pygame.draw.line(background, (80, 85, 90), (x, 0), (x, height), 2)
        for y in range(0, height, 80):
            pygame.draw.line(background, (80, 85, 90), (0, y), (width, y), 2)
        # Simple "window" to space
        window_rect = pygame.Rect(width // 2 - 150, 50, 300, 150)
        pygame.draw.rect(background, (10, 10, 20), window_rect)  # Space color
        for _ in range(20):  # Stars in window
            sx = random.randint(window_rect.left, window_rect.right)
            sy = random.randint(window_rect.top, window_rect.bottom)
            pygame.draw.circle(background, (255, 255, 255), (sx, sy), random.randint(1, 2))
        pygame.draw.rect(background, (150, 155, 160), window_rect, 5)  # Window frame

    elif level == 10:  # Outer Space
        # Black background
        background.fill((0, 0, 0))
        # Stars
        for _ in range(250):
            sx = random.randint(0, width)
            sy = random.randint(0, height)
            s_color = random.choice([(255, 255, 255), (200, 200, 255), (255, 200, 200)])
            pygame.draw.circle(background, s_color, (sx, sy), random.randint(1, 2))
        # Simple Nebula effect (large, faint, overlapping circles)
        for _ in range(5):
            nx = random.randint(0, width)
            ny = random.randint(0, height // 2)
            nr = random.randint(100, 300)
            n_color = random.choice([(50, 0, 80, 50), (0, 50, 80, 50), (80, 30, 0, 50)])  # RGBA with low alpha
            nebula_surf = pygame.Surface((nr * 2, nr * 2), pygame.SRCALPHA)
            pygame.draw.circle(nebula_surf, n_color, (nr, nr), nr)
            background.blit(nebula_surf, (nx - nr, ny - nr), special_flags=pygame.BLEND_RGBA_ADD)

    else:  # Default fallback
        background.fill((40, 0, 40))  # Dark Purple

    # --- Ground ---
    ground_rect = (0, floor_level, width, ground_height)
    if level == 0:  # Practice Room Floor
        pygame.draw.rect(background, (100, 100, 100), ground_rect)  # Dark grey floor
        # Grid lines on the floor
        for x in range(0, width, 50):
            pygame.draw.line(background, (80, 80, 80), (x, floor_level), (x, height), 1)
        for y in range(floor_level, height, 50):
            pygame.draw.line(background, (80, 80, 80), (0, y), (width, y), 1)
    elif level == 1:  # Grass
        for y in range(floor_level, height):
            g = 100 + int((y - floor_level) / ground_height * 50)
            color = (0, g, 0)
            pygame.draw.line(background, color, (0, y), (width, y))
    elif level == 2 or level == 8:  # Rooftop
        pygame.draw.rect(background, (70, 70, 75), ground_rect)  # Dark grey concrete
    elif level == 3:  # Desert Sand
        for y in range(floor_level, height):
            r = 240 - int((y - floor_level) / ground_height * 40)
            g = 200 - int((y - floor_level) / ground_height * 40)
            b = 100 - int((y - floor_level) / ground_height * 40)
            pygame.draw.line(background, (r, g, b), (0, y), (width, y))
    elif level == 4:  # Snow
        pygame.draw.rect(background, (220, 220, 230), ground_rect)
    elif level == 5:  # Forest Floor
        pygame.draw.rect(background, (50, 30, 10), ground_rect)
    elif level == 6:  # Volcanic Rock
        pygame.draw.rect(background, (60, 50, 50), ground_rect)
        # Lava cracks
        for _ in range(5):
            lx1, ly1 = random.randint(0, width), random.randint(floor_level, height)
            lx2, ly2 = lx1 + random.randint(-50, 50), ly1 + random.randint(-30, 30)
            pygame.draw.line(background, (255, 100, 0), (lx1, ly1), (lx2, ly2), random.randint(2, 4))
    elif level == 7:  # Sand
        pygame.draw.rect(background, (245, 222, 179), ground_rect)  # Sandy color
    elif level == 9:  # Station Floor (already filled)
        pass
    elif level == 10:  # Space (no ground)
        pass
    else:  # Default
        pygame.draw.rect(background, (30, 30, 30), ground_rect)

    return background
# --- End Background Generation ---

# --- Menu Background Helper ---
def draw_menu_gradient(surface, color1, color2):
    """Draws a vertical gradient filling the surface."""
    height = surface.get_height()
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))
# --- End Menu Background Helper ---

# --- Projectile Class ---
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right, owner):
        super().__init__()
        self.owner = owner  # Store who fired it
        self.image = pygame.Surface((25, 15), pygame.SRCALPHA)
        # Simple fireball graphic
        pygame.draw.ellipse(self.image, (255, 150, 0), self.image.get_rect())  # Orange ellipse
        pygame.draw.circle(self.image, (255, 255, 0), (12, 7), 5)  # Yellow core
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8
        self.velocity_x = self.speed if facing_right else -self.speed
        self.damage = 30  # Or get from combo_moves

    def update(self, screen_width):
        self.rect.x += self.velocity_x
        # Remove if off-screen
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()  # Remove from all groups

# --- End Projectile Class ---

class FightingGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.clock = clock

        # --- Load Fonts ---
        # Try loading a font known to support symbols, fallback to default
        try:
            # Use a font likely to have the symbols (adjust size as needed)
            # Common options: "Arial", "Segoe UI Symbol", "DejaVu Sans"
            self.font = pygame.font.SysFont("Arial", 30)
            self.title_font = pygame.font.SysFont("Arial", 60)
            print("Using Arial font.")
        except:
            print("Arial font not found, falling back to default Pygame font.")
            # Fallback to default if the specified font isn't found
            self.font = pygame.font.Font(None, 32)
            self.title_font = pygame.font.Font(None, 64)
        # --- End Load Fonts ---

        self.max_levels = 10
        self.current_level = 1

        self.player = None
        self.opponent = None
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.combo_moves = {
            ("punch", "punch", "kick"): {"name": "Fireball", "damage": 30, "type": "projectile"},
            ("kick", "punch"): {"name": "Uppercut", "damage": 25}
        }
        self.floor_level = 400
        self.winner = None
        self.basic_attacks = {
            "Q": "Punch",
            "W": "Kick"
        }
        self.running = False  # Initialize running flag

        # Menu/State Management
        self.game_state = STATE_START_MENU
        self.start_menu_options = ["Start Game", "Attack List", "Exit"]
        self.selected_start_option = 0
        self.pause_options = ["Resume", "Quit to Start Menu"]
        self.selected_pause_option = 0
        self.selected_level = 0  # Default selection to Practice
        self.game_over_message = "" # To store win/lose message

        # --- Attack List Scroll State ---
        self.attack_list_scroll_offset = 0
        self.attack_list_total_items = 0 # Will be calculated later
        self.attack_list_visible_items = 8 # Max items visible at once (adjust as needed)
        # --- End Attack List Scroll State ---

        self.current_background = None

    def initialize_game_session(self, level):
        """Sets up player, opponent, and background for the selected level."""
        self.current_level = level
        self.player = Character("Player", 100, self.floor_level, self.clock, self.screen_width)

        if level == 0:  # Practice Level Setup
            # Create a dummy opponent
            self.opponent = AIOpponent("Dummy", self.screen_width - 100, self.floor_level, self.clock, self.screen_width, level=0)  # Pass level 0
            # Make the dummy passive and invincible (or very high health)
            self.opponent.attack_frequency = 0.0  # Never attack
            self.opponent.combo_chance = 0.0  # Never combo
            self.opponent.health = 99999  # Effectively infinite health
            self.opponent.can_take_damage = False  # Add a flag to prevent damage logic
            print("Initialized Practice Mode: Dummy opponent created.")
        else:  # Normal Level Setup
            self.opponent = AIOpponent("Opponent", self.screen_width - 100, self.floor_level, self.clock, self.screen_width, self.current_level)
            self.opponent.can_take_damage = True  # Normal opponents can take damage

        self.all_sprites.empty()
        self.all_sprites.add(self.player, self.opponent)
        self.winner = None
        self.current_background = generate_level_background(level, self.screen_width, self.screen_height, self.floor_level)
        self.game_state = STATE_GAME_RUNNING

    def draw_attack_list(self):
        """Draws the screen displaying basic attacks and combos with scrolling."""
        draw_menu_gradient(self.screen, (30, 0, 30), (60, 0, 60))
        title_text = self.title_font.render("Attack List", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 60)) # Move title up
        self.screen.blit(title_text, title_rect)

        start_y = 120 # Start drawing items lower
        text_color = (220, 220, 220)
        line_height = 35 # Slightly smaller line height
        max_visible_y = self.screen_height - 80 # Limit drawing area

        # --- Combine all items into a single list for easier scrolling ---
        all_items = []
        all_items.append(("--- Basic Moves ---", (200, 200, 255))) # Add title with color
        basic_moves = {
            "ARROWS": "Move", "UP": "Jump", "DOWN": "Crouch/Block",
            "Q": "Punch", "E": "Kick", "SPACE": "Dodge"
        }
        for key, move in basic_moves.items():
            all_items.append((f"{key}: {move}", text_color))

        all_items.append(("", text_color)) # Spacer
        all_items.append(("--- Combo Moves ---", (200, 200, 255))) # Add title with color

        dir_symbols = {'up': '↑', 'down': '↓', 'left': '←', 'right': '→'}
        # Use the actual combo_moves from a character instance if possible, else default
        combos_to_display = {}
        if self.player:
            combos_to_display = self.player.combo_moves
        else: # Fallback if player doesn't exist yet (e.g., called from menu)
             combos_to_display = {
                 (('down', 'right'), 'punch'): {"name": "Fireball"},
                 (('left', 'down', 'right'), 'punch'): {"name": "Throw"},
                 (('down', 'right'), 'kick'): {"name": "SpinKick"}
             }

        for (directions, attack_trigger), move_info in combos_to_display.items():
            dir_string = " ".join(dir_symbols.get(d, d) for d in directions)
            trigger_key = "Q" if attack_trigger == "punch" else "E" if attack_trigger == "kick" else attack_trigger.upper()
            combo_text_str = f"{dir_string} + {trigger_key}: {move_info['name']}"
            all_items.append((combo_text_str, text_color))

        self.attack_list_total_items = len(all_items)

        # --- Determine visible range ---
        start_index = self.attack_list_scroll_offset
        end_index = min(self.attack_list_total_items, start_index + self.attack_list_visible_items)

        # --- Draw visible items ---
        current_y = start_y
        for i in range(start_index, end_index):
            item_text, item_color = all_items[i]
            if not item_text: # Skip empty spacers
                current_y += line_height // 2
                continue

            text_surface = self.font.render(item_text, True, item_color)
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, current_y))

            # Only blit if within visible area vertically
            if text_rect.bottom < max_visible_y:
                self.screen.blit(text_surface, text_rect)
            current_y += line_height

        # --- Draw Scroll Indicators (Optional) ---
        if self.attack_list_total_items > self.attack_list_visible_items:
            # Up arrow if not at top
            if self.attack_list_scroll_offset > 0:
                up_arrow = self.font.render("↑", True, (150, 150, 255))
                up_rect = up_arrow.get_rect(center=(self.screen_width - 40, start_y))
                self.screen.blit(up_arrow, up_rect)
            # Down arrow if not at bottom
            if self.attack_list_scroll_offset < self.attack_list_total_items - self.attack_list_visible_items:
                down_arrow = self.font.render("↓", True, (150, 150, 255))
                down_rect = down_arrow.get_rect(center=(self.screen_width - 40, max_visible_y - line_height // 2))
                self.screen.blit(down_arrow, down_rect)


        # --- Footer ---
        back_text = self.font.render("Press ESC to return", True, (200, 200, 200))
        back_rect = back_text.get_rect(center=(self.screen_width // 2, self.screen_height - 40))
        self.screen.blit(back_text, back_rect)

    def draw_start_menu(self):
        draw_menu_gradient(self.screen, (0, 0, 20), (0, 0, 80))
        title_text = self.title_font.render("Fighting Game", True, (0, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        self.screen.blit(title_text, title_rect)
        for i, option in enumerate(self.start_menu_options):
            text_color = (0, 255, 255) if i == self.selected_start_option else (180, 180, 180)
            option_text = self.font.render(option, True, text_color)
            option_rect = option_text.get_rect(center=(self.screen_width // 2, 250 + i * 60))
            self.screen.blit(option_text, option_rect)

    def draw_level_select(self):
        """Draws the level selection screen, including Practice."""
        draw_menu_gradient(self.screen, (20, 20, 0), (80, 80, 0))
        title_text = self.title_font.render("Select Level", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 80))
        self.screen.blit(title_text, title_rect)

        cols = 5
        total_options = self.max_levels + 1 # Levels 0 to max_levels
        rows = (total_options + cols - 1) // cols
        box_width = 100
        box_height = 60
        start_x = (self.screen_width - cols * (box_width + 20) + 20) // 2
        start_y = 150

        # Iterate from 0 (Practice) up to max_levels
        for level_num in range(total_options):
            row = level_num // cols
            col = level_num % cols
            x = start_x + col * (box_width + 20)
            y = start_y + row * (box_height + 20)
            rect = pygame.Rect(x, y, box_width, box_height)

            is_selected = (level_num == self.selected_level)
            border_color = (0, 255, 0) if is_selected else (255, 255, 255)
            fill_color = (80, 80, 100) if is_selected else (50, 50, 70)

            pygame.draw.rect(self.screen, fill_color, rect, border_radius=8)
            pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=8)

            # Display "P" for Practice, numbers for others
            level_display_text = "P" if level_num == 0 else str(level_num)
            level_text = self.font.render(level_display_text, True, border_color)
            level_rect = level_text.get_rect(center=rect.center)
            self.screen.blit(level_text, level_rect)

        back_text = self.font.render("ESC to Go Back", True, (200, 200, 200))
        back_rect = back_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        self.screen.blit(back_text, back_rect)

    def draw_health_bar(self, surface, character, x, y):
        BAR_LENGTH = 200
        BAR_HEIGHT = 20
        fill = (character.health / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        col = (0, 255, 0) if character.health > 60 else (255, 255, 0) if character.health > 30 else (255, 0, 0)
        pygame.draw.rect(surface, col, fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)
        name_text = self.font.render(character.name, True, (255, 255, 255))
        surface.blit(name_text, (x, y + BAR_HEIGHT + 5))

    def draw_game_over_screen(self):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200)) # Darker overlay
        self.screen.blit(overlay, (0, 0))

        # Display Win/Loss Message
        result_color = (0, 255, 0) if self.game_state == STATE_GAME_OVER_WIN else (255, 0, 0)
        result_text = self.title_font.render(self.game_over_message, True, result_color)
        result_rect = result_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(result_text, result_rect)

        # Display prompt to continue
        prompt_text = self.font.render("Press ENTER to return to menu", True, (200, 200, 200))
        prompt_rect = prompt_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        self.screen.blit(prompt_text, prompt_rect)

    def handle_start_input(self):
        """Handles input for the main start menu of the fighting game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"  # Signal exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_start_option = (self.selected_start_option - 1) % len(self.start_menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_start_option = (self.selected_start_option + 1) % len(self.start_menu_options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_start_option == 0:  # Start Game -> Go to Level Select
                        self.game_state = STATE_LEVEL_SELECT
                        self.selected_level = 1  # Reset level selection
                    elif self.selected_start_option == 1:  # Attack List
                        self.game_state = STATE_ATTACK_LIST
                    elif self.selected_start_option == 2:  # Exit (Return to main arcade menu)
                        self.running = False  # Stop this game's loop
                        return "QUIT"  # Signal exit from this game instance
                elif event.key == pygame.K_ESCAPE:  # Allow ESC to exit from this game's menu
                    self.running = False
                    return "QUIT"
        return None  # No action taken this frame

    def handle_level_select_input(self):
        """Handles input for level selection, including Practice."""
        total_options = self.max_levels + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = STATE_START_MENU
                    return None
                elif event.key == pygame.K_RETURN:
                    self.initialize_game_session(self.selected_level)
                    return None # Stay in game loop, state changed
                elif event.key == pygame.K_UP:
                    self.selected_level = (self.selected_level - 1) % total_options
                elif event.key == pygame.K_DOWN:
                    self.selected_level = (self.selected_level + 1) % total_options
                elif event.key == pygame.K_LEFT:
                    self.selected_level = max(0, self.selected_level - 1)
                elif event.key == pygame.K_RIGHT:
                    self.selected_level = min(total_options - 1, self.selected_level + 1)
        return None

    def handle_game_over_input(self):
        """Handles input on the game over screen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.reset_game_state() # Go back to the main menu
                elif event.key == pygame.K_ESCAPE: # Also allow ESC to go back
                     self.reset_game_state()
        return None

    def handle_input(self):
        """Handles player input during the game running state."""
        performed_attack_type = None

        # --- Single Event Loop (Handles KEYDOWN for buffer) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = STATE_PAUSED
                    self.selected_pause_option = 0
                    return None

                # Actions triggered on key press
                if self.player:
                    # --- Add Directional Inputs to Buffer on KEYDOWN ---
                    if event.key == pygame.K_UP:
                        self.player._add_direction_to_buffer('up')
                        self.player.jump() # Still trigger jump action
                    elif event.key == pygame.K_DOWN:
                        self.player._add_direction_to_buffer('down')
                        self.player.crouch() # Still trigger crouch action
                    elif event.key == pygame.K_LEFT:
                         self.player._add_direction_to_buffer('left')
                         # Movement itself is handled by get_pressed below
                    elif event.key == pygame.K_RIGHT:
                         self.player._add_direction_to_buffer('right')
                         # Movement itself is handled by get_pressed below
                    # --- End Buffer Input ---

                    # Attack / Dodge Inputs
                    elif event.key == pygame.K_q: # Punch
                        performed_attack_type = self.player.attack("punch")
                    elif event.key == pygame.K_e: # Kick
                        performed_attack_type = self.player.attack("kick")
                    elif event.key == pygame.K_SPACE:
                        self.player.dodge() # Dodge action

            if event.type == pygame.KEYUP:
                # Stop crouching when DOWN key is released
                if self.player and event.key == pygame.K_DOWN:
                    self.player.stand()

        # --- Continuous Movement (outside event loop, uses get_pressed) ---
        # This block now ONLY handles the actual movement, not buffer input
        if self.player and self.game_state == STATE_GAME_RUNNING:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move_left() # Call movement method
            if keys[pygame.K_RIGHT]:
                self.player.move_right() # Call movement method

        # --- Process Attack (if any was performed) ---
        if performed_attack_type and self.opponent:
            self.handle_attack(self.player, self.opponent, performed_attack_type)

        return None

    def handle_attack(self, attacker, defender, attack_name):
        """Processes the specific attack/combo performed."""
        print(f"Handling attack: {attack_name}")

        # --- Handle Projectile Spawning ---
        if attack_name == "Fireball":
            # ... (Fireball logic) ...
            spawn_x = attacker.rect.right + 10 if attacker.facing_right else attacker.rect.left - 10
            spawn_y = attacker.rect.centery - 10
            fireball = Projectile(spawn_x, spawn_y, attacker.facing_right, attacker)
            self.all_sprites.add(fireball)
            self.projectiles.add(fireball)
            return # Fireball handled

        # --- Get Attack Info ---
        attack_info = attacker.attacks.get(attack_name)
        if not attack_info:
             print(f"CRITICAL WARNING: Attack info not found for '{attack_name}' in attacker.attacks!")
             return

        damage = attack_info.get("damage", 0)
        attack_range = attack_info.get("range", attacker.rect.width)

        # --- Throw Logic ---
        if attack_name == "Throw":
            # Check for stun on throw attempt vs dodge
            if abs(attacker.rect.centerx - defender.rect.centerx) < attack_range and \
               abs(attacker.rect.centery - defender.rect.centery) < attacker.rect.height:
                if defender.is_dodging:
                    print(f"{attacker.name} stunned attempting throw on dodging {defender.name}!")
                    attacker.stun(1000) # Stun attacker for 1 second
                    return # Stop throw processing
                # ... (rest of throw success/fail logic) ...
                if not defender.is_dodging and not defender.is_crouching:
                    print(f"{attacker.name} throws {defender.name}!")
                    defender.take_damage(damage)
                    throw_distance = 150
                    defender.rect.x += throw_distance if attacker.facing_right else -throw_distance
                else: print(f"{attacker.name}'s throw failed (dodged/blocked)!")
            else: print(f"{attacker.name}'s throw missed (out of range)!")
            return # Throw handled or missed

        # --- Standard Melee Damage Application (Handles Punch, Kick, SpinKick) ---
        # Check for stun FIRST if defender is dodging
        if defender.is_dodging:
            # Calculate potential hit area to see if the attack *would* have hit
            attack_rect_width = attack_range
            attack_rect_height = attacker.rect.height
            if attacker.facing_right:
                attack_rect = pygame.Rect(attacker.rect.right, attacker.rect.top, attack_rect_width, attack_rect_height)
            else:
                attack_rect = pygame.Rect(attacker.rect.left - attack_rect_width, attacker.rect.top, attack_rect_width, attack_rect_height)

            # If the attack would have collided with the dodging defender
            if attack_rect.colliderect(defender.rect):
                print(f"{attacker.name} stunned attacking dodging {defender.name} with {attack_name}!")
                attacker.stun(1000) # Stun attacker for 1 second
                return # Stop attack processing

        # If defender is NOT dodging, proceed with damage application
        self.apply_damage(defender, damage, attacker.facing_right, attacker, attack_name, attack_range)

    def apply_damage(self, defender, damage, facing_right, attacker, attack_type, attack_range):
        """Applies damage based on hitbox collision, checks if defender can take damage."""
        # Immunity check
        if hasattr(defender, 'can_take_damage') and not defender.can_take_damage:
            return

        # Dodge check (handled in handle_attack for stun)
        if defender.is_dodging:
             return # Dodging characters take no damage

        # --- Handle Projectile Damage Directly ---
        if attack_type == "Projectile":
            # Collision already confirmed before calling apply_damage for projectiles
            if defender.is_crouching: # Blocking check
                print(f"{defender.name} blocked Projectile!")
                defender.take_damage(damage * 0.25)
            else: # Apply full damage
                defender.take_damage(damage)
                print(f"{defender.name} takes {damage} damage from Projectile!")
            return # Projectile damage handled

        # --- Handle Melee Damage (Calculate Hitbox) ---
        else:
            # Calculate attack hitbox based on attacker's position, facing direction, and attack range
            attack_rect_width = attack_range
            attack_rect_height = attacker.rect.height # Use attacker's height for the hitbox vertical size

            if facing_right:
                # Hitbox starts at the right edge of the attacker and extends
                attack_rect = pygame.Rect(attacker.rect.right, attacker.rect.top, attack_rect_width, attack_rect_height)
            else:
                # Hitbox starts attack_range pixels to the left of the attacker's left edge
                attack_rect = pygame.Rect(attacker.rect.left - attack_rect_width, attacker.rect.top, attack_rect_width, attack_rect_height)

            # Check for collision between the attack hitbox and the defender's rectangle
            if attack_rect.colliderect(defender.rect):
                 if defender.is_crouching: # Blocking check
                     print(f"{defender.name} blocked {attack_type}!")
                     defender.take_damage(damage * 0.25)
                 else: # Apply full damage
                    defender.take_damage(damage)
                    print(f"{defender.name} takes {damage} damage from {attack_type}!")
            # else: Melee attack missed

    def run(self):
        """Main loop for the Fighting Game instance."""
        self.running = True
        # Ensure initial state is set (e.g., start menu) if not done in init
        if self.game_state is None: # Add a check just in case
             self.game_state = STATE_START_MENU

        while self.running:
            dt = self.clock.tick(60) / 1000.0 # Delta time
            action = None # Action to take based on input handling

            # --- State Machine Logic ---
            if self.game_state == STATE_START_MENU:
                self.draw_start_menu()
                action = self.handle_start_input()
                if action == "QUIT": # Check if handle_start_input signals exit
                    self.running = False # Stop this game's loop

            elif self.game_state == STATE_LEVEL_SELECT:
                self.draw_level_select()
                action = self.handle_level_select_input()
                if action == "QUIT":
                    self.running = False

            elif self.game_state == STATE_ATTACK_LIST:
                self.draw_attack_list()
                # Handle input for attack list screen (including scrolling)
                for event in pygame.event.get([pygame.QUIT, pygame.KEYDOWN]):
                    if event.type == pygame.QUIT:
                        self.running = False; action = "QUIT"; break
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.game_state = STATE_START_MENU
                            self.attack_list_scroll_offset = 0 # Reset scroll on exit
                            break
                        elif event.key == pygame.K_UP:
                            self.attack_list_scroll_offset = max(0, self.attack_list_scroll_offset - 1)
                        elif event.key == pygame.K_DOWN:
                            max_scroll = max(0, self.attack_list_total_items - self.attack_list_visible_items)
                            self.attack_list_scroll_offset = min(max_scroll, self.attack_list_scroll_offset + 1)
                if action == "QUIT": break

            elif self.game_state == STATE_GAME_RUNNING:
                # Handle game input
                action = self.handle_input()
                if action == "QUIT":
                     self.running = False
                     break # Exit loop immediately on QUIT

                # Update Sprites
                if self.player: self.player.update()
                if self.opponent:
                    opponent_action_name = self.opponent.update(self.player)
                    if opponent_action_name:
                        self.handle_attack(self.opponent, self.player, opponent_action_name)

                # Update Projectiles
                self.projectiles.update(self.screen_width)

                # Check Projectile Collisions
                for proj in self.projectiles:
                    target = None
                    if proj.owner == self.player and self.opponent:
                        target = self.opponent
                    elif proj.owner == self.opponent and self.player:
                        target = self.player

                    if target and pygame.sprite.collide_rect(proj, target):
                        print(f"{target.name} hit by projectile!")
                        self.apply_damage(target, proj.damage, proj.velocity_x > 0, proj.owner, "Projectile", 0) # Apply damage
                        proj.kill() # Remove projectile on hit

                # --- Game Over Check (Modified for Practice) ---
                if self.current_level != 0: # Only check game over in non-practice levels
                    if self.player and self.opponent and (not self.player.is_alive() or not self.opponent.is_alive()):
                        if not self.player.is_alive():
                            self.winner = "Opponent"
                            self.game_over_message = "YOU LOSE!"
                            self.game_state = STATE_GAME_OVER_LOSE
                        else:
                            self.winner = "Player"
                            self.game_over_message = "YOU WIN!"
                            self.game_state = STATE_GAME_OVER_WIN
                        print(f"Level {self.current_level}: {self.winner} wins!")

                # --- Drawing ---
                if self.current_background:
                    self.screen.blit(self.current_background, (0, 0))
                else:
                    self.screen.fill((0, 0, 0)) # Fallback background
                self.all_sprites.draw(self.screen)
                # Draw health bars
                if self.player: self.draw_health_bar(self.screen, self.player, 10, 10)
                if self.opponent: self.draw_health_bar(self.screen, self.opponent, self.screen_width - 210, 10)


            elif self.game_state == STATE_PAUSED:
                # Draw semi-transparent overlay
                overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                self.screen.blit(overlay, (0, 0))
                # Draw pause menu options
                pause_title = self.title_font.render("Paused", True, (255, 255, 0))
                pause_rect = pause_title.get_rect(center=(self.screen_width // 2, 150))
                self.screen.blit(pause_title, pause_rect)
                for i, option in enumerate(self.pause_options):
                    text_color = (0, 255, 255) if i == self.selected_pause_option else (180, 180, 180)
                    option_text = self.font.render(option, True, text_color)
                    option_rect = option_text.get_rect(center=(self.screen_width // 2, 250 + i * 60))
                    self.screen.blit(option_text, option_rect)
                # Handle pause input
                for event in pygame.event.get([pygame.QUIT, pygame.KEYDOWN]):
                     if event.type == pygame.QUIT: self.running = False; break
                     if event.type == pygame.KEYDOWN:
                          if event.key == pygame.K_ESCAPE: self.game_state = STATE_GAME_RUNNING # Resume
                          elif event.key == pygame.K_UP: self.selected_pause_option = (self.selected_pause_option - 1) % len(self.pause_options)
                          elif event.key == pygame.K_DOWN: self.selected_pause_option = (self.selected_pause_option + 1) % len(self.pause_options)
                          elif event.key == pygame.K_RETURN:
                               if self.selected_pause_option == 0: self.game_state = STATE_GAME_RUNNING # Resume
                               elif self.selected_pause_option == 1: # Quit to Start Menu
                                    self.reset_game_state() # Reset to fighting game start menu

            elif self.game_state == STATE_GAME_OVER_WIN or self.game_state == STATE_GAME_OVER_LOSE:
                self.draw_game_over_screen()
                action = self.handle_game_over_input()
                if action == "QUIT":
                    self.running = False

            # Update the display
            pygame.display.flip()

        print("Exiting Fighting Game run loop.") # Indicate loop exit

    def reset_game_state(self):
        """Resets the game to the initial start menu state."""
        self.game_state = STATE_START_MENU
        self.selected_start_option = 0
        self.selected_level = 0 # Reset level selection too
        self.player = None
        self.opponent = None
        self.all_sprites.empty()
        self.projectiles.empty()
        self.winner = None
        self.current_background = None
        print("Fighting game state reset to start menu.")