import webbrowser

import pygame, math , threading

from .utils import load_image
from .db_req import mark_as_read

class Envelope:
    def __init__(self, pos, letter_id) -> None:
        self.pos = pos
        self.id = letter_id
        self.state = 'close'
        self.sprite = {
            'close': load_image('envelope_close.png'),
            'open': load_image('envelope_open.png'),
            'to_kill': load_image('envelope_open.png'),
        }

        self.theta = 0
        
        self.res = [[]]
        self.thread = self._make_thread()

    def _make_thread(self):
        return threading.Thread(target=mark_as_read, args=(self.id,self.res,))

    def _get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], 16, 16)
    
    def _click(self):
        self.state = 'open'
        self.thread.start()

    def update(self, dt, mpos):

        # if it's open, safe to say the thread has started
        if self.state == 'open':
            if not self.thread.is_alive() :
                self.thread.join()
                if self.res[0][0].get('failed'):
                    self.state = 'close'
                    self.thread = self._make_thread()
                else:
                    webbrowser.open(self.res[0][0]['content'])
                    self.state = 'to_kill'
            return

        if pygame.mouse.get_just_pressed()[0] and \
                self._get_rect().collidepoint(mpos):
            self._click()

        self.theta  += 2*dt; 
        if self.theta > 360: self.theta -= 360
        self.pos[1] += 5*math.sin(self.theta)*dt;

    def draw(self, surf):
        surf.blit(self.sprite[self.state], self.pos)

    
