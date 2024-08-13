import pygame
from settings import WIDTH, HEIGHT
from paddle import Paddle
from brick import Brick


class Ball:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/images/ball.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = 1
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
    
    # Checkear colisión cuando la pelota choca con el paddle o los ladrillos
    def check_collision(self, obj):
        if self.rect.colliderect(obj.rect):

            # Si es un paddle
            if isinstance(obj, Paddle):
                # Rebote vertical
                if self.rect.centery < obj.rect.centery:
                    self.rect.bottom = obj.rect.top
                else:
                    self.rect.top = obj.rect.bottom
                self.speed_y = -self.speed_y

            # Si es un ladrillo (Lógica con bugs, necesita arreglarse)
            elif isinstance(obj, Brick):
                # Calcula las distancias desde la bola a los bordes del ladrillo
                overlap_x = min(self.rect.right - obj.rect.left, obj.rect.right - self.rect.left)
                overlap_y = min(self.rect.bottom - obj.rect.top, obj.rect.bottom - self.rect.top)

                # Determina la dirección del rebote en función del lado de colisión
                if overlap_x < overlap_y:
                    # Rebote horizontal (chocando con los lados)
                    if self.rect.centerx < obj.rect.centerx:
                        self.rect.right = obj.rect.left
                    else:
                        self.rect.left = obj.rect.right
                    self.speed_x = -self.speed_x
                else:
                    # Rebote vertical (chocando con la parte superior o inferior)
                    if self.rect.centery < obj.rect.centery:
                        self.rect.bottom = obj.rect.top
                    else:
                        self.rect.top = obj.rect.bottom
                    self.speed_y = -self.speed_y

            return True
        return False



    def draw(self, screen):
        screen.blit(self.image, self.rect)
    