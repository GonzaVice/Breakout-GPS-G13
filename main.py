import pygame
from settings import WIDTH, HEIGHT, TITLE, FPS
from paddle import Paddle

def main():

    # Setting inicial
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    running = True

    # Jugador
    paddle = Paddle(x=WIDTH//2 - 16, y=HEIGHT - 20)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Movimiento por frame
        paddle.move()

        # Dibujo por frame
        screen.fill("black")
        paddle.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()