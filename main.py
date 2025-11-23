import pygame
from src.settings import GAME_SIZE, FPS, CAPTION, MIN_SCREEN_SIZE
from src.loader import Assets
from src.states import MenuState

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(MIN_SCREEN_SIZE, pygame.RESIZABLE)

        self.assets = Assets()
        self.assets.load()

        pygame.display.set_caption(CAPTION)
        pygame.display.set_icon(self.assets.images['icon'])

        self.canvas = pygame.Surface(GAME_SIZE)
        self.state = MenuState(self)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.VIDEORESIZE:
                    size = max(event.w, MIN_SCREEN_SIZE[0]), max(event.h, MIN_SCREEN_SIZE[1])
                    self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                
                self.state.handle_event(event)

            self.state.update()
            self.state.draw(self.canvas)

            # get changed window size
            current_w, current_h = self.screen.get_size()
            scaled_canvas = pygame.transform.scale(self.canvas, (current_w, current_h))
            
            # Blit the scaled canvas to the real screen
            self.screen.blit(scaled_canvas, (0, 0))

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
