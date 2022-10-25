import pygame
import animationStore


class Background:
    def __init__(self, app):
        self.app = app
        self.res = app.res
        self.screen = pygame.Surface(self.res)
        scale = 32
        self.backgrounds = animationStore.Background(self)
        # for x in range(self.res[0]//scale):
        #     for y in range(self.res[1]//scale):
        #         self.backgrounds.default.draw(x*scale, y*scale)



