import pygame
import sys
import os

# Import the games
from Games.GPT_o1.Bullethell import BulletHellGame
from Games.Claude.rythmgame import RhythmGame

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
        self.RED = (255, 0, 0)

        # Font
        self.font = pygame.font.Font(None, 48)
        
        # Menu options
        self.options = ["Rhythm Game", "Bullet Hell", "Exit"]
        self.selected = 0
        
        # Game states
        self.running = True

    def draw_menu(self):
        self.screen.fill(self.BLACK)
        
        # Draw title
        title = self.font.render("Game Selection", True, self.WHITE)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw options
        for i, option in enumerate(self.options):
            color = self.RED if i == self.selected else self.WHITE
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, 250 + i * 70))
            self.screen.blit(text, rect)
        
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()

    def select_option(self):
        if self.options[self.selected] == "Rhythm Game":
            game = RhythmGame()
            game.run()
        elif self.options[self.selected] == "Bullet Hell":
            game = BulletHellGame()
            game.run()
        elif self.options[self.selected] == "Exit":
            self.running = False

    def run(self):
        while self.running:
            self.handle_input()
            self.draw_menu()
            pygame.time.Clock().tick(60)
        pygame.quit()

if __name__ == "__main__":
    menu = GameMenu()
    menu.run()