import pygame
import random
from .character import Character

class AIOpponent(Character):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.image.fill((255, 0, 0))  # Red for opponent
        self.attack_range = 50
        self.decision_interval = 2000  # milliseconds
        self.last_decision_time = 0

    def choose_action(self, player):
        now = pygame.time.get_ticks()
        if now - self.last_decision_time > self.decision_interval:
            self.last_decision_time = now
            distance = abs(self.rect.x - player.rect.x)

            if distance < self.attack_range and not self.is_attacking:
                # 50% chance to punch or kick
                if random.random() < 0.5:
                    return self.attack("punch")
                else:
                    return self.attack("kick")
            elif distance > self.attack_range and self.rect.x < player.rect.x:
                return "move_right"
            elif distance > self.attack_range and self.rect.x > player.rect.x:
                return "move_left"
            else:
                # 20% chance to jump, otherwise do nothing
                if random.random() < 0.2:
                    return "jump"
                else:
                    return None  # Do nothing

    def update(self, player):
        super().update()
        action = self.choose_action(player)

        if action == "move_right":
            self.move_right()
        elif action == "move_left":
            self.move_left()
        elif action == "jump":
            self.jump()
        elif action == "punch":
            return self.attack("punch")
        elif action == "kick":
            return self.attack("kick")