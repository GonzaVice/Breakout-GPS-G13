import pygame
from settings import WIDTH

class Paddle:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/images/paddle.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)