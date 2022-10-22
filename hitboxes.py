import numpy
import pygame


class Hitbox:
    def __init__(self, size, world):
        self.size = self.width, self.height = list(size)
        self.pos = [0, 0]
        self.world = world

    def update(self, pos):
        self.pos = list(pos)

    def hits(self, hitbox2):
        x, y = numpy.array(self.pos)
        x2, y2 = numpy.array(hitbox2.pos)
        size = numpy.array(self.size)
        size2 = numpy.array(hitbox2.size)

        if abs(x - x2) < (size[0]+size2[0])//2 and abs(y - y2) < (size[1]+size2[1])//2:
            return 1
        else:
            return 0

    def hit_any(self, ntype):
        for item in self.world.items:
            hitbox2 = item.hitbox

            if ntype == type(item):
                if self.hits(hitbox2):
                    return item
        return 0
