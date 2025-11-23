import pygame
import os
from .settings import ASSETS_DIR, GAME_SIZE

class Assets:
    def __init__(self):
        self.images = {}
    
    def load(self):
        icon_path = os.path.join(ASSETS_DIR, 'graphics', 'ui', 'start_icon.png')

        sky_path = os.path.join(ASSETS_DIR, 'graphics', 'background', 'sky.png')

        self.images['icon'] = pygame.image.load(icon_path).convert_alpha()

        self.images['sky'] = pygame.image.load(sky_path).convert()
        self.images['sky'] = pygame.transform.smoothscale(self.images['sky'], GAME_SIZE)