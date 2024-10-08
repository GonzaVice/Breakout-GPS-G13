import pygame
import random
from settings import BRICK_IMAGES, POWERUP_IMAGES, AVAILABLE_POWERUPS, POWERUP_PROBABILITY

class Brick:
    def __init__(self, x, y, hit_points=1, is_powerup_brick=False, powerup_chance=POWERUP_PROBABILITY):
        self.hit_points = hit_points
        self.powerup_chance = powerup_chance
        self.is_powerup_brick = is_powerup_brick or random.random() < self.powerup_chance
        
        self.powerup_type = None
        self.powerbrick_texture = None
        if self.is_powerup_brick:
            self.powerup_type = random.choice(AVAILABLE_POWERUPS)
            self.powerbrick_texture = pygame.image.load("assets/images/powerups/powerbrick.png")
        
        # Load the initial brick image
        self.rect = pygame.image.load(BRICK_IMAGES[hit_points - 1]).get_rect(topleft=(x, y))
        self.update_image()

    def update_image(self):
        self.image = pygame.image.load(BRICK_IMAGES[self.hit_points - 1]).convert_alpha()
        
        if self.is_powerup_brick and self.powerbrick_texture:
            powerbrick_rect = self.powerbrick_texture.get_rect(center=self.rect.center)
            self.image.blit(self.powerbrick_texture, (powerbrick_rect.left - self.rect.left, powerbrick_rect.top - self.rect.top))

    def take_hit(self):
        self.hit_points -= 1
        if self.hit_points > 0:
            self.update_image()
        return self.hit_points <= 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, ball):
        return self.rect.colliderect(ball.rect)

    def maybe_drop_powerup(self):
        if self.is_powerup_brick:
            return (self.powerup_type, POWERUP_IMAGES[self.powerup_type])
        
        if random.random() < self.powerup_chance:
            powerup_type = random.choice(AVAILABLE_POWERUPS)
            return (powerup_type, POWERUP_IMAGES[powerup_type])
        
        return None
