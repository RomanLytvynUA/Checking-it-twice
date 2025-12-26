import pygame
from .settings import SCORE_TEXT_COLOR, PROMPT_OFFSET_Y, GAME_SIZE, GROUND_LEVEL
from random import choice, randint

class MenuButton:
    def __init__(self, assets, x, y, text=""):
        self.assets = assets

        self.image = self.assets.images['txt_btn']
        self.img_rect = self.image.get_rect(topleft=(x, y))

        self.text = text
        self.text_surface = self.assets.fonts['main'].render(text, True, (255, 255, 255))

        self.is_hovered = False
        self.is_pressed = False

        
    def draw(self, surface):
        btn = self.image.copy()

        # add text
        text_rect = self.text_surface.get_rect(center=btn.get_rect().center)
        btn.blit(self.text_surface, text_rect)

        current_scale = 0.98 if (self.is_pressed and self.is_hovered) else 1.0

        # scale
        scaled_btn = pygame.transform.scale_by(btn, current_scale)
        scaled_btn_rect = scaled_btn.get_rect(center=self.img_rect.center)

        # draw
        surface.blit(scaled_btn, scaled_btn_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.img_rect.collidepoint(event.pos)
            if self.is_hovered:
                self.image = self.assets.images['txt_btn_active']
            else:
                self.image = self.assets.images['txt_btn']

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_pressed and self.is_hovered:
                    self.is_pressed = False
                    return True
                self.is_pressed = False
        
        return False


class Scoreboard:
    def __init__(self, assets, x, y):
        self.assets = assets
        self.score = 0
        self.board_image = self.assets.images['scoreboard']
        
        self.board_rect = self.board_image.get_rect(topright=(x, y))
        
        self.update_text_surface()

    def update_text_surface(self):
        self.text_surface = self.assets.fonts['main'].render(f"{self.score}", True, SCORE_TEXT_COLOR)
        self.text_surface_rect = self.text_surface.get_rect(center=self.board_rect.center)

    def add_points(self, points):
        self.score += points
        if self.score < 0:
            self.score = 0
        self.update_text_surface()

    def draw(self, surface):
        surface.blit(self.board_image, self.board_rect)
        surface.blit(self.text_surface, self.text_surface_rect)


class GameButton:
    def __init__(self, assets, x, y, icon):
        self.assets = assets

        self.image = self.assets.images['ico_btn']
        self.img_rect = self.image.get_rect(topleft=(x, y))

        self.icon = icon

        self.is_hovered = False
        self.is_pressed = False

        
    def draw(self, surface):
        btn = self.image.copy()

        # add icon
        icon_rect = self.icon.get_rect(center=btn.get_rect().center)
        btn.blit(self.icon, icon_rect)

        current_scale = 0.98 if (self.is_pressed and self.is_hovered) else 1.0

        # scale
        scaled_btn = pygame.transform.scale_by(btn, current_scale)
        scaled_btn_rect = scaled_btn.get_rect(center=self.img_rect.center)

        # draw
        surface.blit(scaled_btn, scaled_btn_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.img_rect.collidepoint(event.pos)
            if self.is_hovered:
                self.image = self.assets.images['ico_btn_active']
            else:
                self.image = self.assets.images['ico_btn']

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_pressed and self.is_hovered:
                    self.is_pressed = False
                    return True
                self.is_pressed = False
        
        return False

class DossierPrompt(pygame.sprite.Sprite):
    def __init__(self, assets, chimney_pos):
        super().__init__()
        self.assets = assets

        self.original_image = self.assets.images['info_btn']
        pressed_scale = 0.9
        self.pressed_image = pygame.transform.scale_by(self.original_image, pressed_scale)

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(chimney_pos[0], chimney_pos[1] - PROMPT_OFFSET_Y))

        self.is_pressed = False
        self.is_hovered = False

    def update(self, dt, world_speed):
        self.rect.x -= world_speed * dt
        
        if self.is_pressed and self.is_hovered:
            current_center = self.rect.center
            self.image = self.pressed_image
            self.rect = self.image.get_rect(center=current_center)
        else:
            current_center = self.rect.center
            self.image = self.original_image
            self.rect = self.image.get_rect(center=current_center)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicked = self.is_pressed and self.is_hovered
                self.is_pressed = False
                if clicked:
                    return True
        
        return False


class Dossier:
    def __init__(self, assets, nice):
        self.shown = False
        self.assets = assets
        self.nice = nice
        self.image = self.assets.images['list_bg']
        self.rect = self.image.get_rect(center=(GAME_SIZE[0]//2, GROUND_LEVEL//2))
        self.line_spacing = 35

        self.behaviour_json = self.assets.behaviour
        self.behavior = []

        clicked_scale = 0.95
        self.original_ribbon = self.assets.images['ribbon']
        self.clicked_ribbon = pygame.transform.scale_by(self.original_ribbon, clicked_scale)
        self.ribbon_image = self.original_ribbon
        self.ribbon_rect = self.ribbon_image.get_rect(midtop=(self.rect.centerx, self.rect.top))
        self.is_hovered = False
        self.is_pressed = False

        self.portrait = choice(self.assets.images['portraits'])
        self.portrait_rect = self.portrait.get_rect(center=(self.rect.centerx, self.rect.top + 1.5*self.ribbon_rect.height))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.ribbon_image, self.ribbon_rect)

        if self.is_pressed and self.is_hovered:
            self.ribbon_image = self.clicked_ribbon
        else:
            self.ribbon_image = self.original_ribbon
        surface.blit(self.portrait, self.portrait_rect)

        for i, behav in enumerate(self.behavior):
            text_surface = self.assets.fonts['dossier'].render(behav, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.portrait_rect.bottom + self.line_spacing*(i+1)))
            surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.ribbon_rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicked = self.is_pressed and self.is_hovered
                self.is_pressed = False
                if clicked:
                    return True
        
        return False

    def generate_contents(self):
        self.portrait = choice(self.assets.images['portraits'])

        self.behavior = []
        deviation_index = randint(0, 2)
        for i in range(3):
            if i == deviation_index:
                if self.nice:
                    self.behavior.append(choice(self.behaviour_json['naughty']))
                else:
                    self.behavior.append(choice(self.behaviour_json['nice']))
            else:
                if self.nice:
                    self.behavior.append(choice(self.behaviour_json['nice']))
                else:
                    self.behavior.append(choice(self.behaviour_json['naughty']))