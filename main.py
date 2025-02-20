import pygame
import sys
import os

# Get the absolute path to the Games directory
GAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Games')

# Add paths to Python path
sys.path.append(os.path.join(GAMES_DIR, 'GPT_o1'))
sys.path.append(os.path.join(GAMES_DIR, 'Claude'))

# Import the games
from Games.GPT_o1.Bullethell import BulletHellGame
from Games.Claude.rythmgame import main as rhythm_game_main

class GameMenu:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Game Menu")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.SELECTED_COLOR = (0, 255, 0)
        
        # Menu options
        self.options = ["Bullet Hell", "Rhythm Game", "Exit"]
        self.selected = 0
        
        # Font
        self.font = pygame.font.Font(None, 64)
        
        # Game states
        self.running = True
        self.in_menu = True

    def draw_menu(self):
        self.screen.fill(self.BLACK)
        
        # Draw title
        title = self.font.render("Game Selection", True, self.WHITE)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH/2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw options
        for i, option in enumerate(self.options):
            color = self.SELECTED_COLOR if i == self.selected else self.WHITE
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.SCREEN_WIDTH/2, 250 + i * 100))
            self.screen.blit(text, rect)
        
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
        clock = pygame.time.Clock()
        
        while self.running:
            if self.in_menu:
                self.draw_menu()
                action = self.handle_input()
                
                if action == "Bullet Hell":
                    self.in_menu = False
                    pygame.display.set_mode((800, 480))  # Set correct resolution for Bullet Hell
                    game = BulletHellGame()
                    game.run()
                    # Reinitialize display for menu
                    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
                    self.in_menu = True
                    
                elif action == "Rhythm Game":
                    self.in_menu = False
                    pygame.display.set_mode((400, 800))  # Set correct resolution for Rhythm Game
                    rhythm_game_main()
                    # Reinitialize display for menu
                    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
                    self.in_menu = True
                    
                elif action == "Exit" or action == "QUIT":
                    self.running = False
            
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    menu = GameMenu()
    menu.run()