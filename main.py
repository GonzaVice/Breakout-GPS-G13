import pygame
from settings import WIDTH, HEIGHT, TITLE, FPS, BRICK_WIDTH, BRICK_HEIGHT, \
    WINDOW_WIDTH, WINDOW_HEIGHT, BRICK_IMAGES
from paddle import Paddle
from ball import Ball
from brick import Brick


def create_bricks():
    bricks = []
    for row in range(6):
        for col in range(20):
            x = col * BRICK_WIDTH
            y = row * BRICK_HEIGHT
            image = BRICK_IMAGES[row]
            brick = Brick(x, y, image)
            bricks.append(brick)
    return bricks

def main():

    # Setting inicial
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    running = True

    # Resolución interna
    render_surface = pygame.Surface((WIDTH, HEIGHT))
    scale_x = WINDOW_WIDTH / WIDTH
    scale_y = WINDOW_HEIGHT / HEIGHT

    # Jugador
    paddle = Paddle(x=WIDTH//2 - 16, y=HEIGHT - 20)
    # Pelota
    ball = Ball(x=WIDTH//2 - 4, y=HEIGHT//2 - 4)
    # Ladrillos
    bricks = create_bricks()

    # Comienza el loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Movimiento por frame
        paddle.move()
        ball.move()

        # Chekear colisiones por frame
        ball.check_collision(paddle)
        for brick in bricks[:]:
            if brick.check_collision(ball):
                bricks.remove(brick)

        # Dibujo por frame
        render_surface.fill("black")
        paddle.draw(render_surface)
        ball.draw(render_surface)
        for brick in bricks:
            brick.draw(render_surface)

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