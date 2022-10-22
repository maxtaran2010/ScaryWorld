from items import *
from dragon import *
from chances import chance


class World:
    def __init__(self, app):
        self.items = []
        self.app = app
        self.last_index = 0
        self.dragon = Dragon
        self.heart = Heart
        self.pre_load_dragons = []
        self.pre_load_hearts = []
        self.pre_loading = False

    def on_ready(self):
        for i in range(50):
            self.pre_load_dragons.append(Dragon(self.app))
        for i in range(5):
            self.pre_load_hearts.append(Heart(self.app))

    def update(self):
        if self.pre_loading and self.app.tick % 10 == 0:
            self.pre_load_hearts.append(Heart(self.app))
            self.pre_load_dragons.append(Dragon(self.app))

        if len(self.pre_load_dragons) <= 2:
            self.pre_loading = True
        elif len(self.pre_load_dragons) >= 50:
            self.pre_loading = False

        if chance(0.05) == 1:
            self.items.append(self.pre_load_hearts[0])
        if chance(3) == 1 and not self.pre_loading:
            self.items.append(self.pre_load_dragons[0])
            self.pre_load_dragons.pop(0)
        for i in self.items:
            i.update()
            if i.pos[0] < 0 or i.pos[0] > self.app.width or i.pos[1] < 0 or i.pos[1] > self.app.height:
                self.remove(i)

    def draw(self):
        for i in self.items:
            i.draw()

    def add_object(self, obj, *args):
        self.items.append(obj(self.app, *args))
        self.last_index += 1

    def remove(self, obj):
        self.items.remove(obj)
