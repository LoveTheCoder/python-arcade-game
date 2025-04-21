import pygame
import sys
import os
import random
import subprocess

# Removed update_game_from_github and configure_wifi functions

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
        self.options = ["Bullet Hell", "Rhythm Game", "Fighting Game"]
        self.selected = 0
        
        # Font
        self.font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 32)
        
        # Game states
        self.running = True
        self.in_menu = True
        self.clock = clock

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected]
                elif event.key == pygame.K_ESCAPE:
                    return "MENU"
        return None

    def run(self):
        bullet_hell_game = BulletHellGame()  # if these work correctly
        while self.running:
            if self.in_menu:
                self.draw_menu()
                action = self.handle_input()
                if action == "Bullet Hell":
                    self.in_menu = False
                    bullet_hell_game.run()
                    self.in_menu = True
                elif action == "Rhythm Game":
                    self.in_menu = False
                    rhythm_game_main()
                    self.in_menu = True
                elif action == "Fighting Game":
                    self.in_menu = False
                    # Create a new instance so that internal state is fresh
                    fighting_game = FightingGame(self.screen, self.clock)
                    fighting_game.run()
                    self.in_menu = True
                elif action == "Exit" or action == "QUIT":
                    self.running = False
                self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 480))
    clock = pygame.time.Clock()
    menu = GameMenu(screen, clock)
    menu.run()