import pygame
from settings import WIDTH, HEIGHT, TITLE, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("black")

        pygame.display.flip()

        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()