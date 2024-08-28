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
            "level_name": "Level 1",
            "bricks": []
        }
        self.manager = manager
        self.level_name = "level_1"
        self.is_drawing = False

        # Define UI layout
        display_width = int(WINDOW_WIDTH * 0.7)
        display_height = int(WINDOW_HEIGHT * 0.7)

        # UI container on the right side
        self.ui_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((display_width, 0), (int(WINDOW_WIDTH * 0.3), WINDOW_HEIGHT)),
            manager=self.manager
        )

        # Bottom container below the level display
        self.bottom_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, display_height), (display_width , WINDOW_HEIGHT - display_height)),
            manager=self.manager
        )

        # Bottom buttons with icons and colors
        self.mode_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 10), (150, 50)),
            text=f"Mode: {self.current_mode.capitalize()}",
            manager=self.manager,
            container=self.bottom_container,
            object_id="#mode_button"
        )
        self.hit_points_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((200, 10), (150, 50)),
            text=f"HP: {self.selected_hit_points}",
            manager=self.manager,
            container=self.bottom_container,
            object_id="#hit_points_button"
        )
        self.powerup_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((380, 10), (150, 50)),
            text=f"Powerup: {'On' if self.selected_powerup else 'Off'}",
            manager=self.manager,
            container=self.bottom_container,
            object_id="#powerup_button"
        )

        self.set_button_styles()

        self.file_name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 20), (250, 50)),
            text=f"File: {self.level_name}",
            manager=self.manager,
            container=self.ui_container
        )
        self.load_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 90), (100, 50)),
            text='Load Level',
            manager=self.manager,
            container=self.ui_container
        )
        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((140, 90), (100, 50)),
            text='Save Level',
            manager=self.manager,
            container=self.ui_container
        )
        self.file_name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((20, 160), (220, 50)),
            manager=self.manager,
            container=self.ui_container
        )
        self.file_name_input.set_text(self.level_name)

    def set_button_styles(self):
        # Customize button appearances via themes
        self.manager.get_theme().load_theme('./theme.json')
        # Make sure to update the buttons with the new theme
        self.mode_button.rebuild()
        self.hit_points_button.rebuild()
        self.powerup_button.rebuild()

    def add_brick(self, x, y):
        # Remove any existing brick at the same position
        self.remove_brick(x, y)

        # Add the new brick
        brick = {
            "x": x,
            "y": y,
            "hit_points": self.selected_hit_points,
            "has_powerup": self.selected_powerup
        }
        self.current_level["bricks"].append(brick)

    def remove_brick(self, x, y):
        self.current_level["bricks"] = [brick for brick in self.current_level["bricks"] if not (brick["x"] == x and brick["y"] == y)]

    def save_level(self, file_name):
        self.current_level["level_name"] = file_name
        with open(file_name + '.json', 'w') as file:
            json.dump(self.current_level, file, indent=4)
        self.level_name = file_name
        self.file_name_label.set_text(f"File: {self.level_name}")

    def load_level(self, file_name):
        try:
            with open(file_name + '.json', 'r') as file:
                level_data = json.load(file)
                self.current_level = level_data
                self.level_name = file_name
                self.file_name_label.set_text(f"File: {self.level_name}")
                self.bricks = self.current_level["bricks"]
        except FileNotFoundError:
            print(f"Error: The file {file_name}.json was not found.")
        except json.JSONDecodeError:
            print(f"Error: The file {file_name}.json could not be parsed.")

    def draw(self, screen):
        for brick in self.current_level["bricks"]:
            hit_points = brick["hit_points"]
            brick_image = pygame.image.load(BRICK_IMAGES[hit_points - 1]).convert_alpha()
            screen.blit(brick_image, (brick["x"], brick["y"]))

            if brick["has_powerup"]:
                powerbrick_texture = pygame.image.load("assets/images/powerups/powerbrick.png").convert_alpha()
                screen.blit(powerbrick_texture, (brick["x"], brick["y"]))

    def update_ui(self):
        self.mode_button.set_text(f"Mode: {self.current_mode.capitalize()}")
        self.hit_points_button.set_text(f"HP: {self.selected_hit_points}")
        self.powerup_button.set_text(f"Powerup: {'On' if self.selected_powerup else 'Off'}")


def run_editor():
    pygame.init()
    pygame.display.set_caption('Level Editor')
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

    editor = LevelEditor(manager)

    render_surface = pygame.Surface((WIDTH, HEIGHT))
    scale_x = int(WINDOW_WIDTH * 0.7) / WIDTH  # Adjusted to take only 70% of the screen width
    scale_y = int(WINDOW_HEIGHT * 0.7) / HEIGHT

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x < int(WIDTH * scale_x):  # Ensure the click is within the render area
                    editor.is_drawing = True  # Start drawing mode
                    x = int(x / scale_x) // BRICK_WIDTH * BRICK_WIDTH
                    y = int(y / scale_y) // BRICK_HEIGHT * BRICK_HEIGHT
                    if event.button == 1:  # Left click to add or remove a brick
                        if editor.current_mode == "add":
                            editor.add_brick(x, y)
                        elif editor.current_mode == "remove":
                            editor.remove_brick(x, y)
            elif event.type == pygame.MOUSEBUTTONUP:
                editor.is_drawing = False  # Stop drawing mode
            elif event.type == pygame.MOUSEMOTION:
                if editor.is_drawing:
                    x, y = event.pos
                    if x < int(WIDTH * scale_x):  # Ensure the drag is within the render area
                        x = int(x / scale_x) // BRICK_WIDTH * BRICK_WIDTH
                        y = int(y / scale_y) // BRICK_HEIGHT * BRICK_HEIGHT
                        if editor.current_mode == "add":
                            editor.add_brick(x, y)
                        elif editor.current_mode == "remove":
                            editor.remove_brick(x, y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    editor.save_level(editor.file_name_input.get_text())

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

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == editor.save_button:
                    editor.save_level(editor.file_name_input.get_text())
                elif event.ui_element == editor.load_button:
                    editor.load_level(editor.file_name_input.get_text())
                elif event.ui_element == editor.mode_button:
                    editor.current_mode = "remove" if editor.current_mode == "add" else "add"
                    editor.update_ui()
                elif event.ui_element == editor.hit_points_button:
                    editor.selected_hit_points = (editor.selected_hit_points % 6) + 1
                    editor.update_ui()
                elif event.ui_element == editor.powerup_button:
                    editor.selected_powerup = not editor.selected_powerup
                    editor.update_ui()

            manager.process_events(event)

        screen.fill((0, 0, 0))
        render_surface.fill((0, 0, 0))

        editor.draw(render_surface)

        # Draw the scaled level display within the level display container
        scaled_surface = pygame.transform.scale(render_surface, (int(WIDTH * scale_x), int(HEIGHT * scale_y)))
        screen.blit(scaled_surface, (0, 0))  # Offset to match container position

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run_editor()
