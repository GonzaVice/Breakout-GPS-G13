import pygame

class Brick:
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    # Cuando choque con la pelota
    def check_collision(self, ball):
        if self.rect.colliderect(ball.rect):
            ball.bounce()
            return True
        return False