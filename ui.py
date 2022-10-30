import pygame
import animationStore
import math


class UI:
    def __init__(self, app, font: pygame.font.Font):
        self.app = app
        self.font = font
        self.screen = app.screen
        self.width = app.width
        self.scenes = [[]]
        self.height = app.height
        self.scene = 0
        self.count_items = len(self.scenes[self.scene])

        self.click_timeout = 0

    def add(self, item, scene=None):
        if scene is None:
            scene = self.scene
        self.scenes[scene].append(item)
        self.count_items = len(self.scenes[scene])
        d = 1
        for i in self.scenes[scene]:
            i.pos = self.width // 2 - i.size[0] // 2, self.height // (self.count_items + 1) * d - i.size[1] // 2
            i.rect.x = i.pos[0]
            i.rect.y = i.pos[1]
            d += 1

    def draw(self):
        self.click_timeout -= 1
        self.screen.fill((0, 60, 48))
        for i in self.scenes[self.scene]:
            i.draw()

    def switch_scene(self, scene):
        self.scene = scene
        self.count_items = len(self.scenes[self.scene])

    def add_scene(self, move_to, scene=None):
        if scene is None:
            scene = []
        if move_to:
            self.scene = len(self.scenes)
        self.scenes.append([])
        for i in scene:
            self.add(i, len(self.scenes) - 1)


class Button:
    def __init__(self, ui: UI, text: str, action, args: tuple):
        self.ui = ui
        self.text = text
        self.action = action
        self.action_args = args
        self.textures = animationStore.UI(self.ui.app)
        self.text_render = self.ui.font.render(self.text, False, (255, 255, 255))
        self.text_size = self.text_render.get_size()
        self.num_pieces = math.ceil(self.text_size[0] / self.textures.button_center.real_size[0] + 6)
        self.peace_size = self.textures.button_center.real_size
        self.size = self.num_pieces * self.peace_size[0], self.peace_size[1]
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
            self.textures.button_center.draw(self.pos[0] + x, self.pos[1])
            x += self.peace_size[0]
        self.textures.button_end.draw(self.pos[0] + x, self.pos[1])
        self.ui.screen.blit(self.text_render, (self.pos[0] + self.size[0] // 2 - self.text_size[0] // 2,
                                               self.pos[1] + self.size[1] // 2 - self.text_size[1] // 2))

        if collides and pygame.mouse.get_pressed()[0] and self.ui.click_timeout <= 0:
            d = self.action(*self.action_args)
            if d:
                self.change_text(d)
            self.ui.click_timeout = 20

    def change_text(self, text):
        self.text = text
        self.text_render = self.ui.font.render(self.text, False, (255, 255, 255))
        self.text_size = self.text_render.get_size()


class Image:
    def __init__(self, img):
        self.img = img
        self.pos = 0, 0
        self.rect = pygame.rect.Rect((0, 0, 0, 0))
        self.size = img.real_size

    def draw(self):
        self.img.draw(*self.pos)


class Slider:
    def __init__(self, ui, default_value, max_v, name, action):
        self.ui = ui
        self.action = action
        self.value = default_value
        self.name_render = self.ui.font.render(name, False, (135, 134, 134))
        self.name_size = self.name_render.get_size()
        self.size = 300, 30 + self.name_render.get_height()
        self.pos = 0, 0
        self.rect = pygame.rect.Rect((*self.pos, *self.size))
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.max_value = max_v

    def draw(self):
        collides = self.rect.collidepoint(*pygame.mouse.get_pos())
        pc = self.value * self.size[0] // self.max_value
        pygame.draw.rect(self.ui.screen, (191, 189, 187),
                         (self.rect.x, self.pos[1], self.rect.w, self.rect.h))
        pygame.draw.rect(self.ui.screen, (54, 54, 54),
                         (self.rect.x + pc - 5, self.pos[1], 10, self.rect.h))
        text_render = self.ui.font.render(str(round(self.value, 1)), False, (255, 28, 28))
        text_size = text_render.get_size()
        self.ui.screen.blit(text_render, (self.pos[0] + 10,
                                          self.pos[1] + self.size[1] // 2 - text_size[1] // 2))
        self.ui.screen.blit(self.name_render, (self.pos[0] + self.size[0] // 2 - self.name_size[0] // 2,
                                               self.pos[1] + self.size[1] // 2 - self.name_size[1] // 2))
        if pygame.mouse.get_pressed()[0] and self.ui.click_timeout <= 0 and collides:
            self.value = ((pygame.mouse.get_pos()[0]-self.pos[0]) * self.max_value // self.size[0])+1
            self.ui.click_timeout = 20
            self.action(self.value)
