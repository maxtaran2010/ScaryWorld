from hitboxes import Hitbox
import math


class EnemyBullet:
    def __init__(self, app, father, pos_to_hit, animation, speed, damage, hard):
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
        self.speed = speed*self.app.temp_settings.hardness
        self.size = self.animation.get_pygame_surface().get_size()
        self.damage = damage
        self.world = self.app.world
        self.hitbox = Hitbox(self.size, self.world)
        self.hard = hard

    def update(self):
        self.pos[0] += self.speed * self.dx
        self.pos[1] += self.speed * self.dy
        self.hitbox.update(self.pos)
        if self.hitbox.hits(self.player.hitbox):
            self.player.give_damage(self.damage)
            self.world.remove(self)

    def draw(self):
        self.animation.draw(*self.pos)


class PlayerBullet:
    def __init__(self, app, father, animation, speed, damage, time, angle):
        self.temp_settings = app.temp_settings
        self.father = father
        self.app = app
        self.animation = animation
        self.screen = self.app.screen
        self.max_damage = damage
        self.player = self.app.player
        self.angle = angle
        self.pos = list(self.father.pos)
        self.dx, self.dy = math.sin(math.radians(angle)), math.cos(math.radians(angle))
        self.speed = speed
        self.world = self.app.world
        self.size = self.animation.get_pygame_surface().get_size()
        self.hitbox = Hitbox(self.size, self.world)
        self.damage = 100 if self.temp_settings.cheats else damage//self.app.temp_settings.hardness
        self.time = time
        self.animation.flip = (0, 1)

    def update(self):
        if not self.temp_settings.cheats:
            self.time -= 1
        self.pos[0] += self.speed * self.dx
        self.pos[1] += self.speed * self.dy
        self.hitbox.update(self.pos)
        d = self.hitbox.hit_any(self.world.preload.to_preload)
        if d:
            d.give_damage(self.damage)
            self.world.remove(self)
        x = self.hitbox.hit_any([EnemyBullet])
        if x:
            if not x.hard:
                x.dx = self.dx
                x.dy = self.dy
                x.player = x.father
                x.damage = x.father.hp // 2
            self.world.remove(self)
        if self.time <= 0:
            self.world.remove(self)
        if not self.temp_settings.cheats:
            self.damage -= self.max_damage // (self.time+1)

    def draw(self):
        self.animation.draw(*self.pos, self.angle)
