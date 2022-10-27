import random


def chance(percentage):
    return random.randint(0, 100 // percentage) == 0


def pos(size, ssize):
    size = list(size)
    size[0] = size[0] // 2
    size[1] = size[1] // 2
    return [random.randint(size[0]+50, ssize[0]-size[0]), random.randint(size[1]+50, ssize[1]-size[1])]


class RandomMoving:
    def __init__(self, pos_d, res, speed, size):
        self.pos = pos_d
        self.speed = speed
        self.res = res
        self.size = size
        self.direction = [random.randint(-self.speed, self.speed), random.randint(-self.speed, self.speed)]

    def increase(self):
        if not (self.pos[0] < (self.size[0] + self.speed*3) or self.pos[0] > self.res[0] - self.speed*2 or self.pos[1] < (self.size[0] + self.speed*2) or self.pos[1] > self.res[1] - self.speed*3):
            if random.randint(0, 200) == 0:
                self.direction = [random.randint(-self.speed, self.speed), random.randint(-self.speed, self.speed)]
            self.pos[0] += self.direction[0]
            self.pos[1] += self.direction[1]
            return self.pos
        else:
            d = (self.direction[0]*-2, self.direction[1]*-2)
            self.direction = [self.direction[0]*(-2 if 3 < self.direction[0] < 3 else -1), self.direction[1]*(-2 if 3 < self.direction[0] < 3 else -1)]
            self.pos[0] += d[0]
            self.pos[1] += d[1]
            return self.pos
