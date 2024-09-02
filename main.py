import pygame
from settings import WIDTH, HEIGHT, TITLE, FPS, \
    WINDOW_WIDTH, WINDOW_HEIGHT
from paddle import Paddle
from particle import ParticleSystem
from powerup import PowerUpSystem
from utils import LevelLoader


def main():
    # Setting inicial
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    running = True
    freeze = False

    # Resolución interna
    render_surface = pygame.Surface((WIDTH, HEIGHT))
    scale_x = WINDOW_WIDTH / WIDTH
    scale_y = WINDOW_HEIGHT / HEIGHT

    # Jugador
    paddle = Paddle(x=WIDTH//2 - 16, y=HEIGHT - 20)

    # Pelota
    balls = []

    # Ladrillos
    level_loader = LevelLoader("level_1.json")
    level_data = level_loader.load_level()  
    if level_data:
        level_loader.parse_level_data(level_data) 
        bricks = level_loader.get_bricks()

    particle_system = ParticleSystem()
    powerup_system = PowerUpSystem()

    powerup_system.shoot_mode = True

    # Comienza el loop
    while running:
        keys = pygame.key.get_pressed()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        freeze = powerup_system.shoot_mode

        # Movimiento por frame
        if not freeze:
            paddle.move()
            for ball in balls:
                ball.move()

        bricks_to_remove = []

        # Chekear colisiones por frame
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

        # Update power-up system
        powerup_system.update(paddle, balls, keys, events)

        # Update particles
        particle_system.update()

        # Dibujo por frame
        render_surface.fill("black")
        paddle.draw(render_surface)
        for ball in balls:
            ball.draw(render_surface)
        for brick in bricks:
            brick.draw(render_surface)

        powerup_system.draw(render_surface, paddle)
        particle_system.draw(render_surface)

        # Escalar al tamaño de la ventana
        scaled_surface = pygame.transform.scale(render_surface,
                                                (int(WIDTH * scale_x),
                                                 int(HEIGHT * scale_y)))
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
