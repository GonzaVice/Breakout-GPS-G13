import pygame

# Inicializar pygame mixer
pygame.mixer.init()

# Cargar sonidos
bounce_sound = pygame.mixer.Sound('assets/sounds/bounce_sound.wav')
block_destroyed_sound = pygame.mixer.Sound('assets/sounds/block_destroyed_sound.wav')
powerup_sound = pygame.mixer.Sound('assets/sounds/powerup_sound.wav')
lose_music = pygame.mixer.Sound('assets/music/lose-music.mp3')
victory_music = pygame.mixer.Sound('assets/music/victory-music.mp3')

# Cargar música
menu_music = 'assets/music/menu-music.mp3'
gameplay_music = 'assets/music/gameplay-music.mp3'

# Cuando la pelota rebote
def ball_hit():
    bounce_sound.play()

# Cuando se destruya un ladrillo
def brick_destroyed():
    block_destroyed_sound.play()

# Cuando se active un powerup
def activate_powerup():
    powerup_sound.play()

# Reproducir música de fondo
def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # -1 para que se repita indefinidamente

# Detener la música
def stop_music():
    pygame.mixer.music.stop()

# Cambiar música según el estado del juego
def start_game():
    play_music(gameplay_music)

def game_over():
    stop_music()
    lose_music.play()

def victory():
    stop_music()
    victory_music.play()

def menu():
    play_music(menu_music)
