import os

MIN_SCREEN_SIZE = (640, 360)
GAME_SIZE = (1280, 720)
CAPTION = "Checking it twice!"

FPS = 60

FILE_PATH = os.path.abspath(__file__)
SRC_DIR = os.path.dirname(FILE_PATH)
BASE_DIR = os.path.dirname(SRC_DIR)
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')