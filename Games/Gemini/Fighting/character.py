import pygame
import os
import math # Import the standard math module

class Character(pygame.sprite.Sprite):
    def __init__(self, name, x, y, clock, screen_width):
        super().__init__()
        self.name = name
        self.screen_width = screen_width
        self.clock = clock
        self.floor_level = 400

        # --- Sprite Generation ---
        self.sprites = self._generate_sprites(name) # Generate sprites first
        self.image = self.sprites['idle_right'] # Initial image
        self.rect = self.image.get_rect()
        # --- End Sprite Generation ---

        self.rect.centerx = x
        self.rect.bottom = self.floor_level

        # --- Game Attributes ---
        self.health = 100
        self.attack_power = 10
        self.speed = 5
        self.is_jumping = False
        self.is_crouching = False
        self.y_velocity = 0
        self.gravity = 0.5
        self.facing_right = (self.rect.centerx < screen_width / 2)
        self.is_dodging = False
        self.dodge_timer = 0
        self.dodge_duration = 300
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 300 # Base duration for punch/kick anims
        self.current_attack_type = None
        self.attack_cooldown = 500
        self.last_attack_time = -self.attack_cooldown

        # --- Stun Attributes ---
        self.is_stunned = False
        self.stun_timer = 0
        self.stun_duration = 0
        # --- End Stun Attributes ---

        # --- Combo Attributes ---
        self.directional_combo_buffer = []
        self.combo_buffer_time = 500
        self.last_direction_time = 0

        # --- Animation Attributes ---
        self.anim_index = 0

        # --- Attacks and Combos (STANDARDIZED NAMES) ---
        self.attacks = {
            # Basic Attacks
            "punch": {"damage": 10, "range": self.rect.width * 1.2, "anim_frames": 3, "duration": 300},
            "kick": {"damage": 15, "range": self.rect.width * 1.4, "anim_frames": 4, "duration": 400},

            # Combo Attacks
            "Fireball": {"damage": 30, "duration": 400, "type": "projectile"},
            "Throw": {"damage": 20, "range": self.rect.width * 0.8, "duration": 500, "type": "melee"},
            "SpinKick": {"damage": 35, "range": self.rect.width * 1.6, "anim_frames": 4, "duration": 500, "type": "melee"}
        }
        self.combo_moves = {
            (('down', 'right'), 'punch'): {"name": "Fireball"},
            (('left', 'down', 'right'), 'punch'): {"name": "Throw"},
            (('down', 'right'), 'kick'): {"name": "SpinKick"}
        }

        # Set initial image based on facing direction
        self._update_sprite()

    def _add_direction_to_buffer(self, direction):
        """Adds a directional input to the combo buffer."""
        now = pygame.time.get_ticks()
        # Reset buffer if too much time has passed
        if now - self.last_direction_time > self.combo_buffer_time:
            self.directional_combo_buffer = []
        # Add direction (limit buffer size if desired)
        if len(self.directional_combo_buffer) < 6: # Limit buffer length
            self.directional_combo_buffer.append(direction)
        self.last_direction_time = now

    def _generate_sprites(self, name):
        """Generates all stick figure sprite surfaces, including animations."""
        sprites = {}
        base_width, base_height = 40, 70
        crouch_height, jump_height = 50, 65
        line_thickness = 4

        # Colors (same as before)
        if name == "Player": stick_color, head_color, attack_color = (0, 180, 255), (200, 200, 255), (255, 255, 0)
        else: stick_color, head_color, attack_color = (255, 100, 0), (255, 180, 150), (0, 255, 255)

        # Points (same as before)
        head_radius = 10; head_center_x = base_width // 2; head_center_y = head_radius + 2
        torso_top_y = head_center_y + head_radius; torso_bottom_y = base_height - 20; torso_x = head_center_x
        shoulder_y = torso_top_y + 5; hip_y = torso_bottom_y

        # --- Draw Functions ---
        def draw_idle(surface):
            pygame.draw.circle(surface, head_color, (head_center_x, head_center_y), head_radius)
            pygame.draw.line(surface, stick_color, (torso_x, torso_top_y), (torso_x, torso_bottom_y), line_thickness)
            pygame.draw.line(surface, stick_color, (torso_x, shoulder_y), (torso_x - 10, shoulder_y + 30), line_thickness)
            pygame.draw.line(surface, stick_color, (torso_x, shoulder_y), (torso_x + 10, shoulder_y + 30), line_thickness)
            pygame.draw.line(surface, stick_color, (torso_x, hip_y), (torso_x - 8, base_height - 2), line_thickness)
            pygame.draw.line(surface, stick_color, (torso_x, hip_y), (torso_x + 8, base_height - 2), line_thickness)

        def draw_jump(surface):
            pygame.draw.circle(surface, head_color, (head_center_x, head_center_y), head_radius)
            pygame.draw.line(surface, stick_color, (torso_x, torso_top_y), (torso_x, jump_height - 15), line_thickness)
            pygame.draw.line(surface, stick_color, (torso_x, shoulder_y), (torso_x - 15, shoulder_y - 5), line_thickness)
            pygame.draw.line(surface, stick_color, (torso_x, shoulder_y), (torso_x + 15, shoulder_y - 5), line_thickness)
            pygame.draw.line(surface, stick_color, (torso_x, jump_height - 15), (torso_x - 5, jump_height - 2), line_thickness)
            pygame.draw.line(surface, stick_color, (torso_x, jump_height - 15), (torso_x + 5, jump_height - 2), line_thickness)

        def draw_crouch(surface):
            crouch_head_y = head_radius + 10; crouch_torso_bottom = crouch_height - 10
            pygame.draw.circle(surface, head_color, (head_center_x, crouch_head_y), head_radius)
            pygame.draw.line(surface, stick_color, (torso_x, crouch_head_y + head_radius), (torso_x, crouch_torso_bottom), line_thickness)
            pygame.draw.line(surface, stick_color, (torso_x, crouch_head_y + head_radius + 5), (torso_x - 15, crouch_head_y + head_radius + 10), line_thickness)
            pygame.draw.line(surface, stick_color, (torso_x, crouch_head_y + head_radius + 5), (torso_x + 15, crouch_head_y + head_radius + 10), line_thickness)
            pygame.draw.line(surface, stick_color, (torso_x, crouch_torso_bottom), (torso_x - 10, crouch_height - 2), line_thickness)
            pygame.draw.line(surface, stick_color, (torso_x, crouch_torso_bottom), (torso_x + 10, crouch_height - 2), line_thickness)

        def draw_punch_anim(surface, frame):
            draw_idle(surface)
            arm_end_x = torso_x + 5 + frame * 7
            arm_end_y = shoulder_y + 10
            pygame.draw.line(surface, attack_color, (torso_x, shoulder_y), (arm_end_x, arm_end_y), line_thickness + 1)

        def draw_kick_anim(surface, frame):
            draw_idle(surface)
            leg_end_x = torso_x + frame * 6
            leg_end_y = hip_y + 5 + frame * 2
            pygame.draw.line(surface, stick_color, (torso_x, hip_y), (torso_x - 5, base_height - 2), line_thickness)
            pygame.draw.line(surface, attack_color, (torso_x, hip_y), (leg_end_x, leg_end_y), line_thickness + 1)

        def draw_fireball_cast(surface):
            draw_idle(surface)
            pygame.draw.line(surface, attack_color, (torso_x, shoulder_y), (torso_x + 15, shoulder_y + 10), line_thickness)
            pygame.draw.line(surface, attack_color, (torso_x, shoulder_y), (torso_x + 15, shoulder_y + 20), line_thickness)

        def draw_throw_windup(surface):
            draw_idle(surface)
            pygame.draw.line(surface, stick_color, (torso_x, shoulder_y), (torso_x - 15, shoulder_y + 5), line_thickness)
            pygame.draw.line(surface, stick_color, (torso_x, shoulder_y), (torso_x - 15, shoulder_y + 15), line_thickness)

        def draw_throw_execute(surface):
            draw_idle(surface)
            pygame.draw.line(surface, attack_color, (torso_x, shoulder_y), (torso_x + 18, shoulder_y + 10), line_thickness + 1)
            pygame.draw.line(surface, attack_color, (torso_x, shoulder_y), (torso_x + 18, shoulder_y + 20), line_thickness + 1)

        def draw_spinkick_anim(surface, frame):
             draw_idle(surface)
             angle = frame * (math.pi / 4)
             leg_len = 25
             leg_end_x = torso_x + int(leg_len * math.cos(angle))
             leg_end_y = hip_y + int(leg_len * math.sin(angle))
             pygame.draw.line(surface, attack_color, (torso_x, hip_y), (leg_end_x, leg_end_y), line_thickness + 2)

        for state, draw_func, w, h in [('idle', draw_idle, base_width, base_height),
                                       ('jump', draw_jump, base_width, jump_height),
                                       ('crouch', draw_crouch, base_width, crouch_height)]:
            surf = pygame.Surface([w, h], pygame.SRCALPHA)
            draw_func(surf)
            sprites[f'{state}_right'] = surf
            sprites[f'{state}_left'] = pygame.transform.flip(surf, True, False)

        sprites['dodge_right'] = sprites['crouch_right'].copy()
        sprites['dodge_left'] = sprites['crouch_left'].copy()

        for attack_name, draw_func, frames, w, h in [('punch', draw_punch_anim, 3, base_width + 15, base_height),
                                                     ('kick', draw_kick_anim, 4, base_width + 15, base_height + 5),
                                                     ('SpinKick', draw_spinkick_anim, 4, base_width + 20, base_height + 10)]:
             anim_r, anim_l = [], []
             for i in range(frames):
                 surf = pygame.Surface([w, h], pygame.SRCALPHA)
                 draw_func(surf, i)
                 anim_r.append(surf)
                 anim_l.append(pygame.transform.flip(surf, True, False))
             sprites[f'{attack_name}_anim_right'] = anim_r
             sprites[f'{attack_name}_anim_left'] = anim_l

        for state, draw_func, w, h in [('Fireball_cast', draw_fireball_cast, base_width + 10, base_height),
                                       ('Throw_windup', draw_throw_windup, base_width, base_height),
                                       ('Throw_execute', draw_throw_execute, base_width + 15, base_height)]:
             surf = pygame.Surface([w, h], pygame.SRCALPHA)
             draw_func(surf)
             sprites[f'{state}_right'] = surf
             sprites[f'{state}_left'] = pygame.transform.flip(surf, True, False)

        return sprites

    def _update_sprite(self):
        """Sets the correct sprite based on the character's state and animation frame."""
        state = 'idle'
        anim_list = None
        num_frames = 1

        if self.is_stunned:
            state = 'idle'  # Optionally, you can add a specific "stunned" sprite
        elif self.is_jumping: state = 'jump'
        elif self.is_dodging: state = 'dodge'
        elif self.is_crouching: state = 'crouch'
        elif self.is_attacking:
            attack_name = self.current_attack_type
            attack_info = self.attacks.get(attack_name, {})

            if attack_info.get("anim_frames", 0) > 1:
                state = attack_name
                anim_key = f"{state}_anim_{'right' if self.facing_right else 'left'}"
                if anim_key in self.sprites:
                    anim_list = self.sprites[anim_key]
                    num_frames = len(anim_list)
                else:
                    print(f"Warning: Animation missing for {attack_name}, key: {anim_key}")
                    state = 'idle'
            elif attack_name == 'Fireball': state = 'Fireball_cast'
            elif attack_name == 'Throw':
                 progress = (pygame.time.get_ticks() - self.attack_timer) / self.attack_duration if self.attack_duration > 0 else 0
                 state = 'Throw_execute' if progress > 0.4 else 'Throw_windup'
            else: state = 'idle'

        if anim_list:
            frame_index = min(self.anim_index, num_frames - 1)
            new_image = anim_list[frame_index]
        else:
            sprite_key = f"{state}_{'right' if self.facing_right else 'left'}"
            if sprite_key not in self.sprites:
                print(f"Warning: Sprite key '{sprite_key}' not found. Falling back to idle.")
                sprite_key = f"idle_{'right' if self.facing_right else 'left'}"
            new_image = self.sprites[sprite_key]

        if self.image is not new_image:
            current_bottom = self.rect.bottom
            current_centerx = self.rect.centerx
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.bottom = current_bottom
            self.rect.centerx = current_centerx

    def update(self):
        # --- Handle Stun ---
        now = pygame.time.get_ticks()
        if self.is_stunned:
            if now - self.stun_timer > self.stun_duration:
                self.is_stunned = False
                print(f"{self.name} recovered from stun.")
            else:
                # If stunned, skip other updates (gravity, attacks, dodge timer)
                self._update_sprite() # Keep updating sprite maybe for visual effect
                return # Prevent movement/actions while stunned
        # --- End Handle Stun ---

        # Gravity
        if self.is_jumping:
            self.y_velocity += self.gravity
            self.rect.y += self.y_velocity
            if self.rect.bottom >= self.floor_level:
                self.rect.bottom = self.floor_level; self.is_jumping = False; self.y_velocity = 0
        elif self.rect.bottom < self.floor_level: self.rect.bottom = self.floor_level

        # Dodge Timer
        if self.is_dodging and now - self.dodge_timer > self.dodge_duration: self.is_dodging = False

        # Attacking State & Animation Update
        if self.is_attacking:
            if now - self.attack_timer > self.attack_duration:
                self.is_attacking = False
                self.current_attack_type = None
                self.anim_index = 0
            else:
                attack_info = self.attacks.get(self.current_attack_type, {})
                num_frames = attack_info.get("anim_frames", 1)
                if num_frames > 1 and self.attack_duration > 0:
                    frame_time = self.attack_duration / num_frames
                    self.anim_index = int((now - self.attack_timer) / frame_time)
                    self.anim_index = min(self.anim_index, num_frames - 1)

        # Update sprite based on state
        self._update_sprite()

    def stun(self, duration_ms):
        """Applies stun effect to the character."""
        if not self.is_stunned: # Don't re-stun if already stunned
            self.is_stunned = True
            self.stun_timer = pygame.time.get_ticks()
            self.stun_duration = duration_ms
            # Cancel current actions
            self.is_attacking = False
            self.is_dodging = False
            self.is_jumping = False
            # Optionally reset animation
            self.anim_index = 0
            print(f"{self.name} is stunned for {duration_ms}ms!")

    def move_left(self):
        # Handles actual movement, NO buffer call here
        if not self.is_stunned and not self.is_dodging and not self.is_attacking and not self.is_crouching:
            self.rect.x -= self.speed
            if self.rect.left < 0: self.rect.left = 0
            self.facing_right = False

    def move_right(self):
        # Handles actual movement, NO buffer call here
        if not self.is_stunned and not self.is_dodging and not self.is_attacking and not self.is_crouching:
            self.rect.x += self.speed
            if self.rect.right > self.screen_width: self.rect.right = self.screen_width
            self.facing_right = True

    def jump(self):
        # Handles jump state, NO buffer call here
        if not self.is_stunned and not self.is_jumping and not self.is_dodging and not self.is_attacking and not self.is_crouching:
            self.is_jumping = True
            self.y_velocity = -12

    def crouch(self):
        # Handles crouch state, NO buffer call here
        if not self.is_stunned and not self.is_jumping and not self.is_dodging and not self.is_attacking:
            self.is_crouching = True

    def stand(self):
        self.is_crouching = False

    def dodge(self):
        now = pygame.time.get_ticks()
        if not self.is_stunned and not self.is_dodging and not self.is_jumping and not self.is_attacking:
            self.is_dodging = True
            self.dodge_timer = now

    def attack(self, attack_type):
        now = pygame.time.get_ticks()
        if not self.is_stunned and \
           now - self.last_attack_time > self.attack_cooldown and \
           not self.is_attacking and not self.is_dodging and \
           not self.is_crouching and not self.is_jumping:

            performed_attack_type = attack_type
            is_combo = False

            if self.directional_combo_buffer and \
               (now - self.last_direction_time <= self.combo_buffer_time):

                combo_key_tuple = tuple(self.directional_combo_buffer)
                full_combo_key = (combo_key_tuple, attack_type)

                if full_combo_key in self.combo_moves:
                    combo_info = self.combo_moves[full_combo_key]
                    performed_attack_type = combo_info['name']
                    is_combo = True
                    print(f"{self.name} performs COMBO: {performed_attack_type}")

            if not is_combo:
                 print(f"{self.name} attacks: {performed_attack_type}")

            self.is_attacking = True
            self.attack_timer = now
            self.last_attack_time = now
            self.current_attack_type = performed_attack_type
            self.anim_index = 0

            attack_info = self.attacks.get(performed_attack_type, self.attacks.get(attack_type))
            self.attack_duration = attack_info.get("duration", 300)

            self.directional_combo_buffer = []
            self.last_direction_time = 0

            return performed_attack_type

        elif self.is_stunned:
             print(f"{self.name} cannot attack while stunned.") # Debug print
             return None

        return None

    def take_damage(self, damage):
        if not self.is_dodging:
            effective_damage = damage * 0.25 if self.is_crouching else damage
            self.health -= effective_damage
            if self.health < 0: self.health = 0
            print(f"{self.name} health: {self.health}")

    def is_alive(self):
        return self.health > 0