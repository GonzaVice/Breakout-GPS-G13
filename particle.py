import pygame
import random

class Particle:
    def __init__(self, x, y, color, lifespan=60):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.color = color
        self.lifespan = lifespan
        self.age = 0
    
    def update(self):
        self.position += self.velocity
        self.age += 1
    
    def draw(self, screen):
        if self.age < self.lifespan:
            alpha = 255 - (255 * (self.age / self.lifespan))
            color_with_alpha = (*self.color, int(alpha))
            pygame.draw.circle(screen, color_with_alpha, (int(self.position.x), int(self.position.y)), 3)

    def is_alive(self):
        return self.age < self.lifespan

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_particles(self, x, y, color, count=10):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
