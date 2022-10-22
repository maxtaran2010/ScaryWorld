from hitboxes import Hitbox
import math


class EnemyBullet:
    def __init__(self, app, father, pos_to_hit, animation, speed, damage):
        self.temp_settings = app.temp_settings
        self.father = father
        self.app = app
        self.animation = animation
        self.screen = self.app.screen
        self.player = self.app.player
        self.pos = list(self.father.pos)
        dx, dy = pos_to_hit[0] - self.pos[0], pos_to_hit[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        self.dx, self.dy = dx / dist, dy / dist
        self.speed = speed
        self.size = self.animation.get_pygame_surface().get_size()
        self.damage = damage
        self.world = self.app.world
        self.hitbox = Hitbox(self.size, self.world)

    def update(self):
        self.pos[0] += self.speed * self.dx
        self.pos[1] += self.speed * self.dy
        self.hitbox.update(self.pos)
        if self.hitbox.hits(self.player.hitbox):
            self.player.damage(self.damage)
            self.world.remove(self)

    def draw(self):
        self.animation.draw(*self.pos)


class PlayerBullet:
    def __init__(self, app, father, pos_to_hit, animation, speed, damage):
        self.temp_settings = app.temp_settings
        self.father = father
        self.app = app
        self.animation = animation
        self.screen = self.app.screen
        self.player = self.app.player
        self.pos = list(self.father.pos)
        dx, dy = pos_to_hit[0] - self.pos[0], pos_to_hit[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        self.dx, self.dy = dx / dist, dy / dist
        self.speed = speed
        self.world = self.app.world
        self.size = self.animation.get_pygame_surface().get_size()
        self.hitbox = Hitbox(self.size, self.world)
        self.damage = damage * 8 if self.temp_settings.cheats else 0

    def update(self):
        self.pos[0] += self.speed * self.dx
        self.pos[1] += self.speed * self.dy
        self.hitbox.update(self.pos)
        d = self.hitbox.hit_any(self.world.dragon)
        if d:
            d.damage(self.damage)
            self.world.remove(self)

    def draw(self):
        self.animation.draw(*self.pos)
