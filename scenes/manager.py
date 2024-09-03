class SceneManager:
    def __init__(self):
        self.running = True
        self.scenes = []

    def go_to(self, scene):
        """Switch to a new scene."""
        self.scenes = [scene]

    def push(self, scene):
        """Push a new scene on top of the current one."""
        self.scenes.append(scene)

    def go_back(self):
        """Return to the previous scene."""
        if len(self.scenes) > 1:
            self.scenes.pop()

    def quit(self):
        self.running = False

    def handle_events(self, events):
        if self.scenes:
            self.scenes[-1].handle_events(events)

    def update(self):
        if self.scenes:
            self.scenes[-1].update()

    def draw(self, screen):
        if self.scenes:
            self.scenes[-1].draw(screen)
