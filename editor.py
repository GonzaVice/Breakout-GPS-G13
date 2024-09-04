import pygame
import pygame_gui
from utils import ensure_directory_exists, LevelLoader
from settings import WIDTH, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT, BRICK_IMAGES

# Define constants for layout and sizing
UI_PANEL_WIDTH_RATIO = 0.2
EDITOR_AREA_WIDTH_RATIO = 0.8
EDITOR_AREA_HEIGHT_RATIO = 0.8

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
PREVIEW_RECT_SIZE_RATIO = 0.1
MARGIN = 10

class LevelEditor:
    def __init__(self, manager):
        self.bricks = []
        self.selected_hit_points = 1
        self.selected_powerup = False
        self.current_mode = "add"
        self.current_level = {
            "level_name": "Level 1",
            "bricks": []
        }
        self.manager = manager
        self.level_name = "level_1"
        self.is_drawing = False

        self.levels_folder = "assets/levels/"
        ensure_directory_exists(self.levels_folder)

        self.level_loader = LevelLoader()

        display_width = int(WINDOW_WIDTH * EDITOR_AREA_WIDTH_RATIO)
        display_height = int(WINDOW_HEIGHT * EDITOR_AREA_HEIGHT_RATIO)
        sidebar_width = int(WINDOW_WIDTH * UI_PANEL_WIDTH_RATIO)

        self.ui_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((display_width, 0), 
                                      (sidebar_width, WINDOW_HEIGHT)),
            manager=self.manager
        )

        self.bottom_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, display_height), 
                                      (display_width, int(WINDOW_HEIGHT * (1 - EDITOR_AREA_HEIGHT_RATIO)))),
            manager=self.manager
        )

        self.file_name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((MARGIN, MARGIN), 
                                      (BUTTON_WIDTH, 40)),
            text=f"File: {self.level_name}",
            manager=self.manager,
            container=self.ui_container
        )
        
        button_x = (sidebar_width - BUTTON_WIDTH) // 2  # Center the buttons horizontally
        
        self.load_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, 70), 
                                      (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Load Level',
            manager=self.manager,
            container=self.ui_container
        )
        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, 130), 
                                      (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Save Level',
            manager=self.manager,
            container=self.ui_container
        )
        self.file_name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((button_x, 190), 
                                      (BUTTON_WIDTH, 40)),
            manager=self.manager,
            container=self.ui_container
        )
        self.file_name_input.set_text(self.level_name)

        # Calculate the preview rectangle size while maintaining the original aspect ratio
        preview_scale_factor = min(WINDOW_WIDTH, WINDOW_HEIGHT) * PREVIEW_RECT_SIZE_RATIO
        brick_aspect_ratio = BRICK_WIDTH / BRICK_HEIGHT

        if brick_aspect_ratio > 1:
            preview_width = int(preview_scale_factor)
            preview_height = int(preview_scale_factor / brick_aspect_ratio)
        else:
            preview_height = int(preview_scale_factor)
            preview_width = int(preview_scale_factor * brick_aspect_ratio)

        # Position the preview rectangle in the bottom-right corner, with margin
        self.preview_rect = pygame.Rect(
            (WINDOW_WIDTH - preview_width - MARGIN, WINDOW_HEIGHT - preview_height - MARGIN),
            (preview_width, preview_height)
        )
        self.preview_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((MARGIN, WINDOW_HEIGHT - preview_height - 30), 
                                      (BUTTON_WIDTH, 20)),
            text="Current Brick:",
            manager=self.manager,
            container=self.ui_container,
        )

        total_button_width = BUTTON_WIDTH * 3 + MARGIN * 4  
        starting_x = (display_width - total_button_width) // 2
        button_y = (int(WINDOW_HEIGHT * (1 - EDITOR_AREA_HEIGHT_RATIO)) - BUTTON_HEIGHT) // 2

        self.mode_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((starting_x, button_y), 
                                      (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text=f"Mode: {self.current_mode.capitalize()}",
            manager=self.manager,
            container=self.bottom_container,
        )
        self.hit_points_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((starting_x + BUTTON_WIDTH + MARGIN, button_y), 
                                      (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text=f"HP: {self.selected_hit_points}",
            manager=self.manager,
            container=self.bottom_container,
        )
        self.powerup_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((starting_x + (BUTTON_WIDTH + MARGIN) * 2, button_y), 
                                      (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text=f"Powerup: {'On' if self.selected_powerup else 'Off'}",
            manager=self.manager,
            container=self.bottom_container,
        )


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
        self.level_name = self.level_loader.save_level(self.current_level, file_name)
        self.file_name_label.set_text(f"File: {self.level_name}")

    def load_level(self, file_name):
        self.level_loader.filename = "assets/levels/" + file_name + ".json"
        level_data = self.level_loader.load_level()  
        if level_data:
            self.current_level = level_data
            self.level_name = file_name
            self.file_name_label.set_text(f"File: {self.level_name}")
            self.bricks = self.current_level["bricks"]

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
    scale_x = int(WINDOW_WIDTH * EDITOR_AREA_WIDTH_RATIO) / WIDTH
    scale_y = int(WINDOW_HEIGHT * EDITOR_AREA_HEIGHT_RATIO) / HEIGHT

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
