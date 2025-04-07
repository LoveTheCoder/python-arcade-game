import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.image = pygame.Surface([50, 50])
        self.image.fill((255, 255, 255))  # Default white color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 100
        self.attack_power = 10
        self.speed = 5
        self.is_jumping = False
        self.is_crouching = False
        self.y_velocity = 0
        self.gravity = 0.5
        self.facing_right = True  # Track facing direction
        self.is_dodging = False
        self.dodge_timer = 0
        self.dodge_duration = 300  # milliseconds
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 200 # milliseconds
        self.current_combo = []
        self.combo_buffer_time = 1000 # milliseconds
        self.last_combo_time = 0
        self.attacks = {
            "punch": {"damage": 10, "range": 30},
            "kick": {"damage": 15, "range": 40}
        }
        self.floor_level = 400  # Define the floor level

    def update(self):
        # Gravity
        if self.is_jumping:
            self.y_velocity += self.gravity
            self.rect.y += self.y_velocity
            if self.rect.bottom >= self.floor_level:  # Ground level
                self.rect.bottom = self.floor_level
                self.is_jumping = False
                self.y_velocity = 0
        else:
            # Keep the character on the floor if not jumping
            if self.rect.bottom < self.floor_level:
                self.rect.bottom = self.floor_level

        # Dodge timer
        if self.is_dodging:
            if pygame.time.get_ticks() - self.dodge_timer > self.dodge_duration:
                self.is_dodging = False

        # Attack timer
        if self.is_attacking:
            if pygame.time.get_ticks() - self.attack_timer > self.attack_duration:
                self.is_attacking = False

    def move_left(self):
        if not self.is_dodging and not self.is_attacking:
            self.rect.x -= self.speed
            self.facing_right = False

    def move_right(self):
        if not self.is_dodging and not self.is_attacking:
            self.rect.x += self.speed
            self.facing_right = True

    def jump(self):
        if not self.is_jumping and not self.is_crouching and not self.is_dodging and not self.is_attacking:
            self.is_jumping = True
            self.y_velocity = -15

    def crouch(self):
        if not self.is_jumping and not self.is_dodging and not self.is_attacking:
            self.is_crouching = True

    def stand(self):
        self.is_crouching = False

    def dodge(self):
        if not self.is_dodging and not self.is_crouching and not self.is_jumping and not self.is_attacking:
            self.is_dodging = True
            self.dodge_timer = pygame.time.get_ticks()

    def attack(self, attack_type):
        if not self.is_attacking and not self.is_dodging and not self.is_crouching and not self.is_jumping:
            self.is_attacking = True
            self.attack_timer = pygame.time.get_ticks()
            return attack_type # Return the attack type

    def take_damage(self, damage):
        if not self.is_dodging:
            self.health -= damage
            if self.health < 0:
                self.health = 0

    def is_alive(self):
        return self.health > 0

class PlayerCharacter:
    def __init__(self, name, health, position):
        self.name = name
        self.health = health
        self.position = position
        self.attack_power = 10
        self.special_move_power = 25

    def move(self, direction):
        if direction == "left":
            self.position[0] -= 5
        elif direction == "right":
            self.position[0] += 5
        elif direction == "up":
            self.position[1] -= 5
        elif direction == "down":
            self.position[1] += 5

    def attack(self):
        return self.attack_power

    def special_move(self):
        return self.special_move_power

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def get_position(self):
        return self.position

    def get_health(self):
        return self.health

    def reset(self):
        self.health = 100
        self.position = [0, 0]  # Reset to starting position