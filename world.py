from items import *
from dragon import *
from chances import chance


class World:
    def __init__(self, app):
        self.items = []
        self.app = app
        self.last_index = 0
        self.dragons = 0
        self.dragon = Dragon
        self.heart = Heart
        self.pre_load_dragons = []
        self.pre_load_hearts = []
        self.hearts = 0

    def on_ready(self):
        for i in range(20):
            self.pre_load_dragons.append(Dragon(self.app))
        for i in range(20):
            self.pre_load_dragons.append(Heart(self.app))

    def update(self):
        if chance(0.05) == 1 and self.hearts < 3:
            self.items.append(self.pre_load_hearts[0])
            self.pre_load_hearts.pop(0)
            self.hearts += 1
        if chance(3) == 1 and self.dragons < 3:
            self.items.append(self.pre_load_dragons[0])
            self.pre_load_dragons.pop(0)
            self.dragons += 1
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
