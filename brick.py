import pygame

class Brick:
    def __init__(self, x, y, images, hit_points=1):
        self.images = images  # List of images corresponding to different hit points
        self.hit_points = hit_points
        self.rect = pygame.image.load(images[hit_points - 1]).get_rect(topleft=(x, y))
        self.update_image()
    
    def update_image(self):
        # Update the image based on current hit points
        self.image = pygame.image.load(self.images[self.hit_points - 1])
    
    def take_hit(self):
        self.hit_points -= 1
        if self.hit_points > 0:
            self.update_image()
        return self.hit_points <= 0
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def check_collision(self, ball):
        return self.rect.colliderect(ball.rect)
