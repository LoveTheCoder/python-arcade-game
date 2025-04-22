import pygame
import sys
import os
import random
import subprocess
from signal import pause  # For handling GPIO events
import atexit  # Ensure cleanup on exit
from gpiozero import Button, GPIOZeroError  # Import Button and Error class

# Get the absolute path to the Games directory
GAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Games')

# Add paths to Python path
sys.path.append(os.path.join(GAMES_DIR, 'GPT_o1'))
sys.path.append(os.path.join(GAMES_DIR, 'Claude'))
sys.path.append(os.path.join(GAMES_DIR, 'Gemini', 'Fighting'))  # Corrected path

# Import the games
from Games.GPT_o1.Bullethell import BulletHellGame
from Games.Claude.rythmgame import main as rhythm_game_main
from Games.Gemini.Fighting.fighting_game import FightingGame

class GameMenu:
    def __init__(self, screen, clock):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 480
        self.screen = screen
        pygame.display.set_caption("Game Menu")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.SELECTED_COLOR = (0, 255, 0)
        
        # Menu options
        self.options = ["Bullet Hell", "Rhythm Game", "Fighting Game"]  # Added Exit
        self.selected = 0
        
        # Font
        self.font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 32)
        
        # Game states
        self.running = True
        self.in_menu = True
        self.clock = clock
        
        # GPIO Buttons for Menu
        self.gpio_buttons = None
        self.initialize_gpio()  # Initialize GPIO for the menu

    def initialize_gpio(self):
        """Initializes GPIO buttons for the menu."""
        if self.gpio_buttons is None:  # Only initialize if not already done
            try:
                self.gpio_buttons = {
                    "button_up": Button(4),
                    "button_down": Button(2),
                    "button_left": Button(3),  # Use left for back/exit confirmation
                    "button_right": Button(5)  # Use right for select
                }
                print("Menu GPIO initialized.")
            except GPIOZeroError as e:
                print(f"Menu GPIO Error: {e}. Check permissions/pins. Using keyboard fallback.")
                self.gpio_buttons = None  # Ensure it's None if failed
            except Exception as e:
                print(f"Unexpected error initializing menu GPIO: {e}. Using keyboard fallback.")
                self.gpio_buttons = None  # Ensure it's None if failed

    def cleanup_gpio(self):
        """Cleans up GPIO buttons used by the menu."""
        if self.gpio_buttons:
            try:
                print("Cleaning up menu GPIO...")
                self.gpio_buttons["button_up"].close()
                self.gpio_buttons["button_down"].close()
                self.gpio_buttons["button_left"].close()
                self.gpio_buttons["button_right"].close()
                print("Menu GPIO cleaned up.")
            except Exception as e:
                print(f"Error cleaning up menu GPIO: {e}")
        self.gpio_buttons = None  # Set to None after cleanup attempt

    def draw_background(self):
        # Retro styled background: vertical gradient only.
        for y in range(self.SCREEN_HEIGHT):
            # Gradient from dark purple to navy-blue for retro feel
            r = 40
            g = max(0, 20 - y // 30)
            b = min(150 + y // 2, 255)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.SCREEN_WIDTH, y))

    def draw_option_graphic(self, option, rect):
        if option == "Bullet Hell":
            # Space themed graphic filling the entire rectangle.
            for y in range(rect.top, rect.bottom):
                intensity = 20 + int(35 * ((y - rect.top) / rect.height))
                pygame.draw.line(self.screen, (10, 10, intensity), (rect.left, y), (rect.right, y))
            planet_center = (rect.centerx, rect.centery)
            planet_radius = min(rect.width, rect.height) // 3
            pygame.draw.circle(self.screen, (100, 50, 150), planet_center, planet_radius)
            pygame.draw.circle(self.screen, (0, 255, 255), planet_center, planet_radius, 3)
        
        elif option == "Rhythm Game":
            # Vaporwave themed graphic filling the rectangle.
            self.screen.fill((20, 0, 40), rect)
            num_lines = 6
            for i in range(1, num_lines):
                y = rect.top + i * rect.height // num_lines
                pygame.draw.line(self.screen, (255, 105, 180), (rect.left, y), (rect.right, y), 2)
                x = rect.left + i * rect.width // num_lines
                pygame.draw.line(self.screen, (255, 105, 180), (x, rect.top), (x, rect.bottom), 2)
            sun_center = (rect.centerx, rect.bottom - rect.height//4)
            sun_radius = min(rect.width, rect.height) // 5
            pygame.draw.circle(self.screen, (255, 100, 100), sun_center, sun_radius)
            pygame.draw.circle(self.screen, (255, 255, 0), sun_center, sun_radius, 3)

        elif option == "Fighting Game":
            # Fighting game themed graphic filling the rectangle.
            self.screen.fill((50, 50, 50), rect)
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 5, border_radius=10)
            text = self.small_font.render("Fighting Game", True, self.WHITE)
            text_rect = text.get_rect(center=(rect.centerx, rect.centery))
            self.screen.blit(text, text_rect)

    def draw_menu(self):
        self.draw_background()
        
        # Draw title with neon effect.
        title_text = self.font.render("Game Selection", True, (0, 255, 255))
        glow = self.font.render("Game Selection", True, (255, 20, 147))
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH/2, 80))
        self.screen.blit(glow, (title_rect.x+2, title_rect.y+2))
        self.screen.blit(title_text, title_rect)
        
        # Draw options with their graphic.
        for i, option in enumerate(self.options):
            rect = pygame.Rect(0, 0, 300, 80)
            rect.center = (self.SCREEN_WIDTH//2, 200 + i * 100)
            fill_color = (50, 50, 50) if i != self.selected else (80, 80, 80)
            pygame.draw.rect(self.screen, fill_color, rect, border_radius=10)
            border_color = self.SELECTED_COLOR if i == self.selected else self.WHITE
            pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=10)
            self.draw_option_graphic(option, rect)
            text = self.small_font.render(option, True, border_color)
            text_rect = text.get_rect(center=(rect.centerx, rect.centery))
            self.screen.blit(text, text_rect)

        # Draw instructions for game selection.
        instructions = self.small_font.render("Press UP/DOWN to select, ENTER to start", True, self.WHITE)
        instr_rect = instructions.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT - 30))
        self.screen.blit(instructions, instr_rect)
                
        pygame.display.flip()

    def handle_input(self):
        """Handles input for the menu, checking if GPIO is available."""
        # Check GPIO first if available
        if self.gpio_buttons:
            # Check GPIO button states for navigation
            if self.gpio_buttons["button_up"].is_pressed:
                self.selected = (self.selected - 1) % len(self.options)
                pygame.time.wait(200)  # Debounce delay
            elif self.gpio_buttons["button_down"].is_pressed:
                self.selected = (self.selected + 1) % len(self.options)
                pygame.time.wait(200)  # Debounce delay
            elif self.gpio_buttons["button_right"].is_pressed:  # Right selects
                pygame.time.wait(200)  # Debounce
                return self.options[self.selected]
            elif self.gpio_buttons["button_left"].is_pressed:  # Left goes back/exits menu
                pygame.time.wait(200)  # Debounce
                return "Exit"  # Example: Left exits the whole app from menu

        # Always check for Pygame events (QUIT, Keyboard fallback)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Exit"
            # Keyboard fallback only if GPIO failed or for testing
            if not self.gpio_buttons and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected]
                elif event.key == pygame.K_ESCAPE:
                    return "Exit"  # Allow Esc to exit

        return None  # No action selected this frame

    def run(self):
        try:  # Wrap run in try...finally for cleanup
            while self.running:
                if self.in_menu:
                    # Ensure GPIO is initialized for the menu state
                    if not self.gpio_buttons:
                        self.initialize_gpio()

                    self.draw_menu()
                    action = self.handle_input()

                    selected_game_action = None
                    if action in ["Bullet Hell", "Rhythm Game", "Fighting Game"]:
                        selected_game_action = action
                    elif action == "Exit":
                        self.running = False
                        break  # Exit the main loop

                    if selected_game_action:
                        print(f"Selected {selected_game_action}")
                        self.cleanup_gpio()  # Release menu GPIO before starting game
                        self.in_menu = False

                        try:
                            if selected_game_action == "Bullet Hell":
                                print("Starting Bullet Hell...")
                                bullet_hell_game = BulletHellGame()
                                bullet_hell_game.run()
                                print("Bullet Hell finished.")
                            elif selected_game_action == "Rhythm Game":
                                print("Starting Rhythm Game...")
                                rhythm_game_main()
                                print("Rhythm Game finished.")
                            elif selected_game_action == "Fighting Game":
                                print("Starting Fighting Game...")
                                fighting_game = FightingGame(self.screen, self.clock)
                                fighting_game.run()
                                print("Fighting Game finished.")
                        except Exception as e:
                            print(f"Error running game {selected_game_action}: {e}")
                        finally:
                            # Ensure menu state is restored even if game crashes
                            self.in_menu = True
                            # GPIO will be re-initialized at the start of the menu loop iteration
                            print("Returned to menu.")

                self.clock.tick(60)
        finally:  # Ensure cleanup happens when run() exits
            print("Exiting application run loop...")
            self.cleanup_gpio()  # Clean up menu GPIO specifically
            pygame.quit()  # Quit Pygame

if __name__ == "__main__":
    pygame.init()
    # Set SDL video driver if needed
    # import os
    # os.environ["SDL_VIDEODRIVER"] = "kmsdrm"  # or "x11"
    screen = None  # Initialize screen to None
    try:
        screen = pygame.display.set_mode((800, 480))
        clock = pygame.time.Clock()
        menu = GameMenu(screen, clock)
        menu.run()  # run() now handles pygame.quit() in its finally block
    except pygame.error as e:
        print(f"Pygame error: {e}")
        print("Ensure display environment is set up correctly.")
    except Exception as e:
        print(f"An unexpected error occurred in main: {e}")
    finally:
        # Ensure pygame quits even if GameMenu creation failed
        if pygame.get_init():
            pygame.quit()
        print("Application finished.")
        sys.exit()