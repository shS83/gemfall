import pygame as pg
import commons as c
from pygame.locals import *

timer = pg.time.Clock()
pg.init()
c.screen = pg.display.set_mode([c.screen_w, c.screen_h], SHOWN)
pg.display.set_caption('fader')

faders = []


class fader:

    def __init__(self, delta=-1, color=(0, 0, 0), a_cap=0):
        self.surface = pg.Surface((c.screen_w, c.screen_h), SRCALPHA)
        self.delta = delta
        self.color = color
        if self.delta < 0:
            self.alpha = 255
            self.a_cap = 0 + a_cap
        else:
            self.alpha = 0
            self.a_cap = 255 - a_cap

    def update(self):
        if self.surface is not None:
            self.surface.fill(self.color)
            self.surface.set_alpha(self.alpha)
            c.screen.blit(self.surface, (0, 0))
        if (self.delta > 0 and self.alpha <= self.a_cap) or (self.delta < 0 and self.alpha >= self.a_cap):
            self.alpha += self.delta
        elif (self.delta > 0 and self.alpha >= self.a_cap) or (self.delta < 0 and self.alpha <= self.a_cap):
            if self.a_cap != 0:
                return True
            else:
                self.surface = None
                return True
        return False


def process_faders():
    for fade in faders:
        if fade.update():
            faders.remove(fade)


def main():

    running = True
    fadein = fader()
    bg_image = pg.image.load('taustakuva.jpg')
    faderz = [fadein]
    font = pg.font.SysFont('msgothic', 18)

    while running:

        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_r:
                    fadein = fader(delta=-fadein.delta)
                    faderz.clear()
                    faderz.append(fadein)
                if event.key == K_t:
                    faderz.append(fader(delta=2, color=(255, 0, 0), a_cap=128))

        c.screen.fill((0, 0, 0))
        c.screen.blit(bg_image, (0, 0))

        for fade in faderz:
            if fade.update():
                faderz.remove(fade)

        c.screen.blit(font.render(f'faders: {len(faderz)}', True, (255, 255, 255)), (50, 50))
        pg.display.flip()
        c.delta_time = 0.001 * timer.tick(144)


if __name__ == '__main__':
    main()
    pg.quit()
