import pygame

from .utils import load_image, log_warn

class Cat:
    def __init__(self, screen_size, sprite) -> None:

        self.sprite = sprite
        self.size = [24,22] # used for collision
        self.pos = [
            (screen_size[0] / 2) - (self.size[0]/2),
            (screen_size[1] / 1.7) - (self.size[1]/2),
        ]

        self.show_hb = False
    
    def change_sprite(self,sprite):
        self.sprite = sprite

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, dt, mpos):
        if pygame.mouse.get_just_pressed()[0] and \
                self.get_rect().collidepoint(mpos):
            log_warn("Haven't implemented on_click")

        if pygame.key.get_just_pressed()[pygame.K_END]:
            self.show_hb = not self.show_hb
    
    def draw(self, surf:pygame.Surface):
        sprite_offset = [4,10]

        if self.show_hb:
            pygame.draw.rect(surf, (255,0,0), self.get_rect(), 1)

        shadow = pygame.Surface([16, 4], pygame.SRCALPHA)
        shadow.set_alpha(120)
        shadow.fill((0,0,0))
        surf.blit(shadow, [self.pos[0]+4, self.pos[1]+20])
        surf.blit(self.sprite, [self.pos[0] - sprite_offset[0], self.pos[1] - sprite_offset[1]])
