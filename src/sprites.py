import pygame

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames, x, y, animation_speed):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)


class Bg_Object(pygame.sprite.Sprite):
    def __init__(self, image, speed, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed

    def shift(self, dt):
        self.rect.x -= self.speed*dt

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, dt):
        self.shift(dt)


class Santa(AnimatedSprite):
    def __init__(self, assets, x, y):
        self.assets = assets
        self.state = 'idle'
        self.idle_speed = 2.2
        self.flying_speed = 7

        frames = self.assets.images['santa_idle']
        super().__init__(frames, x, y, self.idle_speed)
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            if self.state == 'flying':
                self.frames = self.assets.images['santa_flying']
                self.animation_speed = self.flying_speed
            elif self.state == 'idle':
                self.frames = self.assets.images['santa_idle']
                self.animation_speed = self.idle_speed
            self.frame_index = 0 

    def update(self, dt):
        # Call the parent to handle the animation math
        super().update(dt)