import pygame
from settings import WIDTH, HEIGHT, TITLE, FPS
from paddle import Paddle
from ball import Ball

def main():

    # Setting inicial
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    running = True

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
        screen.fill("black")
        paddle.draw(screen)
        ball.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()