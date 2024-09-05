# settings.py
import os

WIDTH = 320
HEIGHT = 240
TITLE = "Breakout G13"
FPS = 60

BRICK_WIDTH = 16
BRICK_HEIGHT = 8

WINDOW_WIDTH = 960 * 1.2
WINDOW_HEIGHT = 720 * 1.2

BRICK_IMAGES = [
    "assets/images/bricks/brick1.png",
    "assets/images/bricks/brick2.png",
    "assets/images/bricks/brick3.png",
    "assets/images/bricks/brick4.png",
    "assets/images/bricks/brick5.png",
    "assets/images/bricks/brick6.png",
    "assets/images/bricks/brick7.png"
]

POWERUP_IMAGES = {
    'expand': "assets/images/powerups/expand.png",
    'duplicate': "assets/images/powerups/duplicate.png",
    'shoot': "assets/images/powerups/shoot.png"
}

AVAILABLE_POWERUPS = ['expand', 'duplicate', 'shoot']
POWERUP_PROBABILITY = 0.0  # Adjust the probability as needed

# Directorio raíz de assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '../assets')

# Música
MUSIC_DIR = os.path.join(ASSETS_DIR, 'music')
MENU_MUSIC = os.path.join(MUSIC_DIR, 'menu-music.mp3')
GAMEPLAY_MUSIC = os.path.join(MUSIC_DIR, 'gameplay-music.mp3')
LOSE_MUSIC = os.path.join(MUSIC_DIR, 'lose-music.mp3')
VICTORY_MUSIC = os.path.join(MUSIC_DIR, 'victory-music.mp3')

# Efectos de sonido
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
BLOCK_DESTROYED_SOUND = os.path.join(SOUNDS_DIR, 'block_destroyed_sound.wav')
BOUNCE_SOUND = os.path.join(SOUNDS_DIR, 'bounce_sound.wav')
POWERUP_SOUND = os.path.join(SOUNDS_DIR, 'powerup_sound.wav')