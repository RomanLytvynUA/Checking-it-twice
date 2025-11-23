import pygame
from src.loader import Assets


class State:
    def __init__(self, game):
        self.game = game
        self.assets = Assets()
        self.assets.load()

    def handle_event(self, event):
        pass
    
    def update(self):
        pass
        
    def draw(self, surface):
        pass


class MenuState(State):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.state = GameState(self.game)

    def draw(self, surface):
        surface.blit(self.assets.images['sky'], (0, 0))

class GameState(State):
    def __init__(self, game):
        super().__init__(game)

    def handle_event(self, event):
        print(1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.state = MenuState(self.game)
        
    def draw(self, surface):
        surface.blit(self.assets.images['sky'], (0, 0))
        surface.fill(pygame.Color(255, 255, 255, 50))