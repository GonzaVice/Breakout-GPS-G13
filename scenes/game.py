import pygame
from .scene import Scene
from paddle import Paddle
from particle import ParticleSystem
from powerup import PowerUpSystem
from utils import LevelLoader, get_font, draw_lives
from settings import WIDTH, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT
from button import Button
from ball import Ball

class PauseMenuScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.bg = pygame.image.load('assets/images/background.png')

        self.continue_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),  # Add the appropriate image path
            pos=(WINDOW_WIDTH // 2, 250),
            text_input="CONTINUE",
            font=get_font(50),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

        self.quit_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),
            pos=(WINDOW_WIDTH // 2, 400),
            text_input="QUIT",
            font=get_font(50),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                self.manager.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.continue_button.checkForInput(mouse_pos):
                    self.manager.go_back()  # Resume game
                if self.quit_button.checkForInput(mouse_pos):
                    self.manager.quit()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        pause_text = get_font(100).render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(pause_text, pause_rect)

        for button in [self.continue_button, self.quit_button]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)


class MainMenuScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.bg = pygame.image.load('assets/images/background.png')
        self.level_buttons = []
        for i in range(5):
            row = i // 5
            col = i % 5
            x = (WINDOW_WIDTH // 2 - 300) + col * 150
            y = 250 + row * 100
            self.level_buttons.append(Button(
                image=pygame.image.load('assets/images/level_button.png'),
                pos=(x, y),
                text_input=f"{i+1}",
                font=get_font(30),
                base_color=(255, 255, 255),
                hovering_color="White"
            ))

        self.quit_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),
            pos=(WINDOW_WIDTH // 2, 450),
            text_input="QUIT",
            font=get_font(30),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                self.manager.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(self.level_buttons):
                    if button.checkForInput(mouse_pos):
                        level = f"level_{i+1}.json"
                        self.manager.go_to(GameScene(self.manager, level))
                if self.quit_button.checkForInput(mouse_pos):
                    self.manager.quit()

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        menu_text = get_font(45).render("MAIN MENU", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(menu_text, menu_rect)

        for button in self.level_buttons + [self.quit_button]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)


class GameScene(Scene):
    def __init__(self, manager, level):
        super().__init__(manager)
        self.lives = 3
        self.spawn_new_ball = False
        self.show_game_over = False
        self.level = level
        self.pause_text = get_font(8).render("P to Pause", True, (255, 255, 255))
        self.pause_rect = self.pause_text.get_rect(topleft=(10, 10))

        self.filled_heart_img = pygame.image.load("assets/images/filled_heart.png")
        self.filled_heart_img = pygame.transform.scale(self.filled_heart_img, (20, 20))

        # Initialize game objects
        self.paddle = Paddle(x=WIDTH//2 - 16, y=HEIGHT - 20)
        self.balls = []
        self.level_loader = LevelLoader(self.level)
        level_data = self.level_loader.load_level()
        if level_data:
            self.level_loader.parse_level_data(level_data)
            self.bricks = self.level_loader.get_bricks()

        self.particle_system = ParticleSystem()
        self.powerup_system = PowerUpSystem()

        # Create an internal render surface and calculate scaling factors
        self.render_surface = pygame.Surface((WIDTH, HEIGHT))
        self.scale_x = WINDOW_WIDTH / WIDTH
        self.scale_y = WINDOW_HEIGHT / HEIGHT

        self.powerup_system.shoot_mode = True

    def handle_events(self, events):
        self.powerup_system.handle_event(event, self.paddle, self.balls)

        for event in events:
            if event.type == pygame.QUIT:
                self.manager.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.manager.go_to(PauseMenuScene(self.manager))

            # Pass relevant events to the power-up system

    def update(self):
        if self.powerup_system.shoot_mode:
            self.powerup_system.update(self.paddle, self.balls)
            return  # Freeze game while in shoot mode

        self.paddle.move()
        for ball in self.balls:
            self.lives, self.spawn_new_ball, running = ball.move(self.paddle, self.balls, self.lives, self.spawn_new_ball)
            if not running:
                self.manager.go_to(GameOverScene(self.manager))
                return

        if self.spawn_new_ball:
            new_ball = Ball(self.paddle.rect.centerx, self.paddle.rect.top - 10)
            self.balls.append(new_ball)
            self.spawn_new_ball = False

        bricks_to_remove = []
        for ball in self.balls:
            for brick in self.bricks:
                if ball.check_collision(brick):
                    if brick.take_hit() and brick not in bricks_to_remove:
                        bricks_to_remove.append(brick)
                        self.particle_system.add_particles(brick.rect.centerx, brick.rect.centery, (200, 0, 0), count=15, type="circle")
                        self.particle_system.add_particles(brick.rect.centerx, brick.rect.centery, (255, 255, 0), count=5, type="square")
                        powerup_data = brick.maybe_drop_powerup()
                        if powerup_data:
                            powerup_type, powerup_image = powerup_data
                            self.powerup_system.spawn_powerup(brick.rect.centerx, brick.rect.centery, powerup_type, powerup_image)

        for brick in bricks_to_remove:
            self.bricks.remove(brick)

        for ball in self.balls:
            ball.check_collision(self.paddle)

        self.powerup_system.update(self.paddle, self.balls)
        self.particle_system.update()

        if not self.bricks:
            self.manager.go_to(YouWinScene(self.manager))

    def draw(self, screen):
        self.render_surface.fill("black")
        self.paddle.draw(self.render_surface)
        for ball in self.balls:
            ball.draw(self.render_surface)
        for brick in self.bricks:
            brick.draw(self.render_surface)

        self.powerup_system.draw(self.render_surface, self.paddle)
        self.particle_system.draw(self.render_surface)
        draw_lives(self.render_surface, self.lives, self.filled_heart_img)
        self.render_surface.blit(self.pause_text, self.pause_rect)

        # Scale the render surface to the window size
        scaled_surface = pygame.transform.scale(self.render_surface, (int(WIDTH * self.scale_x), int(HEIGHT * self.scale_y)))
        screen.blit(scaled_surface, (0, 0))


class GameOverScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.bg = pygame.image.load('assets/images/background.png')

        self.main_menu_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),  # Use an appropriate image
            pos=(WINDOW_WIDTH // 2, 250),
            text_input="MAIN MENU",
            font=get_font(50),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

        self.quit_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),
            pos=(WINDOW_WIDTH // 2, 400),
            text_input="QUIT",
            font=get_font(50),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                self.manager.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.main_menu_button.checkForInput(mouse_pos):
                    self.manager.go_to(MainMenuScene(self.manager))
                if self.quit_button.checkForInput(mouse_pos):
                    self.manager.quit()

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        game_over_text = get_font(100).render("YOU LOST", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(game_over_text, game_over_rect)

        for button in [self.main_menu_button, self.quit_button]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)


class YouWinScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.bg = pygame.image.load('assets/images/background.png')

        self.main_menu_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),
            pos=(WINDOW_WIDTH // 2, 250),
            text_input="MAIN MENU",
            font=get_font(50),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

        self.quit_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),
            pos=(WINDOW_WIDTH // 2, 400),
            text_input="QUIT",
            font=get_font(50),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                self.manager.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.main_menu_button.checkForInput(mouse_pos):
                    self.manager.go_to(MainMenuScene(self.manager))
                if self.quit_button.checkForInput(mouse_pos):
                    self.manager.quit()

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        win_text = get_font(100).render("YOU WIN!", True, (255, 255, 255))
        win_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(win_text, win_rect)

        for button in [self.main_menu_button, self.quit_button]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)
