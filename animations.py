import imageio
import pygame
import numpy


class Animation:
    def __init__(self, file, app, scale_coef, bg=None, delay=5):
        self.scale = scale_coef
        self.image = imageio.get_reader(file, format='GIF-PIL')
        self.len_frames = len(self.image)
        self.frames = []
        self.bg = bg
        for frame in self.image:
            t = []
            for row in frame:
                tt = []
                for pix in row:
                    tt.append(list(pix[:]))
                t.append(tt)
            self.frames.append(t)
        self.res = self.width, self.height = len(self.frames[0]), len(self.frames[0][0])
        self.frames = numpy.array(self.frames)
        self.current = 0
        self.screen = app.screen
        self.app = app
        self.delay = delay
        self.size = len(self.frames[0][0]), len(self.frames[0])
        self.playing = True

    def get_frame(self, number):
        assert number < self.len_frames, 'Incorrect frame number'
        return self.frames[number]

    def get_pygame_surface(self):
        d = self.current // self.delay
        d = d % self.len_frames
        surf = pygame.Surface(self.size)
        c = self.frames[d]
        surf = surf.convert_alpha()
        for y in range(len(c)):
            for x in range(len(c[0])):
                n = list(c[y][x])
                surf.set_at((x, y), n)
        surf = pygame.transform.scale(surf, (surf.get_width()*self.scale, surf.get_height()*self.scale))
        if self.bg is not None:
            surf.set_colorkey(self.bg)
        return surf

    def draw(self, x, y):
        if not self.playing:
            self.current = 0
        self.screen.blit(self.get_pygame_surface(), (x-(self.size[0]//2*self.scale), y-(self.size[1]//2*self.scale)))
        if self.playing:
            self.current += 1
