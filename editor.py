import pygame
import pygame_gui
import json
import os
from settings import WIDTH, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT, BRICK_IMAGES

class LevelEditor:
    def __init__(self, manager):
        # Initialization code remains the same
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

        self.ui_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((display_width, 0), (int(WINDOW_WIDTH * 0.2), WINDOW_HEIGHT)),
            manager=self.manager
        )

        self.bottom_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, display_height), (display_width, int(WINDOW_HEIGHT * 0.2))),
            manager=self.manager
        )

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

        self.preview_rect = pygame.Rect((WINDOW_WIDTH - 100, WINDOW_HEIGHT - 100), (BRICK_WIDTH * 5, BRICK_HEIGHT * 5))
        self.preview_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, WINDOW_HEIGHT - 130), (150, 20)),
            text="Current Brick:",
            manager=self.manager,
            container=self.ui_container
        )

        self.set_button_styles()

        button_width = 150
        button_height = 50
        total_button_width = button_width * 3 + 60  
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

    def draw_brick_preview(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.preview_rect, 2) 
        hit_points = self.selected_hit_points
        brick_image = pygame.image.load(BRICK_IMAGES[hit_points - 1]).convert_alpha()
        scaled_brick_image = pygame.transform.scale(brick_image, (self.preview_rect.width, self.preview_rect.height))
        
        screen.blit(scaled_brick_image, self.preview_rect.topleft)
        
        if self.selected_powerup:
            powerbrick_texture = pygame.image.load("assets/images/powerups/powerbrick.png").convert_alpha()
            scaled_powerbrick_texture = pygame.transform.scale(powerbrick_texture, (self.preview_rect.width, self.preview_rect.height))
            screen.blit(scaled_powerbrick_texture, self.preview_rect.topleft)

    def update_ui(self):
        self.mode_button.set_text(f"Mode: {self.current_mode.capitalize()}")
        self.hit_points_button.set_text(f"HP: {self.selected_hit_points}")
        self.powerup_button.set_text(f"Powerup: {'On' if self.selected_powerup else 'Off'}")

    def process_brick_placement(self, x, y, scale_x, scale_y):
        if x < int(WIDTH * scale_x):
            x = int(x / scale_x) // BRICK_WIDTH * BRICK_WIDTH
            y = int(y / scale_y) // BRICK_HEIGHT * BRICK_HEIGHT
            if self.current_mode == "add":
                self.add_brick(x, y)
            elif self.current_mode == "remove":
                self.remove_brick(x, y)

    def handle_mouse_button_down(self, event, scale_x, scale_y):
        self.is_drawing = True
        self.process_brick_placement(event.pos[0], event.pos[1], scale_x, scale_y)

    def handle_mouse_button_up(self, event):
        self.is_drawing = False

    def handle_mouse_motion(self, event, scale_x, scale_y):
        if self.is_drawing:
            self.process_brick_placement(event.pos[0], event.pos[1], scale_x, scale_y)

    def handle_key_down(self, event):
        if event.key == pygame.K_s:
            self.save_level(self.file_name_input.get_text())
        elif event.key == pygame.K_1:
            self.selected_hit_points = 1
        elif event.key == pygame.K_2:
            self.selected_hit_points = 2
        elif event.key == pygame.K_3:
            self.selected_hit_points = 3
        elif event.key == pygame.K_4:
            self.selected_hit_points = 4
        elif event.key == pygame.K_5:
            self.selected_hit_points = 5
        elif event.key == pygame.K_6:
            self.selected_hit_points = 6
        elif event.key == pygame.K_p:
            self.selected_powerup = not self.selected_powerup
        elif event.key == pygame.K_m:
            self.current_mode = "remove" if self.current_mode == "add" else "add"
        self.update_ui()

    def handle_ui_button_pressed(self, event):
        if event.ui_element == self.save_button:
            self.save_level(self.file_name_input.get_text())
        elif event.ui_element == self.load_button:
            self.load_level(self.file_name_input.get_text())
        elif event.ui_element == self.mode_button:
            self.current_mode = "remove" if self.current_mode == "add" else "add"
            self.update_ui()
        elif event.ui_element == self.hit_points_button:
            self.selected_hit_points = (self.selected_hit_points % 6) + 1
            self.update_ui()
        elif event.ui_element == self.powerup_button:
            self.selected_powerup = not self.selected_powerup
            self.update_ui()

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
                editor.handle_mouse_button_down(event, scale_x, scale_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                editor.handle_mouse_button_up(event)
            elif event.type == pygame.MOUSEMOTION:
                editor.handle_mouse_motion(event, scale_x, scale_y)
            elif event.type == pygame.KEYDOWN:
                editor.handle_key_down(event)
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                editor.handle_ui_button_pressed(event)

            manager.process_events(event)

        screen.fill((0, 0, 0))
        render_surface.fill((0, 0, 0))

        editor.draw(render_surface)

        scaled_surface = pygame.transform.scale(render_surface, (int(WIDTH * scale_x), int(HEIGHT * scale_y)))
        screen.blit(scaled_surface, (0, 0))

        manager.update(time_delta)
        manager.draw_ui(screen)

        editor.draw_brick_preview(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run_editor()
