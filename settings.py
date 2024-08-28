# settings.py

WIDTH = 320
HEIGHT = 240
TITLE = "Breakout G13"
FPS = 60

BRICK_WIDTH = 16
BRICK_HEIGHT = 8

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720

BRICK_IMAGES = [
    "assets/images/bricks/brick1.png",
    "assets/images/bricks/brick2.png",
    "assets/images/bricks/brick3.png",
    "assets/images/bricks/brick4.png",
    "assets/images/bricks/brick5.png",
    "assets/images/bricks/brick6.png"
]

POWERUP_IMAGES = {
    'expand': "assets/images/powerups/expand.png",
    'duplicate': "assets/images/powerups/duplicate.png",
    'shoot': "assets/images/powerups/shoot.png"
}

AVAILABLE_POWERUPS = ['expand', 'duplicate', 'shoot']
POWERUP_PROBABILITY = 0.0  # Adjust the probability as needed
