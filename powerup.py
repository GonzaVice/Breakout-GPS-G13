import pygame
import time
from settings import HEIGHT, WIDTH

class PowerUp:
    def __init__(self, x, y, powerup_type, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center=(x, y))
        self.powerup_type = powerup_type
        self.speed = 2

    def move(self):
        self.rect.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collect(self):
        return self.powerup_type

class PowerUpSystem:
    def __init__(self, powerup_duration=5):
        self.active_powerups = []
        self.active_effects = []
        self.powerup_duration = powerup_duration

    def spawn_powerup(self, x, y, powerup_type, image):
        powerup = PowerUp(x, y, powerup_type, image)
        self.active_powerups.append(powerup)

    def update(self, paddle):
        current_time = time.time()

        # Move and check collisions for power-ups
        for powerup in self.active_powerups[:]:
            powerup.move()
            if powerup.rect.colliderect(paddle.rect):
                effect_type = powerup.collect()

                # Remove any active size or speed power-up before applying the new one
                self.remove_conflicting_effects(effect_type, paddle)

                # Apply the new power-up
                paddle.apply_powerup(effect_type)
                self.active_effects.append({"type": effect_type, "start_time": current_time, "target": paddle})
                self.active_powerups.remove(powerup)
            elif powerup.rect.top > HEIGHT:  # Remove power-ups that go off-screen
                self.active_powerups.remove(powerup)

        # Update active effects and remove expired ones
        for effect in self.active_effects[:]:
            if current_time - effect["start_time"] > self.powerup_duration:
                if effect["type"] == "expand" or effect["type"] == "shrink":
                    effect["target"].rect.width = effect["target"].original_width
                elif effect["type"] == "speed" or effect["type"] == "slow":
                    effect["target"].speed = 4  # Reset to original speed
                self.active_effects.remove(effect)

    def remove_conflicting_effects(self, new_effect_type, paddle):
        """Remove any active effects that conflict with the new power-up type."""
        conflicting_types = []
        if new_effect_type in ["expand", "shrink"]:
            conflicting_types = ["expand", "shrink"]
        elif new_effect_type in ["speed", "slow"]:
            conflicting_types = ["speed", "slow"]

        # Remove the conflicting effects
        self.active_effects = [
            effect for effect in self.active_effects
            if effect["type"] not in conflicting_types
        ]

        # Reset the paddle properties if necessary
        for effect_type in conflicting_types:
            if effect_type == "expand" or effect_type == "shrink":
                paddle.rect.width = paddle.original_width
            elif effect_type == "speed" or effect_type == "slow":
                paddle.speed = 4  # Reset to original speed

    def draw(self, screen):
        # Draw all active power-ups falling on the screen
        for powerup in self.active_powerups:
            powerup.draw(screen)

        # Draw active power-up effects in the bottom-right corner
        for index, effect in enumerate(self.active_effects):
            # Load the power-up icon image
            powerup_icon = pygame.image.load(f"assets/images/powerups/{effect['type']}.png").convert_alpha()
            icon_size = 32  # Set the size of the icons
            icon_x = WIDTH - (icon_size + 10)  # 10 pixels from the right edge
            icon_y = HEIGHT - (icon_size + 10) * (index + 1)  # Stacking from the bottom

            # Draw the power-up icon
            screen.blit(pygame.transform.scale(powerup_icon, (icon_size, icon_size)), (icon_x, icon_y))

            # Calculate remaining time as a percentage
            current_time = time.time()
            time_elapsed = current_time - effect['start_time']
            time_remaining_ratio = max(0, 1 - (time_elapsed / self.powerup_duration))

            # Draw the time bar below the icon
            bar_width = icon_size
            bar_height = 5
            bar_x = icon_x
            bar_y = icon_y + icon_size + 2 

            time_bar_rect = pygame.Rect(bar_x, bar_y, bar_width * time_remaining_ratio, bar_height)
            pygame.draw.rect(screen, (0, 255, 0), time_bar_rect)  # Green bar indicating remaining time
