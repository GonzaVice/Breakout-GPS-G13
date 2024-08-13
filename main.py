import pygame
from settings import WIDTH, HEIGHT, TITLE, FPS
from paddle import Paddle
from ball import Ball

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720

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

    # Comienza el loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Movimiento por frame
        paddle.move()
        ball.move()
        ball.check_collision(paddle)

        # Dibujo por frame
        render_surface.fill("black")
        paddle.draw(render_surface)
        ball.draw(render_surface)

        # Escalar al tamaño de la ventana
        scaled_surface = pygame.transform.scale(render_surface, (int(WIDTH * scale_x), int(HEIGHT * scale_y)))
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()