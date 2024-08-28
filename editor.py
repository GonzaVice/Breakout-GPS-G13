import pygame
import pygame_gui
import json
from settings import WIDTH, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT, BRICK_IMAGES

class LevelEditor:
    def __init__(self, manager):
        self.bricks = []
        self.selected_hit_points = 1
        self.selected_powerup = False
        self.grid_size = (BRICK_WIDTH, BRICK_HEIGHT)
        self.current_mode = "add"  # Start in add mode
        self.current_level = {
            "level_name": "Custom Level",
            "bricks": []
        }
        self.manager = manager

        # UI elements
        self.mode_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((20, WINDOW_HEIGHT - 70), (250, 50)),
                                                      text=f"Mode: {self.current_mode.capitalize()}",
                                                      manager=self.manager)
        self.hit_points_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((300, WINDOW_HEIGHT - 70), (250, 50)),
                                                            text=f"Hit Points: {self.selected_hit_points}",
                                                            manager=self.manager)
        self.powerup_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((600, WINDOW_HEIGHT - 70), (250, 50)),
                                                         text=f"Powerup: {'On' if self.selected_powerup else 'Off'}",
                                                         manager=self.manager)

    def add_brick(self, x, y):
        brick = {
            "x": x,
            "y": y,
            "hit_points": self.selected_hit_points,
            "has_powerup": self.selected_powerup
        }
        self.current_level["bricks"].append(brick)

    def remove_brick(self, x, y):
        for brick in self.current_level["bricks"]:
            if brick["x"] == x and brick["y"] == y:
                self.current_level["bricks"].remove(brick)
                break

    def save_level(self, file_name):
        with open(file_name + '.json', 'w') as file:
            json.dump(self.current_level, file, indent=4)

    def draw(self, screen):
        for brick in self.current_level["bricks"]:
            hit_points = brick["hit_points"]
            brick_image = pygame.image.load(BRICK_IMAGES[hit_points - 1]).convert_alpha()
            screen.blit(brick_image, (brick["x"], brick["y"]))

            if brick["has_powerup"]:
                powerbrick_texture = pygame.image.load("assets/images/powerups/powerbrick.png").convert_alpha()
                screen.blit(powerbrick_texture, (brick["x"], brick["y"]))

    def update_ui(self):
        self.mode_label.set_text(f"Mode: {self.current_mode.capitalize()}")
        self.hit_points_label.set_text(f"Hit Points: {self.selected_hit_points}")
        self.powerup_label.set_text(f"Powerup: {'On' if self.selected_powerup else 'Off'}")


def run_editor():
    pygame.init()
    pygame.display.set_caption('Level Editor')
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

    editor = LevelEditor(manager)

    render_surface = pygame.Surface((WIDTH, HEIGHT))
    scale_x = WINDOW_WIDTH / WIDTH
    scale_y = WINDOW_HEIGHT / HEIGHT

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x = int(x / scale_x) // BRICK_WIDTH * BRICK_WIDTH
                y = int(y / scale_y) // BRICK_HEIGHT * BRICK_HEIGHT

                if event.button == 1:  # Left click to add or remove a brick
                    if editor.current_mode == "add":
                        editor.add_brick(x, y)
                    elif editor.current_mode == "remove":
                        editor.remove_brick(x, y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    editor.save_level("custom_level")

                # Change hit points with number keys
                if event.key == pygame.K_1:
                    editor.selected_hit_points = 1
                elif event.key == pygame.K_2:
                    editor.selected_hit_points = 2
                elif event.key == pygame.K_3:
                    editor.selected_hit_points = 3
                elif event.key == pygame.K_4:
                    editor.selected_hit_points = 4
                elif event.key == pygame.K_5:
                    editor.selected_hit_points = 5
                elif event.key == pygame.K_6:
                    editor.selected_hit_points = 6

                # Toggle powerup with 'P' key
                if event.key == pygame.K_p:
                    editor.selected_powerup = not editor.selected_powerup

                # Switch between add and remove mode with 'M' key
                if event.key == pygame.K_m:
                    editor.current_mode = "remove" if editor.current_mode == "add" else "add"

                editor.update_ui()

            manager.process_events(event)

        screen.fill((0, 0, 0))
        render_surface.fill((0, 0, 0))

        editor.draw(render_surface)

        scaled_surface = pygame.transform.scale(render_surface, (int(WIDTH * scale_x), int(HEIGHT * scale_y)))
        screen.blit(scaled_surface, (0, 0))

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run_editor()
