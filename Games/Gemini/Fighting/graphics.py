import pygame

class Graphics:
    def __init__(self, screen, clock):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.clock = clock
        self.font = pygame.font.Font(None, 32)

    def load_image(self, path):
        return pygame.image.load(path).convert_alpha()

    def draw_background(self, color):
        self.screen.fill(color)

    def draw_character(self, character, x, y):
        self.screen.blit(character.image, (x, y))

    def draw_health_bar(self, screen, character, x, y):
        health_percentage = character.health / 100
        bar_width = 200
        bar_height = 20
        fill_width = int(bar_width * health_percentage)
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill_width, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), outline_rect, 2)  # Red outline
        pygame.draw.rect(screen, (0, 255, 0), fill_rect)  # Green fill
        health_text = self.font.render(f"{character.name}: {character.health}", True, (255, 255, 255))
        screen.blit(health_text, (x, y - 30))

    def update_display(self):
        pygame.display.flip()
        self.clock.tick(60)