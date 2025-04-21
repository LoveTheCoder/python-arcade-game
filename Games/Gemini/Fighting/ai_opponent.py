import pygame
import random
from .character import Character

# Define AI States
STATE_IDLE = 0
STATE_ATTACKING = 1
STATE_BLOCKING = 2
STATE_DODGING = 3
STATE_MOVING = 4

class AIOpponent(Character):
    def __init__(self, name, x, y, clock, screen_width, level=1):
        super().__init__(name, x, y, clock, screen_width)
        self.level = level
        self.can_take_damage = True # Default

        if level == 0: # Practice Dummy Setup
            self.decision_interval = 99999 # Very long interval
            self.movement_decision_interval = 99999
            self.dodge_chance = 0.0
            self.block_chance = 0.0
            self.combo_chance = 0.0
            self.jump_chance = 0.0
            self.optimal_distance = 50 # Doesn't matter much
            self.attack_frequency = 0.0 # Never attack
            self.health = 99999 # Set high health here too
            self.can_take_damage = False # Explicitly set flag
        else: # Normal AI Setup
            # --- AI Parameters Scaled by Level ---
            base_decision_interval = 450 # Slightly slower base decisions
            base_movement_interval = 250 # Slightly slower base movement decisions
            base_block_chance = 0.05 # Start low
            base_combo_chance = 0.15 # *** INCREASED base chance slightly ***
            base_jump_chance = 0.01
            base_optimal_distance = 55 # Start slightly further away
            base_attack_frequency = 0.4 # Base probability to attack when in range/state

            level_factor = 1 + (level - 1) * 0.15

            self.decision_interval = max(50, int(base_decision_interval / level_factor))
            self.movement_decision_interval = max(30, int(base_movement_interval / level_factor))

            # --- New Dodge Chance Calculation ---
            if level == 1:
                self.dodge_chance = 0.0
            else:
                # Increase dodge chance by 2% for each level above 1
                dodge_increase_per_level = 0.02
                self.dodge_chance = min(0.4, dodge_increase_per_level * (level - 1)) # Cap at 40%
            # --- End New Dodge Chance Calculation ---

            self.block_chance = min(0.5, base_block_chance * level_factor)
            self.combo_chance = min(0.7, base_combo_chance * level_factor) # Cap at 70%
            self.jump_chance = min(0.15, base_jump_chance * level_factor)
            self.optimal_distance = max(30, int(base_optimal_distance / (1 + (level-1)*0.05)))
            # Attack frequency increases with level
            self.attack_frequency = min(0.95, base_attack_frequency + (level - 1) * 0.06)

            # Ensure can_take_damage remains True for normal levels
            self.can_take_damage = True

        # --- Fixed Parameters ---
        self.attack_range = 70
        self.safe_distance = 150
        self.flee_health_threshold = 30

        # --- State Variables ---
        self.last_decision_time = 0
        self.current_state = STATE_IDLE
        self.state_timer = 0
        self.state_duration = 0
        self.target_x = self.rect.centerx
        self.last_movement_decision = 0
        self._desired_state = STATE_IDLE

        print(f"AI Level {self.level}: Dodge Chance={self.dodge_chance:.2f}, Combo Chance={self.combo_chance:.2f}, Attack Freq={self.attack_frequency:.2f}") # Updated Debug Print

    def decide_action_state(self, player):
        """Decides the AI's *action* state (attack, block, dodge, idle)."""
        now = pygame.time.get_ticks()
        distance = abs(self.rect.centerx - player.rect.centerx)
        time_in_current_state = self.state_timer

        # --- High-Priority Interrupts ---
        if random.random() < self.dodge_chance and not self.is_dodging and self.current_state != STATE_DODGING:
            self.current_state = STATE_DODGING
            self.state_duration = self.dodge_duration
            self.state_timer = 0
            return

        if random.random() < self.block_chance and not self.is_crouching and self.current_state != STATE_BLOCKING:
            self.current_state = STATE_BLOCKING
            self.state_duration = random.randint(300, 800)
            self.state_timer = 0
            return

        # --- Re-evaluate Action State periodically or if current action finished ---
        time_to_reconsider = (time_in_current_state >= self.state_duration and self.state_duration > 0) or \
                             (now - self.last_decision_time > self.decision_interval)

        if time_to_reconsider:
            self.last_decision_time = now
            desired_state = STATE_IDLE # Default

            if distance < self.optimal_distance:
                desired_state = STATE_ATTACKING
            # Add other conditions if needed (e.g., specific counter-attack states)

            # Change state if needed (and not currently dodging/blocking unless finished)
            if desired_state != self.current_state:
                 if self.current_state not in [STATE_DODGING, STATE_BLOCKING] or time_in_current_state >= self.state_duration:
                    self.current_state = desired_state
                    self.state_timer = 0

                    # Set typical duration for action states
                    if self.current_state == STATE_ATTACKING:
                        self.state_duration = random.randint(400, 1200)
                    else: # IDLE
                        self.state_duration = random.randint(50, 200)

        # --- Update Timer ---
        self.state_timer += self.clock.get_time()

    def decide_movement_target(self, player):
        """Decides the AI's target X position."""
        now = pygame.time.get_ticks()
        if now - self.last_movement_decision > self.movement_decision_interval:
            self.last_movement_decision = now
            distance = self.rect.centerx - player.rect.centerx
            health_percentage = (self.health / 100) * 100

            if health_percentage <= self.flee_health_threshold:
                # Flee: Target a point safe_distance away
                target_offset = self.safe_distance
            else:
                # Approach/Maintain: Target a point optimal_distance away
                target_offset = self.optimal_distance

            # Aim to be offset distance away from the player
            if distance > 0: # AI is to the right of player
                self.target_x = player.rect.centerx + target_offset
            else: # AI is to the left of player
                self.target_x = player.rect.centerx - target_offset

            # Clamp target_x within screen bounds, considering character width
            half_width = self.rect.width // 2
            self.target_x = max(half_width, min(self.screen_width - half_width, self.target_x))

    def update(self, player):
        # 1. Base character updates
        super().update()

        # 2. Decide target position
        self.decide_movement_target(player)

        # 3. Decide action state (Important: This happens BEFORE attack execution)
        self.decide_action_state(player)

        # 4. Execute continuous movement towards target_x
        move_threshold = self.speed
        can_move = not (self.is_attacking or self.is_dodging or self.current_state == STATE_BLOCKING)
        if can_move:
            if self.rect.centerx < self.target_x - move_threshold:
                self.move_right()
            elif self.rect.centerx > self.target_x + move_threshold:
                self.move_left()

        # 5. Execute actions based on state
        action_performed_name = None
        if self.current_state == STATE_ATTACKING:
            self.facing_right = (player.rect.centerx > self.rect.centerx)

            if not self.is_attacking and \
               (pygame.time.get_ticks() - self.last_attack_time > self.attack_cooldown) and \
               (random.random() < self.attack_frequency):

                 distance = abs(self.rect.centerx - player.rect.centerx)
                 melee_range = max(self.attacks.get("punch", {}).get("range", 50),
                                   self.attacks.get("kick", {}).get("range", 60))
                 can_try_melee = distance < melee_range

                 # --- Try Directional Combos First ---
                 if random.random() < self.combo_chance:
                     print(f"AI rolled {self.combo_chance*100:.1f}% chance and is TRYING to combo...")
                     possible_combos = []

                     # --- CORRECTED KEY STRUCTURE & MODIFIED FIREBALL CHECK ---
                     # Check Fireball combo - REMOVED range check
                     fireball_dir_key = ('down', 'right')
                     fireball_trigger = 'punch'
                     fireball_check_key = (fireball_dir_key, fireball_trigger)
                     # Allow Fireball attempt regardless of distance if the combo exists
                     if fireball_check_key in self.combo_moves:
                         print(f"  - Fireball possible (No range check)") # Updated debug print
                         possible_combos.append(self.combo_moves[fireball_check_key]['name'])

                     # Check Throw combo (Still requires melee range)
                     throw_dir_key = ('left', 'down', 'right')
                     throw_trigger = 'punch'
                     throw_check_key = (throw_dir_key, throw_trigger)
                     if can_try_melee and throw_check_key in self.combo_moves:
                         print(f"  - Throw possible (Range OK: {can_try_melee})")
                         possible_combos.append(self.combo_moves[throw_check_key]['name'])

                     # Check SpinKick combo (Still requires melee range)
                     spinkick_dir_key = ('down', 'right')
                     spinkick_trigger = 'kick'
                     spinkick_check_key = (spinkick_dir_key, spinkick_trigger)
                     if can_try_melee and spinkick_check_key in self.combo_moves:
                         print(f"  - SpinKick possible (Range OK: {can_try_melee})")
                         possible_combos.append(self.combo_moves[spinkick_check_key]['name'])
                     # --- END MODIFIED CHECKS ---

                     if possible_combos:
                         chosen_combo_name = random.choice(possible_combos)
                         # --- Directly initiate the combo state ---
                         self.is_attacking = True
                         self.attack_timer = pygame.time.get_ticks()
                         self.last_attack_time = self.attack_timer
                         self.current_attack_type = chosen_combo_name
                         self.anim_index = 0
                         attack_info = self.attacks.get(chosen_combo_name, {})
                         self.attack_duration = attack_info.get("duration", 300)
                         action_performed_name = chosen_combo_name
                         print(f"AI decided COMBO: {action_performed_name}")
                     else:
                         print("AI combo attempt failed: No valid combos available/in range.")

                 # --- If no combo performed, try basic attack ---
                 if not action_performed_name and can_try_melee:
                     basic_attack_type = random.choice(["punch", "kick"])
                     self.directional_combo_buffer = [] # Ensure buffer clear
                     action_performed_name = self.attack(basic_attack_type)
                     if action_performed_name:
                         print(f"AI decided BASIC: {action_performed_name}")

            # If AI is in attacking state but didn't attack (e.g., cooldown), ensure it stands
            if not self.is_attacking:
                self.stand()

        # Handle other states
        elif self.current_state == STATE_BLOCKING: self.crouch()
        elif self.current_state == STATE_DODGING: self.dodge()
        elif self.current_state == STATE_IDLE: self.stand()

        # Ensure sprite updates based on final state
        self._update_sprite()

        return action_performed_name # Return name of move performed (or None)
