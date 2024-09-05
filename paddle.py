import pygame
from settings import WIDTH
import sounds

class Paddle:
    def __init__(self, x, y):
        self.original_image = pygame.image.load("assets/images/paddle.png").convert_alpha()
        self.rect = self.original_image.get_rect(topleft=(x, y))
        self.original_width = self.rect.width
        self.speed = 4
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
    
    def apply_powerup(self, powerup_type):
        sounds.activate_powerup()
        if powerup_type == 'expand':
            self.rect.width = int(self.original_width * 1.5)
        elif powerup_type == 'shrink':
            self.rect.width = max(int(self.original_width * 0.75), 10)  
        elif powerup_type == 'speed':
            self.speed += 2
        elif powerup_type == 'slow':
            self.speed = max(1, self.speed - 2)

    def draw(self, screen):
        # Prevent stretching by splitting the paddle image into three parts:
        # left cap, middle repeatable section, and right cap
        left_cap = self.original_image.subsurface((0, 0, 10, self.rect.height))  # Adjust 10 to the width of the cap
        right_cap = self.original_image.subsurface((self.original_width - 10, 0, 10, self.rect.height))
        middle_section_width = self.rect.width - 20  # Subtract the width of the caps

        if middle_section_width > 0:
            middle_section = pygame.transform.scale(
                self.original_image.subsurface((10, 0, self.original_width - 20, self.rect.height)),
                (middle_section_width, self.rect.height)
            )
        else:
            middle_section = None

        # Draw the left cap, middle section, and right cap
        screen.blit(left_cap, self.rect.topleft)
        if middle_section:
            screen.blit(middle_section, (self.rect.left + 10, self.rect.top))
        screen.blit(right_cap, (self.rect.left + self.rect.width - 10, self.rect.top))
