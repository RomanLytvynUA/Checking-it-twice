import os

MIN_SCREEN_SIZE = (640, 360)
GAME_SIZE = (1280, 720)
CAPTION = "Checking it twice!"

FPS = 60
WORLD_SPEED = 100

FILE_PATH = os.path.abspath(__file__)
SRC_DIR = os.path.dirname(FILE_PATH)
BASE_DIR = os.path.dirname(SRC_DIR)
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

GROUND_LEVEL = GAME_SIZE[1]/1.15
BAR_HEIGHT = GAME_SIZE[1]*0.04
BAR_SIDE_MARGINS = GAME_SIZE[1]*0.04

MUSIC_CHANNEL_ID = 7