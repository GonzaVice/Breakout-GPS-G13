import pygame
from settings import WIDTH, HEIGHT


class Ball:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/images/ball.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = 2
        self.speed_y = -2
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Rebote de izquierda a derecha
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x
        
        # Rebote de arriba y abajo (NOTA: Hacer lógica de perder vidas más adelante)
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y
    
    # Cuando la pelota choca con el paddle
    def bounce(self):
        self.speed_y = -self.speed_y
    
    # Checkear colisión de la pelota con el paddle
    def check_collision(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.bounce()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    