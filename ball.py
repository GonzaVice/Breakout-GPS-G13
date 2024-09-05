import pygame
from settings import WIDTH, HEIGHT
from paddle import Paddle
from brick import Brick
import sounds

class Ball:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/images/ball.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = 3
        self.speed_y = -2
        self.is_still_col_hor = False
        self.is_still_col_ver = False

    def move(self, paddle, balls, lives, spawn_new_ball):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        running = True

        # Rebote de izquierda a derecha
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            if not self.is_still_col_hor:
                sounds.ball_hit()
                self.speed_x = -self.speed_x
                self.is_still_col_hor = True
        else:
            self.is_still_col_hor = False

        # Rebote de arriba y abajo
        if self.rect.top <= 0:
            if not self.is_still_col_ver:
                self.speed_y = -self.speed_y
                self.is_still_col_ver = True
        elif self.rect.bottom >= HEIGHT:
            if len(balls) == 1:  # revisar si es que es la ultima pelota
                lives -= 1
                if lives > 0:
                    spawn_new_ball = True
                else:
                    running = False
            balls.remove(self)  # sacar la pelota
        else:
            self.is_still_col_ver = False

        return lives, spawn_new_ball, running


    def check_collision(self, obj):
        if self.rect.colliderect(obj.rect):
            # Si es un paddle
            if isinstance(obj, Paddle):
                sounds.ball_hit()
                # Rebote vertical
                if self.rect.centery < obj.rect.centery:
                    self.rect.bottom = obj.rect.top
                else:
                    self.rect.top = obj.rect.bottom

                # Cambiar dirección horizontal basada en la posición de la colisión
                hit_pos = self.rect.centerx - obj.rect.left
                paddle_section = obj.rect.width // 5  # Divide el paddle en 5 secciones

                if hit_pos < paddle_section:
                    self.speed_x = -3 # Más hacia la izquierda
                    self.speed_y = -2
                elif hit_pos < 2 * paddle_section:
                    self.speed_x = -2 # Levemente hacia la izquierda
                    self.speed_y = -3
                elif hit_pos < 3 * paddle_section:
                    self.speed_x = 0  # Rebote central, sin cambio horizontal
                    self.speed_y = -4
                elif hit_pos < 4 * paddle_section:
                    self.speed_x = 2 # Levemente hacia la derecha
                    self.speed_y = -3
                else:
                    self.speed_x = 3 # Más hacia la derecha
                    self.speed_y = -2

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
