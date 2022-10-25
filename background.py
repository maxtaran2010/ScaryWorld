import pygame
import animationStore
import random
from chances import chance


class Background:
    def __init__(self, app):
        self.app = app
        self.res = app.res
        self.screen = pygame.Surface(self.res)
        self.backgrounds = animationStore.Background(self)
        scale = self.backgrounds.default.scale * self.backgrounds.default.width
        for x in range(self.res[0]//scale):
            for y in range(self.res[1]//scale):
                random.choice(self.backgrounds.defaults).draw(x*scale+scale//2, y*scale+scale//2)
                if chance(5):
                    img = random.choice(self.backgrounds.tiles)
                    pos1 = [random.randint(img.real_size[0]//2, scale - img.real_size[0]//2),
                            random.randint(img.real_size[1]//2, scale - img.real_size[1]//2)]
                    pos1[0] += x*scale
                    pos1[1] += y*scale
                    img.draw(*pos1)
