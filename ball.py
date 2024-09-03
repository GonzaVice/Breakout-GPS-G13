import pygame
import math
from settings import WIDTH, HEIGHT, BALL_SPEED
from paddle import Paddle
from brick import Brick

class Ball:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/images/ball.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.angle = math.radians(45)  # Initial angle of movement in radians
        self.update_speed_components()

        # Log initial speed and modulus
        self.log_speed("Initial speed")

    def update_speed_components(self):
        self.speed_x = BALL_SPEED * math.cos(self.angle)
        self.speed_y = -BALL_SPEED * math.sin(self.angle)  # Negative to move upwards initially

    def normalize_speed(self):
        speed = math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)
        self.speed_x = (self.speed_x / speed) * BALL_SPEED
        self.speed_y = (self.speed_y / speed) * BALL_SPEED

        # Log normalized speed and modulus
        self.log_speed("Normalized speed")

    def log_speed(self, context):
        speed_modulus = math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)
        print(f"{context}: ({self.speed_x:.2f}, {self.speed_y:.2f}), Modulus: {speed_modulus:.2f}")

    def move(self, paddle, balls, lives, spawn_new_ball):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        running = True

        # Wall collisions
        if self.rect.left <= 0:  # Hit the left wall
            self.rect.left = 0
            self.angle = math.pi - self.angle  # Reflect the angle horizontally
            self.update_speed_components()
            print("Collision: Left wall")
            self.log_speed("After collision with Left wall")

        elif self.rect.right >= WIDTH:  # Hit the right wall
            self.rect.right = WIDTH
            self.angle = math.pi - self.angle  # Reflect the angle horizontally
            self.update_speed_components()
            print("Collision: Right wall")
            self.log_speed("After collision with Right wall")

        if self.rect.top <= 0:  # Hit the top wall
            self.rect.top = 0
            self.angle = -self.angle  # Reflect the angle vertically
            self.update_speed_components()
            print("Collision: Top wall")
            self.log_speed("After collision with Top wall")

        elif self.rect.bottom >= HEIGHT:  # Hit the bottom (player loses a life)
            if len(balls) == 1:  # Check if it's the last ball
                lives -= 1
                if lives > 0:
                    spawn_new_ball = True
                else:
                    running = False
            balls.remove(self)  # Remove the ball
            print("Collision: Bottom wall")
            self.log_speed("After collision with Bottom wall")

        return lives, spawn_new_ball, running

    def check_collision(self, obj):
        if self.rect.colliderect(obj.rect):
            if isinstance(obj, Paddle):
                # Calculate the point of impact
                hit_pos = self.rect.centerx - obj.rect.left
                hit_ratio = (hit_pos / obj.rect.width) - 0.5  # Ratio from -0.5 to 0.5

                # Adjust angle based on hit position
                self.angle = math.radians(90) - (hit_ratio * math.radians(70))
                self.update_speed_components()
                print("Collision: Paddle")
                self.log_speed("After collision with Paddle")

            elif isinstance(obj, Brick):
                # Calculate overlaps
                overlap_x = min(self.rect.right - obj.rect.left, obj.rect.right - self.rect.left)
                overlap_y = min(self.rect.bottom - obj.rect.top, obj.rect.bottom - self.rect.top)

                # Determine which side is hit and reflect accordingly
                if overlap_x < overlap_y:
                    self.angle = math.pi - self.angle  # Reflect horizontally
                    print("Collision: Brick (Horizontal)")
                else:
                    self.angle = -self.angle  # Reflect vertically
                    print("Collision: Brick (Vertical)")

                self.update_speed_components()
                self.log_speed("After collision with Brick")

            # Normalize speed after collision
            self.normalize_speed()

            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
