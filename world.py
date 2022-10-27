from items import *
from dragon import *
from bars import MonsterBar
from chances import chance


class World:
    def __init__(self, app):
        self.monsters = 0
        self.items = []
        self.app = app
        self.last_index = 0
        self.dragon = Dragon
        self.heart = Heart
        self.pre_load_dragons = []
        self.pre_loading = False
        self.pre_loading_num = 5
        self.killed = 0
        self.app.max_loading_process += self.pre_loading_num
        self.bar = MonsterBar((self.app.width//2, 15), self.killed, self.pre_loading_num, self.app.screen, app=self.app)
        self.app.bars.append(self.bar)

    def on_ready(self):
        def preload():
            self.pre_load_dragons.append(Dragon(self.app))
            self.app.loading_process += 1
        self.pre_load_dragons = []
        for i in range(5):
            preload()

    def count(self, types):
        x = 0
        for i in self.items:
            if type(i) == types:
                x += 1
        return x

    def update(self):
        if self.killed >= self.pre_loading_num:
            self.app.ended = True
            self.app.win = True
        self.bar.update(self.killed)
        if chance(0.07) == 1:
            self.items.append(Heart(self.app))
        if chance(3) == 1 and self.monsters < self.pre_loading_num:
            if self.count(Dragon) < 2:
                self.monsters += 1
                self.items.append(self.pre_load_dragons[-1])
                self.pre_load_dragons.pop(-1)
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
        if obj in self.items:
            self.items.remove(obj)
