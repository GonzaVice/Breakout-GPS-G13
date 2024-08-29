import pygame
import pygame_gui
import json
import os
from settings import WIDTH, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT, BRICK_IMAGES

class LevelEditor:
    def __init__(self, manager):
        self.bricks = []
        self.selected_hit_points = 1
        self.selected_powerup = False
        self.grid_size = (BRICK_WIDTH, BRICK_HEIGHT)
        self.current_mode = "add"
        self.current_level = {
            "level_name": "Level 1",
            "bricks": []
        }
        self.manager = manager
        self.level_name = "level_1"
        self.is_drawing = False

        self.levels_folder = "assets/levels/"

        if not os.path.exists(self.levels_folder):
            os.makedirs(self.levels_folder)

        display_width = int(WINDOW_WIDTH * 0.8)
        display_height = int(WINDOW_HEIGHT * 0.8)

        # Sidebar container
        self.ui_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((display_width, 0), (int(WINDOW_WIDTH * 0.2), WINDOW_HEIGHT)),
            manager=self.manager
        )

        # Bottom container
        self.bottom_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, display_height), (display_width, int(WINDOW_HEIGHT * 0.2))),
            manager=self.manager
        )

        # Load and Save buttons stacked vertically in the sidebar
        self.file_name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 20), (150, 40)),
            text=f"File: {self.level_name}",
            manager=self.manager,
            container=self.ui_container
        )
        self.load_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 70), (150, 50)),
            text='Load Level',
            manager=self.manager,
            container=self.ui_container
        )
        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 130), (150, 50)),
            text='Save Level',
            manager=self.manager,
            container=self.ui_container
        )
        self.file_name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 190), (150, 50)),
            manager=self.manager,
            container=self.ui_container
        )
        self.file_name_input.set_text(self.level_name)

        # Current brick preview box in the sidebar
        self.preview_rect = pygame.Rect((10, WINDOW_HEIGHT - 100), (BRICK_WIDTH, BRICK_HEIGHT))
        self.preview_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, WINDOW_HEIGHT - 130), (150, 20)),
            text="Current Brick:",
            manager=self.manager,
            container=self.ui_container
        )

        self.set_button_styles()

        # Buttons centered in the bottom container
        button_width = 150
        button_height = 50
        total_button_width = button_width * 3 + 60  # 60 is the combined padding between buttons
        starting_x = (display_width - total_button_width) // 2
        button_y = (int(WINDOW_HEIGHT * 0.2) - button_height) // 2

        self.mode_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((starting_x, button_y), (button_width, button_height)),
            text=f"Mode: {self.current_mode.capitalize()}",
            manager=self.manager,
            container=self.bottom_container,
            object_id="#mode_button"
        )
        self.hit_points_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((starting_x + button_width + 30, button_y), (button_width, button_height)),
            text=f"HP: {self.selected_hit_points}",
            manager=self.manager,
            container=self.bottom_container,
            object_id="#hit_points_button"
        )
        self.powerup_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((starting_x + (button_width + 30) * 2, button_y), (button_width, button_height)),
            text=f"Powerup: {'On' if self.selected_powerup else 'Off'}",
            manager=self.manager,
            container=self.bottom_container,
            object_id="#powerup_button"
        )

    def set_button_styles(self):
        try:
            self.manager.get_theme().load_theme('./theme.json')
        except Exception as e:
            print(f"Error loading theme: {e}")

    def add_brick(self, x, y):
        self.remove_brick(x, y)
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
        file_name = file_name if file_name.endswith('.json') else f"{file_name}.json"
        file_path = os.path.join(self.levels_folder, file_name)
        self.current_level["level_name"] = file_name
        with open(file_path, 'w') as file:
            json.dump(self.current_level, file, indent=4)
        self.level_name = file_name
        self.file_name_label.set_text(f"File: {self.level_name}")

    def load_level(self, file_name):
        file_name = file_name if file_name.endswith('.json') else f"{file_name}.json"
        file_path = os.path.join(self.levels_folder, file_name)
        try:
            with open(file_path, 'r') as file:
                level_data = json.load(file)
                self.current_level = level_data
                self.level_name = file_name
                self.file_name_label.set_text(f"File: {self.level_name}")
                self.bricks = self.current_level["bricks"]
        except FileNotFoundError:
            print(f"Error: The file {file_name} was not found in {self.levels_folder}.")
        except json.JSONDecodeError:
            print(f"Error: The file {file_name} could not be parsed.")

    def draw(self, screen):
        for brick in self.current_level["bricks"]:
            hit_points = brick["hit_points"]
            brick_image = pygame.image.load(BRICK_IMAGES[hit_points - 1]).convert_alpha()
            screen.blit(brick_image, (brick["x"], brick["y"]))

            if brick["has_powerup"]:
                powerbrick_texture = pygame.image.load("assets/images/powerups/powerbrick.png").convert_alpha()
                screen.blit(powerbrick_texture, (brick["x"], brick["y"]))

        # Draw the current brick preview in the sidebar
        self.draw_brick_preview(screen)

    def draw_brick_preview(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.preview_rect)  # Draw the box border
        hit_points = self.selected_hit_points
        brick_image = pygame.image.load(BRICK_IMAGES[hit_points - 1]).convert_alpha()
        screen.blit(brick_image, self.preview_rect.topleft)

        if self.selected_powerup:
            powerbrick_texture = pygame.image.load("assets/images/powerups/powerbrick.png").convert_alpha()
            screen.blit(powerbrick_texture, self.preview_rect.topleft)

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
    scale_x = int(WINDOW_WIDTH * 0.8) / WIDTH
    scale_y = int(WINDOW_HEIGHT * 0.8) / HEIGHT

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x < int(WIDTH * scale_x):
                    editor.is_drawing = True
                    x = int(x / scale_x) // BRICK_WIDTH * BRICK_WIDTH
                    y = int(y / scale_y) // BRICK_HEIGHT * BRICK_HEIGHT
                    if event.button == 1:
                        if editor.current_mode == "add":
                            editor.add_brick(x, y)
                        elif editor.current_mode == "remove":
                            editor.remove_brick(x, y)
            elif event.type == pygame.MOUSEBUTTONUP:
                editor.is_drawing = False
            elif event.type == pygame.MOUSEMOTION:
                if editor.is_drawing:
                    x, y = event.pos
                    if x < int(WIDTH * scale_x):
                        x = int(x / scale_x) // BRICK_WIDTH * BRICK_WIDTH
                        y = int(y / scale_y) // BRICK_HEIGHT * BRICK_HEIGHT
                        if editor.current_mode == "add":
                            editor.add_brick(x, y)
                        elif editor.current_mode == "remove":
                            editor.remove_brick(x, y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    editor.save_level(editor.file_name_input.get_text())
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
                if event.key == pygame.K_p:
                    editor.selected_powerup = not editor.selected_powerup
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

        scaled_surface = pygame.transform.scale(render_surface, (int(WIDTH * scale_x), int(HEIGHT * scale_y)))
        screen.blit(scaled_surface, (0, 0))

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run_editor()
