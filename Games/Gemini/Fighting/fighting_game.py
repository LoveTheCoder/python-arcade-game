import pygame
import sys
import os
import random
from .character import Character
from .ai_opponent import AIOpponent
from .graphics import Graphics

class FightingGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.clock = clock
        self.graphics = Graphics(self.screen, self.clock)
        self.player = Character("Player", 100, 300)
        self.opponent = AIOpponent("Opponent", 600, 300)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player, self.opponent)
        self.combo_moves = {
            ("punch", "punch", "kick"): {"name": "Fireball", "damage": 30},
            ("kick", "punch"): {"name": "Uppercut", "damage": 25}
        }
        self.floor_level = 400  # Define the floor level
        self.paused = False
        self.start_menu = True
        self.game_running = False
        self.pause_options = ["Resume", "Quit to Start Menu"]
        self.start_menu_options = ["Start Game", "Attack List", "Exit"]
        self.selected_pause_option = 0
        self.selected_start_option = 0
        self.show_attack_list = False
        self.winner = None
        self.basic_attacks = {
            "Q": "Punch",
            "W": "Kick"
        }
        self.running = False  # Add this line

    def reset_game(self):
        self.player = Character("Player", 100, 300)
        self.opponent = AIOpponent("Opponent", 600, 300)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player, self.opponent)
        self.paused = False
        self.game_running = True
        self.winner = None
        self.player.health = 100
        self.opponent.health = 100

    def clear_event_queue(self):
        pygame.event.clear()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Player movement
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if keys[pygame.K_UP]:
            self.player.jump()
        if keys[pygame.K_DOWN]:
            self.player.crouch()
        else:
            self.player.stand()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.dodge()
                if event.key == pygame.K_q:
                    attack_type = self.player.attack("punch")
                    if attack_type:
                        self.handle_attack(self.player, self.opponent, attack_type)
                if event.key == pygame.K_w:
                    attack_type =  self.player.attack("kick")
                    if attack_type:
                        self.handle_attack(self.player, self.opponent, attack_type)
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                    self.selected_pause_option = 0  # Reset selection

    def handle_attack(self, attacker, defender, attack_type):
        now = pygame.time.get_ticks()
        if now - attacker.last_combo_time > attacker.combo_buffer_time:
            attacker.current_combo = []
        attacker.current_combo.append(attack_type)
        attacker.last_combo_time = now
        
        # Check for combos
        combo_key = tuple(attacker.current_combo)
        if combo_key in self.combo_moves:
            combo = self.combo_moves[combo_key]
            print(f"{attacker.name} performs {combo['name']}!")
            self.apply_damage(defender, combo["damage"], attacker.facing_right, attacker)
            attacker.current_combo = []  # Reset combo after successful execution
        else:
            # Apply damage for basic attacks
            self.apply_damage(defender, attacker.attacks[attack_type]["damage"], attacker.facing_right, attacker)

    def apply_damage(self, defender, damage, facing_right, attacker):
        # Check if the defender is dodging
        if defender.is_dodging:
            print(f"{defender.name} dodged the attack!")
            return

        # Calculate the distance between the attacker and defender
        distance = abs(attacker.rect.centerx - defender.rect.centerx)

        # Check if the defender is within the attack range
        if distance <= 50:  # Adjust the attack range as needed
            defender.take_damage(damage)
            print(f"{defender.name} takes {damage} damage!")
        else:
            print(f"{attacker.name}'s attack missed!")

    def draw_pause_menu(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        title_text = self.graphics.font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title_text, title_rect)

        for i, option in enumerate(self.pause_options):
            text_color = (255, 255, 255) if i == self.selected_pause_option else (128, 128, 128)
            option_text = self.graphics.font.render(option, True, text_color)
            option_rect = option_text.get_rect(center=(self.screen_width // 2, 200 + i * 50))
            self.screen.blit(option_text, option_rect)

    def handle_pause_input(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_pause_option = (self.selected_pause_option - 1) % len(self.pause_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_pause_option = (self.selected_pause_option + 1) % len(self.pause_options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_pause_option == 0:  # Resume
                        self.paused = False
                    elif self.selected_pause_option == 1:  # Quit to Start Menu
                        self.paused = False
                        self.start_menu = True
                        self.game_running = False
                        self.reset_game()

    def draw_attack_list(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        title_text = self.graphics.font.render("Attack List", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_text, title_rect)

        y_offset = 150
        # Display basic attacks
        for key, attack in self.basic_attacks.items():
            attack_text = self.graphics.font.render(f"{key}: {attack}", True, (255, 255, 255))
            attack_rect = attack_text.get_rect(center=(self.screen_width // 2, y_offset))
            self.screen.blit(attack_text, attack_rect)
            y_offset += 50

        # Display combo attacks
        for combo, move in self.combo_moves.items():
            combo_string = " + ".join(combo)
            combo_text = self.graphics.font.render(f"{combo_string}: {move['name']}", True, (255, 255, 255))
            combo_rect = combo_text.get_rect(center=(self.screen_width // 2, y_offset))
            self.screen.blit(combo_text, combo_rect)
            y_offset += 50

        back_text = self.graphics.font.render("Press ESC to return", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        self.screen.blit(back_text, back_rect)

    def draw_start_menu(self):
        self.graphics.draw_background((0, 0, 0))
        title_text = self.graphics.font.render("Fighting Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title_text, title_rect)

        for i, option in enumerate(self.start_menu_options):
            text_color = (255, 255, 255) if i == self.selected_start_option else (128, 128, 128)
            option_text = self.graphics.font.render(option, True, text_color)
            option_rect = option_text.get_rect(center=(self.screen_width // 2, 200 + i * 50))
            self.screen.blit(option_text, option_rect)

    def handle_start_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_start_option = (self.selected_start_option - 1) % len(self.start_menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_start_option = (self.selected_start_option + 1) % len(self.start_menu_options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_start_option == 0:  # Start Game
                        self.start_menu = False
                        self.game_running = True
                        self.reset_game()
                    elif self.selected_start_option == 1:  # Attack List
                        self.start_menu = False
                        self.show_attack_list = True
                    elif self.selected_start_option == 2:  # Exit
                        return "MENU"
                elif event.key == pygame.K_ESCAPE:
                    return "MENU"
        return None

    def run(self):
        self.running = True
        while self.running:
            if self.start_menu:
                self.draw_start_menu()
                action = self.handle_start_input()
                if action == "MENU":
                    self.start_menu = False
                    return  # Return to main menu
            elif self.show_attack_list:
                self.draw_attack_list()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.show_attack_list = False
                            self.start_menu = True
            elif self.paused:
                self.handle_pause_input()
                self.draw_pause_menu()
            elif self.game_running:
                self.handle_input()
                opponent_attack = self.opponent.update(self.player)

                if opponent_attack:
                    self.handle_attack(self.opponent, self.player, opponent_attack)

                self.player.update()

                # Drawing
                self.graphics.draw_background((0, 0, 0))
                # Draw the floor
                pygame.draw.line(self.screen, (255, 255, 255), (0, self.floor_level), (self.screen_width, self.floor_level), 3)
                self.graphics.draw_character(self.player, self.player.rect.x, self.player.rect.y)
                self.graphics.draw_character(self.opponent, self.opponent.rect.x, self.opponent.rect.y)

                # Draw health bars
                self.graphics.draw_health_bar(self.screen, self.player, 50, 50)
                self.graphics.draw_health_bar(self.screen, self.opponent, 550, 50)

                # Check for game over
                if not self.player.is_alive() or not self.opponent.is_alive():
                    self.game_running = False
                    self.start_menu = True
                    self.winner = "Opponent" if not self.player.is_alive() else "Player"
                    print(f"{self.winner} wins!")

            self.graphics.update_display()
            self.clock.tick(60)