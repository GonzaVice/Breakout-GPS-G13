import pygame
import random

class Particle:
    def __init__(self, x, y, color, type="circle", lifespan=60, size=3):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.color = color
        self.type = type 
        self.lifespan = lifespan
        self.age = 0
        self.size = size 

    def update(self):
        self.position += self.velocity
        self.age += 1
        self.size = max(0, self.size * (1 - (self.age / self.lifespan)))  
    
    def draw(self, screen):
        if self.age < self.lifespan:
            alpha = 255 - (255 * (self.age / self.lifespan))
            color_with_alpha = (*self.color, int(alpha))

            if self.type == "circle":
                pygame.draw.circle(screen, color_with_alpha, (int(self.position.x), int(self.position.y)), int(self.size))
            elif self.type == "square":
                pygame.draw.rect(screen, color_with_alpha, pygame.Rect(int(self.position.x - self.size // 2), int(self.position.y - self.size // 2), int(self.size), int(self.size)))
            elif self.type == "triangle":
                self.draw_triangle(screen, color_with_alpha)
            elif self.type == "star":
                self.draw_star(screen, color_with_alpha)
            elif self.type == "hexagon":
                self.draw_hexagon(screen, color_with_alpha)

    def draw_triangle(self, screen, color_with_alpha):
        points = [
            (self.position.x, self.position.y - self.size),
            (self.position.x - self.size, self.position.y + self.size),
            (self.position.x + self.size, self.position.y + self.size),
        ]
        pygame.draw.polygon(screen, color_with_alpha, points)

    def draw_star(self, screen, color_with_alpha):
        # Define points for a simple star shape
        points = []
        for i in range(5):
            angle = i * 72
            x = self.position.x + self.size * (1 if i % 2 == 0 else 0.5) * pygame.math.Vector2(1, 0).rotate(angle).x
            y = self.position.y + self.size * (1 if i % 2 == 0 else 0.5) * pygame.math.Vector2(1, 0).rotate(angle).y
            points.append((x, y))
        pygame.draw.polygon(screen, color_with_alpha, points)

    def draw_hexagon(self, screen, color_with_alpha):
        points = [
            (self.position.x + self.size * pygame.math.Vector2(1, 0).rotate(angle).x,
             self.position.y + self.size * pygame.math.Vector2(1, 0).rotate(angle).y)
            for angle in range(0, 360, 60)
        ]
        pygame.draw.polygon(screen, color_with_alpha, points)

    def is_alive(self):
        return self.age < self.lifespan

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_particles(self, x, y, color, count=10, type="circle"):
        for _ in range(count):
            size = random.uniform(3, 6)  # Random initial size
            self.particles.append(Particle(x, y, color, type, size=size))
    
    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
