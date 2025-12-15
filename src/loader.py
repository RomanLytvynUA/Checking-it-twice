import pygame
import os
from .settings import ASSETS_DIR, GAME_SIZE

class Assets:
    def __init__(self):
        self.images = {}
        self.fonts = {}
        self.audio = {}

    def resize(self, surface, size):
        return pygame.transform.smoothscale(surface, size)
    
    def adapt(self, surface, percentage):
        return pygame.transform.smoothscale(surface, (int(GAME_SIZE[0]*percentage), 
                                                         int(GAME_SIZE[0]*percentage/surface.get_width()*surface.get_height())))

    def load(self):
        self.audio['menu'] = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'audio', 'menu.ogg'))
        self.audio['main'] = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'audio', 'main.ogg'))
        self.audio['main'].set_volume(0.3)

        self.fonts['main'] = pygame.font.Font(os.path.join(ASSETS_DIR, 'fonts', 'main.ttf'), int(GAME_SIZE[0]*0.035))

        self.images['icon'] = pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'ui', 'start_icon.png')).convert_alpha()
        self.images['cursor'] = self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'ui', 'cursor.png')).convert_alpha(), 0.02)
        self.images['btn'] = self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'ui', 'btn.png')).convert_alpha(), 0.25)
        self.images['btn_active'] = self.resize(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'ui', 'btn_active.png')).convert_alpha(), self.images['btn'].get_size())

        self.images['houses'] = [{
            'image': self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'sprites', 'house_1.png')).convert_alpha(), 0.2),
            'chimney_offset_ratio': 0.69,
        },{
            'image': self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'sprites', 'house_2.png')).convert_alpha(), 0.2),
            'chimney_offset_ratio': 0.63,
        },{
            'image': self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'sprites', 'house_3.png')).convert_alpha(), 0.2),
            'chimney_offset_ratio': 0.63,
        },
        ]

        self.images['sky'] = self.resize(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'background', 'sky.png')).convert(), GAME_SIZE)
        self.images['ground'] = self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'background', 'ground.png')).convert(), 1)
        self.images['slopes'] = self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'background', 'bg_slope.png')).convert_alpha(), 1)
        self.images['lights'] = self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'background', 'lights.png')).convert_alpha(), 0.8)
        self.images['bg_pine'] = self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'background', 'bg_pine.png')).convert_alpha(), 0.1)
        self.images['fg_pine'] = self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'background', 'fg_pine.png')).convert_alpha(), 0.15)
        self.images['fg_slopes'] = []
        for i in range(4):
            self.images['fg_slopes'].append(self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'background', f'slope_{i}.png')).convert_alpha(), 0.1))
        


        self.images['menu_fg'] =  self.resize(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'ui', 'menu_fg.png')).convert_alpha(), GAME_SIZE)

        self.images['title'] = self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'ui', 'title.png')).convert_alpha(), 0.4)

        self.images['santa_idle'] = []
        for i in range(4):
            self.images['santa_idle'].append(self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'sprites', f'santa_idle{i}.png')).convert_alpha(), 0.25))
        
        self.images['santa_flying'] = []
        for i in range(8):
            self.images['santa_flying'].append(self.adapt(pygame.image.load(os.path.join(ASSETS_DIR, 'graphics', 'sprites', f'santa_flying_{i}.png')).convert_alpha(), 0.25))
        