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
            # Add other shapes or types here as needed

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
