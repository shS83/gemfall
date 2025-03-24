import pygame as pg


class Zoom:

    def __init__(self, surface: pg.Surface, x=100, y=100, scale: float = 1.0, rotation: float = 1.0, sca_start: float = 1.0, rot_start: float = 1.0,
                 sca_max: float = None, rot_max: float = None, opacity: int = 255, opacity_delta: int = 0, opa_min: int = None, persistent=True, blink=False):
        self.x = x
        self.y = y
        self.surface = surface
        self.rotation = rotation
        self.scale = scale
        self.opacity = opacity
        self.rotation_max = rot_max
        self.scale_max = sca_max
        self.opacity_min = opa_min
        self.scale_start = sca_start
        self.rotation_start = rot_start
        self.s = sca_start
        self.r = rot_start
        self.opacity_delta = opacity_delta
        self.blit_surface = self.surface
        self.rot_done = False
        self.sca_done = False
        self.done = False
        self.persistent = persistent
        self.xmd = 1
        self.ymd = 1
        self.blink = blink
        self.blit_x = 0
        self.blit_y = 0
        self.moving = False

    def update(self, screen):
        if (self.scale > 1.0 and self.s < self.scale_max) or (self.scale < 1.0 and self.s > self.scale_max) or \
                not self.scale_max:
            self.sca_done = False
            self.s += self.scale - 1
        else:
            self.sca_done = True
        if (self.rotation > 1.0 and self.r < self.rotation_max) or (self.rotation < 1.0 and self.r > self.rotation_max)\
                or not self.rotation_max:
            self.rot_done = False
            self.r += self.rotation - 1
        else:
            self.rot_done = True

        if self.sca_done and self.rot_done and not self.opacity_min:
            self.done = True
        elif not self.scale_max and not self.opacity_min and self.rot_done:
            self.done = True
        elif not self.rotation_max and not self.opacity_min and self.sca_done:
            self.done = True

        if self.opacity_min is not False and self.opacity < self.opacity_min:
            self.done = True

        if (self.blink and self.opacity > 255) or (self.blink and self.opacity < 0):
            self.opacity_delta = -self.opacity_delta
        self.blit_surface = pg.transform.rotozoom(self.surface, self.r, self.s)
        self.blit_x = self.x - self.blit_surface.get_width() / 2
        self.blit_y = self.y - self.blit_surface.get_height() / 2
        self.opacity += self.opacity_delta
        self.blit_surface.set_alpha(self.opacity)
        if self.moving:
            self.x += self.xmd
            if self.x > screen.get_width() or self.x < 0:
                self.xmd = -self.xmd
            self.y += self.ymd
            if self.y > screen.get_height() or self.y < 0:
                self.ymd = -self.ymd


zoomers = []
zoomed = False


def add_zoomer(surface, x, y, scale, rotation, sca_start=1.0, rot_start=1.0, sca_max=False, rot_max=False, opacity=255,
               opacity_delta=0, opa_min=0, persistent=True, blink=False):

    zoomers.append(Zoom(surface, x, y, scale, rotation, sca_start, rot_start, sca_max, rot_max, opacity, opacity_delta,
                        opa_min, persistent, blink))


def blit_zoomers(screen):
    global zoomed

    for z in zoomers:
        if not z.done:
            z.update(screen)

        if z.done:
            if not z.persistent:
                zoomers.remove(z)
            zoomed = True

        screen.blit(z.blit_surface, (z.blit_x, z.blit_y))
