import pygame, sys, threading, random, os
from .utils import load_image, load_images
from .cat import Cat
from .envelope import Envelope
from .db_req import get_unread_letters

class App:
    def __init__(self) -> None:

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
        pygame.init()
        self.screen = pygame.display.set_mode((300,300), pygame.NOFRAME)
        self.zoom = self.screen.get_size()[0] / 60
        self.display = pygame.Surface((60,60))
        self.clock = pygame.Clock()
        self.dt = 0

        self.bg_assets = load_images('bgs')
        self.bg_asset_idx = 0

        self.cat_assets = [load_image('cess.png'), load_image('rey.png')]
        self.cat_asset_idx = 0
        self.cat = Cat(self.display.get_size(), self.cat_assets[self.cat_asset_idx])

        self.envelopes = {}
        self.request_interval = 20
        self.request_timer = 0
    
        # just make sure to always do a self.res[0]
        self.res = [[]]

        self.thread = threading.Thread(target=get_unread_letters, args=(self.res,))
        self.thread.start()

    def _change_cat_sprite(self, n):
        self.cat_asset_idx = (self.cat_asset_idx + n) % len(self.cat_assets)
        self.cat.change_sprite(self.cat_assets[self.cat_asset_idx])

    def _change_background(self, n):
        self.bg_asset_idx = (self.bg_asset_idx + n) % len(self.bg_assets)

    def _update(self):
        adjusted_mpos = [
            pygame.mouse.get_pos()[0] / self.zoom,
            pygame.mouse.get_pos()[1] / self.zoom
        ]

        keys_pressed = pygame.key.get_just_pressed()

        if keys_pressed[pygame.K_LEFT]:
            self._change_cat_sprite(-1)
        elif keys_pressed[pygame.K_RIGHT]:
            self._change_cat_sprite(1)

        if keys_pressed[pygame.K_DOWN]:
            self._change_background(-1)
        elif keys_pressed[pygame.K_UP]:
            self._change_background(1)
        
        # nyet
        self.cat.update(self.dt, adjusted_mpos)

        # envelopes
        to_kill_id = []
        for id, envelope in self.envelopes.items():
            envelope.update(self.dt, adjusted_mpos)
            if envelope.state == 'to_kill':
                to_kill_id.append(id)

        # removing envelopes
        for id in to_kill_id:
            del self.envelopes[id]


        self.request_timer -= self.dt

        # if the thread died, it means it finished
        # so combine join it with the main thread
        if not self.thread.is_alive():
            self.thread.join()
            if self.request_timer <= 0:
                self._refresh_envelopes()
                self._request_unread()
                self.request_timer = self.request_interval

    def _draw(self):
        self.display.blit(self.bg_assets[self.bg_asset_idx])
        self.cat.draw(self.display)

        for _, envelope in self.envelopes.items():
            envelope.draw(self.display)

    def _refresh_envelopes(self):
        for response in self.res[0]:
            if response['id'] in self.envelopes: continue
            self._spawn_envelope(response['id'])

    def _spawn_envelope(self, id):
        self.envelopes[id] = Envelope([
            random.randint(0, self.display.get_size()[0] - 16),
            random.randint(0, self.display.get_size()[1] - 16),
        ], id)

    def _request_unread(self):
        self.thread = threading.Thread(target=get_unread_letters, args=(self.res,))
        self.thread.start()

    def run(self):
        while True:
            self.screen.fill((0,0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self._update()
            self._draw()
                
            adjusted_display = pygame.transform.scale(self.display, self.screen.size)
            self.screen.blit(adjusted_display, (0,0))   

            pygame.display.update()
            self.dt = self.clock.tick(60) / 1000.0
