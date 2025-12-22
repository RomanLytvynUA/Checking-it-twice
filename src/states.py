import pygame
from random import randint, uniform, choice
from math import ceil
from .sprites import Santa, Bg_Object, House, Gift
from .ui import MenuButton, GameButton, Scoreboard
from .settings import WORLD_SPEED, MUSIC_CHANNEL_ID, GROUND_LEVEL, BAR_HEIGHT, BAR_SIDE_MARGINS, GRAVITY, GAME_SIZE

class State:
    def __init__(self, game, assets):
        self.game = game
        self.assets = assets

    def handle_event(self, event):
        pass
    
    def update(self, dt):
        pass
        
    def draw(self, surface):
        pass


class MenuState(State):
    def __init__(self, game, assets):
        super().__init__(game, assets)
        self.santa = Santa(self.assets, 100, 300)
        
        self.music_channel = pygame.mixer.Channel(MUSIC_CHANNEL_ID)
        self.music_channel.play(self.assets.audio['menu'], loops=-1)

        sw = self.assets.images['sky'].get_width()

        tw = self.assets.images['title'].get_width()
        self.title_x = (sw / 2) - (tw / 2)
        self.title_y = self.assets.images['sky'].get_height() * 0.05

        btnw = self.assets.images['txt_btn'].get_width()
        btns_x = (sw / 2) - (btnw / 2)
        btns_offset_y = 100
        first_btn_y = self.title_y+self.assets.images['title'].get_height() + btns_offset_y

        self.start_btn = MenuButton(self.assets, btns_x, first_btn_y, "START ROUTE")
        self.settings_btn = MenuButton(self.assets, btns_x, first_btn_y+btns_offset_y, "SETTINGS")
        self.exit_btn = MenuButton(self.assets, btns_x, first_btn_y+btns_offset_y*2, "EXIT")

    def update(self, dt):
        self.santa.update(dt)
    
    def handle_event(self, event):
        if self.start_btn.handle_event(event):
            pygame.mixer.Channel(MUSIC_CHANNEL_ID).fadeout(500)
            self.game.state = GameState(self.game, self.assets)
        elif self.settings_btn.handle_event(event):
            pygame.mixer.Channel(MUSIC_CHANNEL_ID).fadeout(500)
        elif self.exit_btn.handle_event(event):
            return 1

    def draw(self, surface):
        surface.blit(self.assets.images['sky'], (0, 0))
        surface.blit(self.assets.images['menu_fg'], (0, 0))
        surface.blit(self.assets.images['title'], (self.title_x, self.title_y))
        
        surface.blit(self.santa.image, self.santa.rect)
        self.start_btn.draw(surface)
        self.settings_btn.draw(surface)
        self.exit_btn.draw(surface)

class GameState(State):
    def __init__(self, game, assets):
        super().__init__(game, assets)
        self.assets = assets
        self.game = game
        self.world_speed = WORLD_SPEED

        self.scoreboard = Scoreboard(self.assets, GAME_SIZE[0]-BAR_SIDE_MARGINS, BAR_HEIGHT)

        self.sw = self.assets.images['sky'].get_width()
        self.sh = self.assets.images['sky'].get_height()
        self.ground_level = GROUND_LEVEL

        self.santa = Santa(self.assets, 0, 0)
        self.santa.rect = self.santa.image.get_rect(center=(self.sw/2, self.sh/3.2))
        self.santa.set_state("flying")

        self.santa_sack_pos = (self.santa.rect.left+0.2*self.santa.image.get_width(), self.santa.rect.top+0.6*self.santa.image.get_height())

        self.land_g = pygame.sprite.Group()
        self.bg_slopes_g = pygame.sprite.Group()
        self.lights_g = pygame.sprite.Group()

        self.bg_pines_g = pygame.sprite.Group()
        self.fg_pines_g = pygame.sprite.Group()
        self.fg_slopes_g = pygame.sprite.Group()
        self.houses_g = pygame.sprite.Group()
        self.gifts_g = pygame.sprite.Group()
        self.coal_g = pygame.sprite.Group()

        self.initial_scene_setup()

        self.exit_btn = GameButton(self.assets, BAR_SIDE_MARGINS, BAR_HEIGHT, self.assets.images['exit_icon'])
        self.coal_btn = GameButton(self.assets, self.sw/2-1.4*self.assets.images['coal_icon'].get_width(), BAR_HEIGHT, self.assets.images['coal_icon'])
        self.gift_btn = GameButton(self.assets, self.sw/2+0.9*self.assets.images['gift_icon'].get_width(), BAR_HEIGHT, self.assets.images['gift_icon'])

        self.music_channel = pygame.mixer.Channel(MUSIC_CHANNEL_ID)
        self.music_channel.play(self.assets.audio['main'], loops=-1)


    def initial_scene_setup(self):
        # set up the bg pines
        for i in range(10):
            pos_x = randint(0, self.sw)
            image = pygame.transform.scale_by(self.assets.images['bg_pine'], uniform(0.9, 1.1))
            obj = Bg_Object(image, self.world_speed*0.3, (pos_x, self.ground_level-1-image.get_height()))
            self.bg_pines_g.add(obj)
        
        # set up the fg pines
        for i in range(3):
            pos_x = randint(0, self.sw)
            image = pygame.transform.scale_by(self.assets.images['fg_pine'], uniform(0.9, 1.1))
            obj = Bg_Object(image, self.world_speed, (pos_x, self.ground_level-1-image.get_height()))
            self.fg_pines_g.add(obj)

        # set up fg slopes
        for i in range(5):
            pos_x = randint(0, self.sw)
            image = pygame.transform.scale_by(choice(self.assets.images['fg_slopes']), uniform(0.9, 1.1))
            obj = Bg_Object(image, self.world_speed, (pos_x, self.ground_level-1-image.get_height()))
            self.fg_slopes_g.add(obj)


    def handle_houses(self, speed):
        if len(self.houses_g) == 0:
            pos_x = self.sw + randint(0, self.sw)
            house_asset = choice(self.assets.images['houses'])
            obj = House(house_asset['image'], speed, house_asset['chimney_offset_ratio'],
                         (pos_x, self.ground_level-1-house_asset['image'].get_height()), choice(["nice", "naughty"]))
            self.houses_g.add(obj)

        # kill house when no longer visible
        for sprite in self.houses_g.sprites():
            if sprite.rect.topright[0] < 0:
                sprite.kill()


    def prop(self, group, images, speed, max, max_scaling):
        # manages props such as bg pines, slopes etc.

        group_length = len(group)

        if group_length < max:
            pos_x = self.sw + randint(0, self.sw)
            image = pygame.transform.scale_by(choice(images), uniform(1-max_scaling, 1+max_scaling))
            obj = Bg_Object(image, speed, (pos_x, self.ground_level-1-image.get_height()))
            group.add(obj)
        
        # kill objects that are no longer visible
        for sprite in group.sprites():
            if sprite.rect.topright[0] < 0:
                sprite.kill()


    def parallax(self, group, image, default_pos, speed, flip_to_match=False):
        # manages the layers groups

        group_length = len(group)

        # number of instances of the given surface needed to cover the screen
        num = ceil(self.sw/image.get_width())
        
        if group_length < num*2:
            pos = default_pos
            should_flip = False
            
            if group_length > 0:
                last_sprite = group.sprites()[-1]
                pos = (last_sprite.rect.topright[0]-1, last_sprite.rect.topright[1])
                
                if flip_to_match:
                    last_was_flipped = getattr(last_sprite, 'is_flipped', False)
                    should_flip = not last_was_flipped

            if should_flip:
                image = pygame.transform.flip(image, True, False)

            new_layer = Bg_Object(image, speed, pos)
            new_layer.is_flipped = should_flip 
            
            group.add(new_layer)

        # kill layers that are no longer visible
        for sprite in group.sprites():
            if sprite.rect.topright[0] < 0:
                sprite.kill()


    def handle_event(self, event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or self.exit_btn.handle_event(event):
            self.game.state = MenuState(self.game, self.assets)

        if self.gift_btn.handle_event(event):
            gift = Gift(choice(self.assets.images['gifts']), self.santa_sack_pos[0], self.santa_sack_pos[1],
                         WORLD_SPEED, GRAVITY, GROUND_LEVEL+1, 'gift')
            self.gifts_g.add(gift)

        elif self.coal_btn.handle_event(event):
            coal = Gift(self.assets.images['coal'], self.santa_sack_pos[0], self.santa_sack_pos[1],
                        WORLD_SPEED, GRAVITY, GROUND_LEVEL, 'coal')
            self.coal_g.add(coal)

    def update(self, dt):
        self.parallax(self.land_g, self.assets.images['ground'], (0, self.ground_level), WORLD_SPEED)
        self.parallax(self.bg_slopes_g, self.assets.images['slopes'], (0, 
                                                                       self.ground_level-self.assets.images['slopes'].get_height()+1), 
                                                                       WORLD_SPEED*0.8, flip_to_match=True)
        self.parallax(self.lights_g, self.assets.images['lights'], 
                      (0, self.ground_level-self.assets.images['lights'].get_height()+1), WORLD_SPEED)

        self.prop(self.bg_pines_g, [self.assets.images['bg_pine']], WORLD_SPEED*0.3, 10, 0.1)
        self.prop(self.fg_pines_g, [self.assets.images['fg_pine']], WORLD_SPEED, 3, 0.1)
        self.prop(self.fg_slopes_g, self.assets.images['fg_slopes'], WORLD_SPEED, 5, 0.1)

        self.handle_houses(WORLD_SPEED)

        self.santa.update(dt)

        self.bg_slopes_g.update(dt)
        self.lights_g.update(dt)
        self.land_g.update(dt)
        self.bg_pines_g.update(dt)
        self.fg_pines_g.update(dt)
        self.fg_slopes_g.update(dt)
        self.houses_g.update(dt)

        house = self.houses_g.sprites()[0] if len(self.houses_g.sprites()) > 0 else None
        for sprite in self.gifts_g.sprites() + self.coal_g.sprites():
            sprite.fall(dt)
            sprite.shift(dt)
            if house:
                self.scoreboard.add_points(sprite.handle_chimney_collision(house.get_chimney_pos(), house.obedience))
            # kill if no longer visible
            if sprite.rect.topright[0] < 0:
                sprite.kill()
    
    def draw(self, surface):
        surface.blit(self.assets.images['sky'], (0, 0))

        surface.blit(self.assets.images['top_bar'], (0, -1))
        self.gift_btn.draw(surface)
        self.coal_btn.draw(surface)
        self.exit_btn.draw(surface)
        self.scoreboard.draw(surface)

        self.bg_pines_g.draw(surface)
        self.bg_slopes_g.draw(surface)
        self.fg_pines_g.draw(surface)
        self.lights_g.draw(surface)
        self.land_g.draw(surface)
        self.houses_g.draw(surface)
        surface.blit(self.santa.image, self.santa.rect)
        self.gifts_g.draw(surface)
        self.coal_g.draw(surface)
        self.fg_slopes_g.draw(surface)