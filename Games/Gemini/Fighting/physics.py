import pygame

class Physics:
    def __init__(self):
        self.gravity = 0.5
        self.friction = 0.1

    def apply_gravity(self, character):
        if character.y_velocity < 10:  # Limit falling speed
            character.y_velocity += self.gravity

    def apply_friction(self, character):
        if character.on_ground:
            character.x_velocity *= (1 - self.friction)

    def check_collision(self, character1, character2):
        if (character1.rect.colliderect(character2.rect)):
            self.resolve_collision(character1, character2)

    def resolve_collision(self, character1, character2):
        # Simple collision resolution
        if character1.rect.bottom > character2.rect.top:
            character1.rect.bottom = character2.rect.top
            character1.y_velocity = 0
            character1.on_ground = True
        elif character1.rect.top < character2.rect.bottom:
            character1.rect.top = character2.rect.bottom
            character1.y_velocity = 0
        if character1.rect.right > character2.rect.left and character1.rect.left < character2.rect.left:
            character1.rect.right = character2.rect.left
        elif character1.rect.left < character2.rect.right and character1.rect.right > character2.rect.right:
            character1.rect.left = character2.rect.right

    def update(self, character):
        character.rect.x += character.x_velocity
        character.rect.y += character.y_velocity
        self.apply_gravity(character)
        self.apply_friction(character)