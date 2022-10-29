from items import *
from dragon import *
import preload
from bars import MonsterBar
from chances import chance


class World:
    def __init__(self, app):
        self.monsters = 0
        self.items = []
        self.app = app
        self.last_index = 0
        self.to_kill = 25
        self.killed = 0
        self.preload = preload.Preload(self.app)
        self.bar = MonsterBar((self.app.width//2, 15), self.killed, self.to_kill, self.app.screen, app=self.app)
        self.app.bars.append(self.bar)
        self.current_monsters = 0

        self.dragon = Dragon

    def on_ready(self):
        self.preload.preload()
        self.app.need_to_load = False

    def countall(self, types):
        x = 0
        for i in self.items:
            if type(i) in types:
                x += 1
        return x

    def update(self):
        self.current_monsters = self.countall(self.preload.to_preload)
        if self.killed >= self.to_kill:
            self.app.ended = True
            self.app.win = True
        self.bar.update(self.killed)
        if chance(0.07) == 1:
            self.items.append(Heart(self.app))
        if self.monsters < self.to_kill:
            if self.current_monsters < 3:
                self.monsters += 1
                n = random.randint(0, len(self.preload.to_preload)-1)
                x = self.preload.preloads[n][0]
                self.items.append(x)
                self.preload.preloads[n].pop(0)
                self.preload.preloads[n].append(x)
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
