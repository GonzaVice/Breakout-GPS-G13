import pygame
import time
import math
from ball import Ball
from settings import HEIGHT, WIDTH, POWERUP_IMAGES, BALL_SPEED

class PowerUp:
    def __init__(self, x, y, powerup_type, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center=(x, y))
        self.powerup_type = powerup_type
        self.speed = 1

    def move(self):
        self.rect.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collect(self):
        return self.powerup_type

class PowerUpSystem:
    def __init__(self, powerup_duration=8):
        self.active_powerups = []
        self.active_effects = []
        self.powerup_duration = powerup_duration
        self.shoot_mode = False
        self.pointer_angle = -math.pi / 2  # Start pointing upwards
        self.pointer_length = 50  # Length of the pointer line

    def spawn_powerup(self, x, y, powerup_type, image):
        powerup = PowerUp(x, y, powerup_type, image)
        self.active_powerups.append(powerup)

    def update(self, paddle, balls, keys, events):
        current_time = time.time()

        if self.shoot_mode:
            self._update_shoot_mode(paddle, balls, keys, events)
        else:
            self._update_powerups(paddle, balls, current_time)
            self._update_effects(current_time, paddle)

    def _update_powerups(self, paddle, balls, current_time):
        for powerup in self.active_powerups[:]:
            powerup.move()
            if powerup.rect.colliderect(paddle.rect):
                self._handle_powerup_collect(powerup, paddle, balls, current_time)
                self.active_powerups.remove(powerup)
            elif powerup.rect.top > HEIGHT:
                self.active_powerups.remove(powerup)

    def _handle_powerup_collect(self, powerup, paddle, balls, current_time):
        effect_type = powerup.collect()

        if effect_type == "expand":
            self._apply_expand_powerup(paddle, effect_type, current_time)
        elif effect_type == "duplicate":
            self._apply_duplicate_powerup(balls)
        elif effect_type == "shoot":
            self._activate_shoot_mode()

    def _apply_expand_powerup(self, paddle, effect_type, current_time):
        self._remove_conflicting_effects(effect_type, paddle)
        paddle.apply_powerup(effect_type)
        self.active_effects.append({"type": effect_type, "start_time": current_time, "target": paddle})

    def _apply_duplicate_powerup(self, balls):
        new_balls = []
        for ball in balls:
            new_ball = Ball(ball.rect.x, ball.rect.y)
            new_ball.speed_x = -ball.speed_x
            new_ball.speed_y = ball.speed_y
            new_balls.append(new_ball)
        balls.extend(new_balls)

    def _activate_shoot_mode(self):
        self.shoot_mode = True

    def _update_shoot_mode(self, paddle, balls, keys, events):
        self._control_pointer_angle(keys)
        self._handle_shoot_event(paddle, balls, events)

    def _control_pointer_angle(self, keys):
        if keys[pygame.K_LEFT]:
            self.pointer_angle -= 0.05
        elif keys[pygame.K_RIGHT]:
            self.pointer_angle += 0.05

        self.pointer_angle %= 2 * math.pi

    def _handle_shoot_event(self, paddle, balls, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._shoot_new_ball(paddle, balls)
                self.shoot_mode = False 

    def _shoot_new_ball(self, paddle, balls):
        speed_x = BALL_SPEED * math.cos(self.pointer_angle)
        speed_y = BALL_SPEED * math.sin(self.pointer_angle)

        new_ball = Ball(paddle.rect.centerx, paddle.rect.top - 10)
        new_ball.speed_x = speed_x
        new_ball.speed_y = speed_y

        balls.append(new_ball)

    def _update_effects(self, current_time, paddle):
        for effect in self.active_effects[:]:
            if current_time - effect["start_time"] > self.powerup_duration:
                self._remove_expired_effect(effect, paddle)

    def _remove_expired_effect(self, effect, paddle):
        if effect["type"] == "expand":
            paddle.rect.width = paddle.original_width
        self.active_effects.remove(effect)

    def _remove_conflicting_effects(self, new_effect_type, paddle):
        if new_effect_type == "expand":
            self.active_effects = [effect for effect in self.active_effects if effect["type"] != "expand"]
            paddle.rect.width = paddle.original_width

    def draw(self, screen, paddle):
        for powerup in self.active_powerups:
            powerup.draw(screen)

        self._draw_active_effects(screen)

        if self.shoot_mode:
            self._draw_pointer(screen, paddle)

    def _draw_active_effects(self, screen):
        for index, effect in enumerate(self.active_effects):
            self._draw_effect_icon(screen, effect, index)

    def _draw_effect_icon(self, screen, effect, index):
        powerup_icon = pygame.image.load(f"assets/images/powerups/{effect['type']}.png").convert_alpha()
        icon_size = 32
        icon_x = WIDTH - (icon_size + 10)
        icon_y = HEIGHT - (icon_size + 10) * (index + 1)

        screen.blit(pygame.transform.scale(powerup_icon, (icon_size, icon_size)), (icon_x, icon_y))

        self._draw_time_bar(screen, effect, icon_x, icon_y, icon_size)

    def _draw_time_bar(self, screen, effect, icon_x, icon_y, icon_size):
        current_time = time.time()
        time_elapsed = current_time - effect['start_time']
        time_remaining_ratio = max(0, 1 - (time_elapsed / self.powerup_duration))

        bar_width = icon_size
        bar_height = 5
        bar_x = icon_x
        bar_y = icon_y + icon_size + 2 

        time_bar_rect = pygame.Rect(bar_x, bar_y, bar_width * time_remaining_ratio, bar_height)
        pygame.draw.rect(screen, (0, 255, 0), time_bar_rect)

    def _draw_pointer(self, screen, paddle):
        end_x = paddle.rect.centerx + self.pointer_length * math.cos(self.pointer_angle)
        end_y = paddle.rect.centery - 10 + self.pointer_length * math.sin(self.pointer_angle)

        pygame.draw.line(screen, (255, 0, 0), paddle.rect.center, (end_x, end_y), 3)
