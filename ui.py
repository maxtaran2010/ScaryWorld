import pygame
import animationStore
import math


class UI:
    def __init__(self, app, font: pygame.font.Font):
        self.app = app
        self.font = font
        self.screen = app.screen
        self.width = app.width
        self.height = app.height
        self.items = []
        self.count_items = len(self.items)

    def add(self, item):
        self.items.append(item)
        self.count_items = len(self.items)
        d = 1
        for i in self.items:
            i.pos = self.width // 2 - i.size[0] // 2, self.height // (self.count_items+1) * d - i.size[1] // 2
            i.rect.x = i.pos[0]
            i.rect.y = i.pos[1]
            d += 1

    def draw(self):
        self.screen.fill((0, 60, 48))
        for i in self.items:
            i.draw()


class Button:
    def __init__(self, ui: UI, text: str, action, args: tuple):
        self.ui = ui
        self.text = text
        self.action = action
        self.action_args = args
        self.textures = animationStore.UI(self.ui.app)
        self.text_render = self.ui.font.render(self.text, True, (255, 255, 255))
        self.text_size = self.text_render.get_size()
        self.num_pieces = math.ceil(self.text_size[0]/self.textures.button_center.real_size[0]+6)
        self.peace_size = self.textures.button_center.real_size
        self.size = self.num_pieces*self.peace_size[0], self.peace_size[1]
        self.pos = 0, 0
        self.rect = pygame.rect.Rect((*self.pos, *self.size))
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def draw(self):
        collides = self.rect.collidepoint(*pygame.mouse.get_pos())

        np = self.num_pieces - 2
        x = 0
        self.textures.button_start.draw(*self.pos)
        x += self.peace_size[0]
        for i in range(np):
            self.textures.button_center.draw(self.pos[0]+x, self.pos[1])
            x += self.peace_size[0]
        self.textures.button_end.draw(self.pos[0]+x, self.pos[1])
        self.ui.screen.blit(self.text_render, (self.pos[0]+self.size[0]//2-self.text_size[0]//2,
                                               self.pos[1]+self.size[1]//2-self.text_size[1]//2))

        if collides and pygame.mouse.get_pressed()[0]:
            self.action(*self.action_args)


class Image:
    def __init__(self, img):
        self.img = img
        self.pos = 0, 0
        self.rect = pygame.rect.Rect((0, 0, 0, 0))
        self.size = img.real_size

    def draw(self):
        self.img.draw(*self.pos)
