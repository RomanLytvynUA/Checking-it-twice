import pygame

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