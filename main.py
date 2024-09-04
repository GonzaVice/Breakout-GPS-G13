import pygame
from settings import WIDTH, HEIGHT, TITLE, FPS, \
    WINDOW_WIDTH, WINDOW_HEIGHT
from paddle import Paddle
from particle import ParticleSystem
from powerup import PowerUpSystem
from utils import LevelLoader
from button import Button
from ball import Ball

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def draw_lives(screen, lives, filled_heart):
    for i in range(3):
        x_position = screen.get_width() - (20 + 10) * (i + 1)  # Start from the right and move left
        y_position = 10  # Keep the y position fixed at the top
        if i < lives:
            screen.blit(filled_heart, (x_position, y_position))

def show_menu():
    menu_running = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    bg = pygame.image.load('assets/images/background.png')

    while menu_running:
        screen.blit(bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(45).render("MAIN MENU", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, 100))

        choose_text = get_font(35).render("Choose a level", True, (255, 255, 255))
        choose_rect = choose_text.get_rect(center=(WINDOW_WIDTH // 2, 150))

        # Create level buttons in two rows of five
        level_buttons = []
        for i in range(10):
            row = i // 5
            col = i % 5
            x = (WINDOW_WIDTH // 2 - 300) + col * 150
            y = 250 + row * 120
            level_buttons.append(Button(
                image=pygame.image.load('assets/images/level_button.png'),
                pos=(x, y),
                text_input=f"{i+1}",
                font=get_font(30),
                base_color=(255, 255, 255),
                hovering_color="White"
            ))

        # Quit button
        quit_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),
            pos=(WINDOW_WIDTH // 2, 500),
            text_input="QUIT",
            font=get_font(30),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

        screen.blit(menu_text, menu_rect)
        screen.blit(choose_text, choose_rect)

        # Update and draw level buttons
        for button in level_buttons:
            button.changeColor(mouse_pos)
            button.update(screen)

        # Update and draw quit button
        quit_button.changeColor(mouse_pos)
        quit_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(level_buttons):
                    if button.checkForInput(mouse_pos):
                        level = f"level_{i+1}.json"
                        return level
                if quit_button.checkForInput(mouse_pos):
                    running = False
                    menu_running = False

        pygame.display.update()

def pause_menu():
    menu_running = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    bg = pygame.image.load('assets/images/background.png')

    while menu_running:
        screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()

        pause_text = get_font(100).render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, 100))

        continue_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),
            pos=(WINDOW_WIDTH // 2, 250),
            text_input="CONTINUE",
            font=get_font(50),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

        quit_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),
            pos=(WINDOW_WIDTH // 2, 400),
            text_input="QUIT",
            font=get_font(50),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

        screen.blit(pause_text, pause_rect)

        # Update and draw buttons
        for button in [continue_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.checkForInput(mouse_pos):
                    menu_running = False  # Exit pause menu to continue the game
                if quit_button.checkForInput(mouse_pos):
                    menu_running = False
                    return False

        pygame.display.update()
    return True

def game_over_menu():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    bg = pygame.image.load('assets/images/background.png')
    menu_running = True

    while menu_running:
        screen.blit(bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        game_over_text = get_font(100).render("YOU LOST", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 100))

        main_menu_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),
            pos=(WINDOW_WIDTH // 2, 250),
            text_input="MAIN MENU",
            font=get_font(50),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

        quit_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),
            pos=(WINDOW_WIDTH // 2, 400),
            text_input="QUIT",
            font=get_font(50),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

        screen.blit(game_over_text, game_over_rect)

        for button in [main_menu_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.checkForInput(mouse_pos):
                    main()  # Restart the game loop
                if quit_button.checkForInput(mouse_pos):
                    return False  # Quit the game

        pygame.display.update()

def you_win_menu():
    menu_running = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    bg = pygame.image.load('assets/images/background.png')

    while menu_running:
        screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()

        won_text = get_font(80).render("YOU WIN!", True, (255, 255, 255))
        won_rect = won_text.get_rect(center=(WINDOW_WIDTH // 2, 100))

        restart_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),
            pos=(WINDOW_WIDTH // 2, 250),
            text_input="RESTART",
            font=get_font(50),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

        quit_button = Button(
            image=pygame.image.load('assets/images/quit_button.png'),
            pos=(WINDOW_WIDTH // 2, 400),
            text_input="QUIT",
            font=get_font(50),
            base_color=(255, 255, 255),
            hovering_color="White"
        )

        screen.blit(won_text, won_rect)

        # Update and draw buttons
        for button in [restart_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.checkForInput(mouse_pos):
                    main()
                if quit_button.checkForInput(mouse_pos):
                    menu_running = False
                    return False

        pygame.display.update()
    return False


def main():
    # Setting inicial
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    running = True
    freeze = False

    lives = 3
    spawn_new_ball = False
    show_game_over = False

    filled_heart_img = pygame.image.load("assets/images/filled_heart.png")
    empty_heart_img = pygame.image.load("assets/images/empty_heart.png")

    desired_width = 20
    desired_height = 20
    filled_heart_img = pygame.transform.scale(filled_heart_img, (desired_width, desired_height))

    # Resolución interna
    render_surface = pygame.Surface((WIDTH, HEIGHT))
    scale_x = WINDOW_WIDTH / WIDTH
    scale_y = WINDOW_HEIGHT / HEIGHT

    # Jugador
    paddle = Paddle(x=WIDTH//2 - 16, y=HEIGHT - 20)

    # Pelota
    balls = []

    level = show_menu()
    # Ladrillos
    level_loader = LevelLoader(level)
    level_data = level_loader.load_level()
    if level_data:
        level_loader.parse_level_data(level_data)
        bricks = level_loader.get_bricks()

    particle_system = ParticleSystem()
    powerup_system = PowerUpSystem()

    powerup_system.shoot_mode = True

    pause_text = get_font(8).render("P to Pause", True, (255, 255, 255))
    pause_rect = pause_text.get_rect(topleft=(10, 10))

    while running:
        keys = pygame.key.get_pressed()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: # incorporando el menu de pausa
                    if not pause_menu():
                        running = False
                        return

        freeze = powerup_system.shoot_mode

        render_surface.fill("black")

        if not freeze:
            paddle.move()
            for ball in balls:
                lives, spawn_new_ball, running = ball.move(paddle, balls, lives, spawn_new_ball)
                if not running:
                    game_over_menu()
                    break

            if spawn_new_ball:
                # Spawn a new ball on the paddle
                new_ball = Ball(paddle.rect.centerx, paddle.rect.top - 10)
                balls.append(new_ball)
                spawn_new_ball = False

        bricks_to_remove = []

        # Check collisions
        for ball in balls:
            for brick in bricks:
                if ball.check_collision(brick):
                    if brick.take_hit() and brick not in bricks_to_remove:
                        bricks_to_remove.append(brick)
                        particle_system.add_particles(brick.rect.centerx, brick.rect.centery, (200, 0, 0), count=15, type="circle")
                        particle_system.add_particles(brick.rect.centerx, brick.rect.centery, (255, 255, 0), count=5, type="square")

                        powerup_data = brick.maybe_drop_powerup()
                        if powerup_data:
                            powerup_type, powerup_image = powerup_data
                            powerup_system.spawn_powerup(brick.rect.centerx, brick.rect.centery, powerup_type, powerup_image)

        for brick in bricks_to_remove:
            bricks.remove(brick)

        for ball in balls:
            ball.check_collision(paddle)

        powerup_system.update(paddle, balls, keys, events)
        particle_system.update()

        paddle.draw(render_surface)
        for ball in balls:
            ball.draw(render_surface)
        for brick in bricks:
            brick.draw(render_surface)

        if not bricks:
            running = you_win_menu()
            if not running:
                break

        powerup_system.draw(render_surface, paddle)
        particle_system.draw(render_surface)

        draw_lives(render_surface, lives, filled_heart_img)

        render_surface.blit(pause_text, pause_rect)

        scaled_surface = pygame.transform.scale(render_surface,
                                                (int(WIDTH * scale_x),
                                                int(HEIGHT * scale_y)))
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
